from flask import Flask
from flask import make_response
import time
from picamera import PiCamera
import io
import tick
import configuration


app = Flask(__name__)
camera = PiCamera()
t=None


def initialize():
    camera.resolution = (320, 240)
    camera.framerate = 30
    camera.start_preview()
    time.sleep(2)
    t=tick(camera, None)

@app.route('/currenttime')
def current_time():
    return str(time.time())

@app.route('/currentimage.jpg')
def current_image():
    image_stream = io.BytesIO()
    camera.capture(image_stream, 'jpeg')
    response = make_response(image_stream.getvalue())
    response.headers.set('Content-Type', 'image/jpeg')
    return response



if __name__=="__main__":
    initialize()
    app.run(host='0.0.0.0', port=5000)
