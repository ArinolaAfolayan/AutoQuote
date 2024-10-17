import pandas as pd
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

def main():
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = ""

    # Load the dataset
    df = pd.read_csv('C:/Users/aiden/Source/Repos/AutoQuote/parent_reply.csv')


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
    llm = OpenAI()  # Set any necessary parameters here

    userInput = input("Enter a response: ")
    quotes = vector_store.similarity_search(userInput)

    prompt = f"Out of all of the quotes below, return the one most similar to the quote '{userInput}': "
    
    for quote in quotes:
        prompt += "\n - " + quote.page_content
    
    print(prompt)

    result = llm.invoke(prompt)
    
    print(result)
    
if __name__ == "__main__":
    result = main()
