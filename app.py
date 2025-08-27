from flask import Flask, render_template

import DBcm
import time

print("Hello")

creds = {
    "host": "localhost",
    "user": "wordgameuser",
    "password": "wordgamepasswd",
    "database": "wordgameappdb",
}

app = Flask(__name__)
app.secret_key = "awdlwaspdlwphfksmdkelfkdseofpdklsmelkf"

@app.get("/")
def test():
   return render_template(
        "gameover.html",
    )

app.run(debug=True)