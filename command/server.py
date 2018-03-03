from flask import Flask
from flask import send_file
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

@app.route('/currentimage')
def current_image():
    pid="img"
    image_stream = io.BytesIO()
    camera.capture(image_stream, 'jpeg')
    return send_file(
        image_stream,
        mimetype='image/jpeg',
        as_attachment=True,
        attachment_filename='%s.jpg' % pid)



if __name__=="__main__":
    initialize()
    app.run(host='0.0.0.0', port=5000)
