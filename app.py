from flask import Flask, render_template, request, session

import DBcm
import time
import random
import time

creds = {
    "host": "localhost",
    "user": "wordgameuser",
    "password": "wordgamepasswd",
    "database": "wordgamedb",
}

timeStart = 0.0
timeEnd = 0.0

global gameOver 
gameOver = False

results = []

sourceWords = open('source_words.txt').read().splitlines()
source_word = "spicy"

app = Flask(__name__)
app.secret_key = "awdlwaspdlwphfksmdkelfkdseofpdklsmelkf"

@app.get("/")
def EnterGame():

    session["source_word"] = ""
    session["input"] = ""

    session["timeStart"] = 0.0
    session["timeEnd"] = 0.0

    session["gameOver"] = True
   
    return render_template(
        "intro.html",
        title = "Word Game 4"
    )

@app.get("/intro")
def restart():

    session["source_word"] = ""
    session["input"] = ""

    session["timeStart"] = 0.0
    session["timeEnd"] = 0.0
   
    return render_template(
        "intro.html",
        title = "Word Game 4"
    )

@app.get("/startgame")
def startGame():
    global gameOver
    gameOver = False

    session["source_word"] = random.choice(sourceWords)
    print(session["source_word"])
   
    session["timeStart"] = time.time()

    return render_template(
       "startgame.html",
        title = "Word Game 4",
        sourceWord = session["source_word"]
    )

@app.route("/processwords", methods = ['POST'])
def processWords():
    timeStart = session["timeStart"]

    timeEnd = time.time() - timeStart
    timeEnd = round(timeEnd, 2)
    session["timeEnd"] = timeEnd

    print("TIME : " + str(timeEnd))
    
    input = request.form["words"]
    session["input"] = input

    ans = input.split()

    print(ans)

    errorList = []

    if checkAnsLen(ans):
        errorList.append(checkAnsLen(ans))
    if checkAnsDup(ans):
        errorList.append(checkAnsDup(ans))
    if checkAnsMatch(ans):
        errorList.append(checkAnsMatch(ans))
    if checkAnsValid(ans):
        errorList.append(checkAnsValid(ans))

    print(gameOver)

    if gameOver == False:
        return render_template(
            "winner.html",
            title = "Word Game 4",
            time = timeEnd
        )
    else:
        return render_template(
            "gameOver.html",
            title = "Word Game 4",
            Errors = errorList,
        )
    
@app.route("/leaderboard", methods = ['POST'])
def leaderboard():
    user = request.form["name"]
    source_word = session["source_word"]
    input = session["input"]
    time = session["timeEnd"]
    timeStr = str(time)

    mariaDBQuery = "insert into leaderboard (Time, User, Sourceword, Matches) values ('" + timeStr + "','" + user + "','" + source_word + "','" + input +"')"
    print(mariaDBQuery)

    addScore(mariaDBQuery)

    results = setupBoard()

    return render_template(
            "top10.html",
            title = "Word Game 4",
            leaderboard = results
        )

@app.route("/top10")
def top10():
    results = setupBoard()

    return render_template(
            "top10.html",
            title = "Word Game 4",
            leaderboard = results
        )

def checkAnsLen(ans):
     if (len(ans) < 7):
         print("Less than 7 words entered")
         global gameOver
         gameOver = True
         print(gameOver)
         print("Game Over")
         return  "Less than 7 words entered"

     for word in ans:
         if len(word) < 4:
             print(word + " is too short")
             gameOver = True
             print(gameOver)
             print("Game Over")
             return  word + " too short"
         else:
             print("Words Valid Length")

def checkAnsValid(ans):
    validWord = True
    
    for word in ans:
            if validWord == True:
                print(word)
                validWord = False
                with open("words_alpha.txt") as wordsfile:
                    for x in wordsfile:
                        if x.strip() == word:
                            print(word)
                            print("Good")
                            validWord = True
                            break
                print(validWord)
            else:
                print(word + ": Invalid Word")
                global gameOver
                gameOver = True
                print("Game Over")
                return word + " is Invalid"

def checkAnsMatch(ans):
    charFound = True




    source_word = session["source_word"]
    
    for word in ans:
        print("CURRENT CHECKED WORD : " + word)

        if word == source_word:
            print("Sourceword Used")
            global gameOver
            gameOver = True
            print("Game Over")
            return "Sourceword used"
        else:
            tempSourceWord = source_word
        
            print(source_word)
            
            for char in word:
                print("CHARS REMAINING : " + tempSourceWord)

                if charFound == True:
                    charFound = False
                    for sourceChar in tempSourceWord:
                        if char == sourceChar:
                            tempSourceWord = tempSourceWord.replace(char, "", 1)
                            charFound = True
                            break
                    print("Match")
                else:
                    print("Word Not in Source")
                    gameOver = True
                    print("Game Over")
                    return word + " not available within sourceword"

def checkAnsDup(ans):
    print(len(ans))
    print(len(set(ans)))

    if len(ans) != len(set(ans)):
        print("Duplicate Word")
        global gameOver
        gameOver = True
        print("Game Over")
        return "Duplicate word used"

def addScore(query):
    with DBcm.UseDatabase(creds) as db:
            db.execute(query)

def setupBoard():
    with DBcm.UseDatabase(creds) as db:
        db.execute("select * from leaderboard ORDER BY ABS(Time) limit 10")
        results = db.fetchall()

    return results

app.run(debug=True)