import pandas as pd
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from openai import OpenAI
from flask import Flask
from flask_cors import CORS
from giphy_fxn import giphy_call

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

client = OpenAI()


testTexts = [
    "A picture is worth a thousand words",
    "Actions speak louder than words",
    "Better late than never",
    "Birds of a feather flock together",
    "Break the ice",
    "Burn the midnight oil",
    "Don’t count your chickens before they hatch",
    "Don’t cry over spilled milk",
    "Every cloud has a silver lining",
    "Fortune favors the bold",
    "Give someone the benefit of the doubt",
    "Haste makes waste",
    "If it ain’t broke, don’t fix it",
    "It takes two to tango",
    "Kill two birds with one stone",
    "Let the cat out of the bag",
    "Make hay while the sun shines",
    "No pain, no gain",
    "The early bird catches the worm",
    "You can’t judge a book by its cover",
    "When in Rome, do as the Romans do",
    "A stitch in time saves nine",
    "All that glitters is not gold",
    "An apple a day keeps the doctor away",
    "Barking up the wrong tree",
    "Beat around the bush",
    "Bite off more than you can chew",
    "Burn bridges",
    "Call it a day",
    "Caught between a rock and a hard place",
    "Curiosity killed the cat",
    "Cut corners",
    "Don’t bite the hand that feeds you",
    "Don’t judge a book by its cover",
    "Don’t put all your eggs in one basket",
    "Every dog has its day",
    "Good things come to those who wait",
    "Hit the nail on the head",
    "Ignorance is bliss",
    "It’s a small world",
    "Keep your chin up",
    "Kill them with kindness",
    "Laughter is the best medicine",
    "Let bygones be bygones",
    "Live and learn",
    "Look before you leap",
    "Loose lips sink ships",
    "Measure twice, cut once",
    "Money doesn’t grow on trees",
    "Necessity is the mother of invention",
    "No use crying over spilled milk",
    "Old habits die hard",
    "One man’s trash is another man’s treasure",
    "Out of sight, out of mind",
    "Practice makes perfect",
    "Rome wasn’t built in a day",
    "Slow and steady wins the race",
    "Speak of the devil",
    "The grass is always greener on the other side",
    "The pen is mightier than the sword",
    "The squeaky wheel gets the grease",
    "There’s no place like home",
    "There’s no such thing as a free lunch",
    "Time flies when you’re having fun",
    "Too many cooks spoil the broth",
    "Two heads are better than one",
    "When it rains, it pours",
    "You can lead a horse to water, but you can’t make it drink",
    "You can’t have your cake and eat it too",
    "You can’t teach an old dog new tricks",
    "Your guess is as good as mine",
    "Absence makes the heart grow fonder",
    "Actions have consequences",
    "Beggars can’t be choosers",
    "Better safe than sorry",
    "Easy come, easy go",
    "Every rose has its thorn",
    "Good things come in small packages",
    "Hindsight is 20/20",
    "If the shoe fits, wear it",
    "If you can’t beat them, join them",
    "It’s always darkest before the dawn",
    "Let sleeping dogs lie",
    "Life is a journey, not a destination",
    "Lightning never strikes twice in the same place",
    "Man proposes, God disposes",
    "Necessity knows no law",
    "No man is an island",
    "One step at a time",
    "Penny wise and pound foolish",
    "The devil is in the details",
    "There’s more than one way to skin a cat",
    "Variety is the spice of life",
    "What doesn’t kill you makes you stronger",
    "What goes around comes around",
    "Where there’s smoke, there’s fire",
    "You reap what you sow",
    "Don’t judge a man until you’ve walked a mile in his shoes",
    "The proof is in the pudding",
    "It's raining cats and dogs"
]


meanings = []

for text in testTexts:
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": 
                f"""
                    You are an expert in determining the meaning of a phrase. You will be given a single phrase, and you must return the meaning of the phrase in a single sentence.
                    
                    Simply respond with the meaning of the phrase. Do not include anything else.
                    
                    Use common language when expressing the meaning of the phrase.
                    
                    
                    Below are some examples of inputs you will receive and the output you should return:
                    
                    input: it's a piece of cake, output: something is easy
                    
                    input: it's raining cats and dogs, output: it's raining heavily
                    
                    input: kill two birds with one stone, output: to accomplish two things with one action
              
                """},
            {"role": "user", "content": text}
        ],
        model="gpt-4o",
    )

    meaning = response.choices[0].message.content
    meanings.append(meaning)
    
testIndices = []
for i in range(len(testTexts)):
    print(testTexts[i])
    print(meanings[i])
    print()
    testIndices.append({'id': str(i)})


index_path = "faiss_index"

os.makedirs(index_path, exist_ok=True)
vector_store = FAISS.from_texts(meanings, OpenAIEmbeddings(), metadatas=testIndices)
vector_store.save_local(index_path)
print("Created and saved new FAISS index.")


#quotes = vector_store.similarity_search(userInput, k=5)
