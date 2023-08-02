from flask import Flask
from threading import Thread

app = Flask('Artys Moderation Uptime')

@app.route('/')
def home():
    return "Heyo! You found the secret sauce, my uptime website! There's nothing much here at the moment, but congrats for finding me."

def run():
  app.run(host='0.0.0.0',port=8080)

def uptime_check():
    t = Thread(target=run)
    t.start() 