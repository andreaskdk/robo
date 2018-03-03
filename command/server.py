from flask import Flask
import time

app = Flask(__name__)

@app.route('/currenttime')
def current_time():
    return str(time.time())