from flask import Flask
from flask import Flask, render_template
from threading import Thread

app = Flask('Artys Moderation')

@app.route('/')
def home():
    return render_template('coming_soon.html')

@app.route('/policies')
def policies():
  return render_template('coming_soon.html')

def run():
  app.run(host='0.0.0.0',port=8080)

def website():
    t = Thread(target=run)
    t.start() 