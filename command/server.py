from flask import Flask
from flask import make_response
import time
from picamera import PiCamera
import io


app = Flask(__name__)
camera = PiCamera()


def initialize():
    camera.start_preview()
    time.sleep(1)
    camera.resolution = (320, 240)
    camera.framerate = 30

@app.route('/currenttime')
def current_time():
    return str(time.time())

@app.route('/currentimage.jpg')
def current_image():
    pid="img"
    image_stream = io.BytesIO()
    camera.capture(image_stream, 'jpeg')
    response = make_response(image_stream.getvalue())
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='currentimage.jpg')
    return response



if __name__=="__main__":
    initialize()
    app.run(host='0.0.0.0', port=5000)
