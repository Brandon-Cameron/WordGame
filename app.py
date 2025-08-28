from flask import Flask, render_template, request

import DBcm
import time
import random
import time

creds = {
    "host": "localhost",
    "user": "wordgameuser",
    "password": "wordgamepasswd",
    "database": "wordgameappdb",
}

timeStart = 0.0
timeEnd = 0.0

results = []

sourceWords = open('source_words.txt').read().splitlines()
source_word = ""

app = Flask(__name__)
app.secret_key = "awdlwaspdlwphfksmdkelfkdseofpdklsmelkf"

@app.get("/")
def EnterGame():
   
    return render_template(
        "intro.html",
        title = "Word Game 4"
    )

@app.get("/startgame")
def startGame():
    source_word = random.choice(sourceWords)
    print(source_word)
   
    timeStart = time.time()

    return render_template(
       "startgame.html",
        title = "Word Game 4",
        sourceWord = source_word
    )

@app.get("/processwords", methods = ['POST'])
def processWords():
    timeEnd = time.time() - timeStart
    
    input = request.form[words]
    source_word

app.run(debug=True)