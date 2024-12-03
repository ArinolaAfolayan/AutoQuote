import pandas as pd
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from langdetect import detect
from googletrans import Translator
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
translator = Translator()

def embed_text(text):
    return embedding_model.encode(text)
def translate_to_english(text, source_lang):
    if source_lang != "en":
        return translator.translate(text, src=source_lang, dest="en").text
    return text

def translate_to_user_language(text, target_lang):
    return translator.translate(text, src="en", dest=target_lang).text


# import giphy call fxn
from giphy_fxn import giphy_call

app = Flask(__name__)

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
llm = OpenAI(model="text-davinci-003")  # You can adjust the model if needed

@app.route('/data/<userInput>')
def get_quote(userInput):
    print(f"Received user input: {userInput}")
    user_language = detect(userInput)

    translated_input = translate_to_english(userInput, user_language)
    print(f"Translated input: {translated_input}")

    user_embedding = OpenAIEmbeddings().embed_query(translated_input)
    top_quotes = vector_store.similarity_search_by_vector(user_embedding, k=5)

    # Refine results with LLM
    prompt = (
        f"The user provided the input: '{translated_input}'. Below are five quotes retrieved based on similarity:\n"
        + "\n".join([f"{i+1}. {quote.page_content}" for i, quote in enumerate(top_quotes)])
        + "\n\nSelect the single most relevant quote for the user's input and explain your reasoning."
    )
    refined_result = llm.invoke(prompt)

    final_result = translate_to_user_language(refined_result, user_language) if user_language != "en" else refined_result

    return jsonify({"userInput": userInput, "refinedQuote": final_result})
    # try:
    #     # Perform similarity search
    #     quotes = vector_store.similarity_search(userInput, k=5)
    #     print(f"Found quotes: {quotes}")
    # except Exception as e:
    #     print(f"Error during similarity search: {e}")
    #     return {'error': str(e)}

    # prompt = f"Out of all of the quotes below, return the one that could be used in place of the quote '{userInput}'. You should only respond with the quote you select. Do not include anything else.\n\n"
    # for quote in quotes:
    #     prompt += "\n" + quote.page_content + ' - ' + authors[int(quote.metadata['id'])]

    # try:
    #     # Get the result from the language model
    #     result = llm.invoke(prompt)
    #     print(f"LLM response: {result}")
    # except Exception as e:
    #     print(f"Error with LLM invoke: {e}")
    #     return {'error': str(e)}

    # # Get the best keyword for searching GIPHY
    # keyword = llm.invoke(f'Find the best one keyword of this that can be used to search GIPHY: {result}')
    # print(f"Keyword for GIPHY: {keyword}")

    # # Return result along with GIF URL
    # return {
    #     'Output': result,
    #     'gif_url': giphy_call(keyword)
    # }
if __name__ == "__main__":
    app.run(debug=True)
