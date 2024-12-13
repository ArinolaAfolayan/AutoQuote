import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "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"

index_path = "faiss_index"

if os.path.exists(index_path):
    print("Loading existing FAISS index...")
    vector_store = FAISS.load_local(index_path, OpenAIEmbeddings())
    print("Loaded existing FAISS index.")

prompt = "It is raining really hard today"
prompt = "If you put all your money into one stock and it doesn’t perform as expected, you could lose everything"
prompt = "lets take care of this issue before it turns into something bigger"
meanings = vector_store.similarity_search(prompt, k=3)

i = int(meanings[0].metadata['id'])

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

pop_culture_quotes = [
    "May the Force be with you. - Star Wars",
    "I’ll be back. - The Terminator",
    "To infinity and beyond! - Toy Story",
    "Why so serious? - The Dark Knight",
    "Here's looking at you, kid. - Casablanca",
    "I am inevitable. - Avengers: Endgame",
    "You can’t handle the truth! - A Few Good Men",
    "I’m the king of the world! - Titanic",
    "Winter is coming. - Game of Thrones",
    "With great power comes great responsibility. - Spider-Man",
    "I see dead people. - The Sixth Sense",
    "I solemnly swear that I am up to no good. - Harry Potter",
    "Live long and prosper. - Star Trek",
    "Just keep swimming. - Finding Nemo",
    "I’ll have what she’s having. - When Harry Met Sally",
    "Life is like a box of chocolates. - Forrest Gump",
    "Say hello to my little friend! - Scarface",
    "It’s-a me, Mario! - Super Mario",
    "I drink and I know things. - Game of Thrones",
    "Yabba Dabba Doo! - The Flintstones"
]


print("User input: " + prompt)
print("Matching meaning: " + meanings[0].page_content)
print("Matching quote: " + testTexts[i])
