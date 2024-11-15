import pandas as pd
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
import kagglehub



#print("Path to dataset files:", path)
# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable  routes

# Download latest version
path = kagglehub.dataset_download("manann/quotes-500k")
print(path)
# Load the dataset
df = pd.read_csv(os.path.join(path, 'quotes.csv'))

index_path = "faiss_index"

# Check if the FAISS index exists locally
if os.path.exists(index_path):
    # Load the existing FAISS index
    vector_store = FAISS.load_local(index_path, OpenAIEmbeddings())
    print("Loaded existing FAISS index")
else:
    # Create a FAISS vector store
    print("Creating Vector Store")
    vector_store = FAISS.from_texts(df['reply'].tolist(), OpenAIEmbeddings())
    # Save the new FAISS index locally
    vector_store.save_local(index_path)
    print("Created and saved new FAISS index")

# Initialize the language model
llm = OpenAI()  # Adjust parameters if necessary

@app.route('/data', methods=['POST'])
def get_quote():
    user_input = request.json.get('userInput')  # Get the user input from the request
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    quotes = vector_store.similarity_search(user_input)

    prompt = f"Out of all of the quotes below, return the one most similar to the quote '{user_input}': "
    
    for quote in quotes:
        prompt += "\n - " + quote.page_content
    
    print(prompt)

    result = llm.invoke(prompt)

    return jsonify({'Output': result})

if __name__ == "__main__":
    app.run(debug=True)
