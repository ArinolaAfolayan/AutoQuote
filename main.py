import pandas as pd
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "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"

# Load the dataset
df = pd.read_csv('C:/Users/aiden/Source/Repos/AutoQuote/quotes.csv')

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
    # Load the existing FAISS index
    vector_store = FAISS.load_local(index_path, OpenAIEmbeddings())
    print("Loaded existing FAISS index")
else:
    # Create a FAISS vector store
    print("Creating Vector Store")
    vector_store = FAISS.from_texts(newTexts[:1000], OpenAIEmbeddings(), metadatas=indices[:1000])
    # Save the new FAISS index locally
    vector_store.save_local(index_path)
    print("Created and saved new FAISS index")

# Initialize the language model
llm = OpenAI()  # Set any necessary parameters here

@app.route('/data/<userInput>')
def get_quote(userInput):
    quotes = vector_store.similarity_search(userInput, k=5)

    prompt = f"Out of all of the quotes below, return the one most similar to the quote '{userInput}': "
    for quote in quotes:
        print(quote.metadata)
        prompt += "\n - " + quote.page_content + ' - ' + authors[int(quote.metadata['id'])]
    
    print(prompt)

    result = llm.invoke(prompt)
    
    return {'Output': result}
    
if __name__ == "__main__":
    app.run(debug=True)
