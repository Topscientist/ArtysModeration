from flask import Flask
from threading import Thread

app = Flask('Artys Moderation Uptime')

@app.route('/')
def home():
    return "Heyo! I am alive, wheeee"

def run():
  app.run(host='0.0.0.0',port=8080)

def uptime_check():
    t = Thread(target=run)
    t.start() 