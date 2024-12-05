import pandas as pd
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from openai import OpenAI
from flask import Flask
from flask_cors import CORS

# import giphy call fxn
from giphy_fxn import giphy_call

app = Flask(__name__)
CORS(app, origins=["*"])

# Ensure the OpenAI API key is set
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "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"


# Load the dataset and validate the CSV file exists
if not os.path.exists('./quotes.csv'):
    raise FileNotFoundError("The file quotes.csv does not exist.")

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


# Check if the FAISS index exists locally
if os.path.exists(index_path):
    print("Loading existing FAISS index...")
    try:
        vector_store = FAISS.load_local(index_path, OpenAIEmbeddings())
        print("Loaded existing FAISS index.")
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        print("Attempting to recreate the index.")
        os.makedirs(index_path, exist_ok=True)  # Ensure the directory exists
        vector_store = FAISS.from_texts(newTexts[:10000], OpenAIEmbeddings(), metadatas=indices[:10000])
        vector_store.save_local(index_path)
        print("Created and saved new FAISS index.")
else:
    print("FAISS index not found. Creating new index...")
    os.makedirs(index_path, exist_ok=True)
    vector_store = FAISS.from_texts(newTexts[:10000], OpenAIEmbeddings(), metadatas=indices[:10000])
    vector_store.save_local(index_path)
    print("Created and saved new FAISS index.")



# Initialize the language model
client = OpenAI()  # Set any necessary parameters here

@app.route('/data/<userInput>')
def get_quote(userInput):
    print(f"Received user input: {userInput}")
    try:
        # Perform similarity search
        quotes = vector_store.similarity_search(userInput, k=5)
    except Exception as e:
        print(f"Error during similarity search: {e}")
        return {'error': str(e)}

    prompt = ""
    for quote in quotes:
        prompt += quote.page_content + ' - ' + authors[int(quote.metadata['id'])] + "\n\n"
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": f"You are an expert in matching quotes. You will be given a list of quotes, and you must return the quote in the list that has the most similar meaning to the quote: '{userInput}'. You should only respond with the quote you select. Do not include anything else."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o",
    )
    
    print(prompt)
    print("Response")
    matchedQuote = response.choices[0].message.content
    print(matchedQuote)
    

    # Get the best keyword for searching GIPHY
    response_key = client.chat.completions.create(
        messages=[
            {"role": "system", "content": f"You are an expert in finding the keyword in a sentence. You will be given a sentence, and you must return the keyword. You should only respond with the word you select. Do not include anything else."},
            {"role": "user", "content": matchedQuote}
        ],
        model="gpt-4o",
    )
    
    keyword = response_key.choices[0].message.content
    print(f"Keyword for GIPHY: {keyword}")

    # Return result along with GIF URL
    return {
        'Output': matchedQuote,
        'gif_url': giphy_call(keyword)
    }
    
if __name__ == "__main__":
    # Run the Flask app
    app.run(port=8000, debug=True)  # Changed port to 8000 to avoid possible conflicts
