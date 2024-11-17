import pandas as pd
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from flask import Flask
from flask_cors import CORS
from giphy_fxn import giphy_call

app = Flask(__name__)
CORS(app)

# Ensure the OpenAI API key is set
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "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"

# Load the dataset and validate the CSV file exists
if not os.path.exists('./quotes.csv'):
    raise FileNotFoundError("The file quotes.csv does not exist.")

df = pd.read_csv('./quotes.csv')

import os
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load the dataset
df = pd.read_csv('./quotes.csv')

texts = df['quote'].to_list()
authors = df['author'].to_list()
newTexts = []
indices = []
newAuthors = []

for i in range(len(texts)):
    indices.append({'id': str(i)})
    newTexts.append(str(texts[i]))
    newAuthors.append(str(authors[i]))

index_path = "faiss_index"

index_path = "faiss_index"

# Check if the FAISS index exists locally
if os.path.exists(index_path):
    print("Loading existing FAISS index...")
    try:
        vector_store = FAISS.load_local(index_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
        print("Loaded existing FAISS index.")
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        print("Attempting to recreate the index.")
        os.makedirs(index_path, exist_ok=True)  # Ensure the directory exists
        vector_store = FAISS.from_texts(newTexts[:1000], OpenAIEmbeddings(), metadatas=indices[:1000])
        vector_store.save_local(index_path)
        print("Created and saved new FAISS index.")
else:
    print("FAISS index not found. Creating new index...")
    os.makedirs(index_path, exist_ok=True)
    vector_store = FAISS.from_texts(newTexts[:1000], OpenAIEmbeddings(), metadatas=indices[:1000])
    vector_store.save_local(index_path)
    print("Created and saved new FAISS index.")



# Initialize the language model
llm = OpenAI()  # Set any necessary parameters here

@app.route('/data/<userInput>')
def get_quote(userInput):
    print(f"Received user input: {userInput}")
    try:
        # Perform similarity search
        quotes = vector_store.similarity_search(userInput, k=5)
        print(f"Found quotes: {quotes}")
    except Exception as e:
        print(f"Error during similarity search: {e}")
        return {'error': str(e)}

    prompt = f"Out of all of the quotes below, return the one that could be used in place of the quote '{userInput}'. You should only respond with the quote you select. Do not include anything else.\n\n"
    for quote in quotes:
        prompt += "\n" + quote.page_content + ' - ' + authors[int(quote.metadata['id'])]

    try:
        # Get the result from the language model
        result = llm.invoke(prompt)
        print(f"LLM response: {result}")
    except Exception as e:
        print(f"Error with LLM invoke: {e}")
        return {'error': str(e)}

    # Get the best keyword for searching GIPHY
    keyword = llm.invoke(f'Find the best one keyword of this that can be used to search GIPHY: {result}')
    print(f"Keyword for GIPHY: {keyword}")

    # Return result along with GIF URL
    return {
        'Output': result,
        'gif_url': giphy_call(keyword)
    }

if __name__ == "__main__":
    # Run the Flask app
    app.run(port=8000, debug=True)  # Changed port to 8000 to avoid possible conflicts
