from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Server Host Connected and Synced to Main Code."

def run():
  app.run(host='0.0.0.0',port=1215)

def keep_alive():  
    t = Thread(target=run)
    t.start()