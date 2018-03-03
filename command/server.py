from flask import Flask
import time
from picamera import PiCamera


app = Flask(__name__)

@app.route('/currenttime')
def current_time():
    return str(time.time())


if __name__=="__main__":

    camera = PiCamera()
    camera.start_preview()
    time.sleep(1)
    camera.resolution = (320, 240)
    camera.framerate = 30