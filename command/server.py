from flask import Flask
from flask import make_response
import time
from picamera import PiCamera
import io
from tick import tick
from moving import Moving


app = Flask(__name__)

class DataServer:
    camera = PiCamera()
    t=None
    m=None


    def __init__(self):
        self.camera.resolution = (320, 240)
        self.camera.framerate = 30
        self.camera.start_preview()
        self.m = Moving()
        time.sleep(2)
        self.t=tick(self.camera, self.m)
        self.t.start()

    def current_time(self):
        return str(time.time())

    def current_image(self):
        image_stream = io.BytesIO()
        self.camera.capture(image_stream, 'jpeg')
        response = make_response(image_stream.getvalue())
        response.headers.set('Content-Type', 'image/jpeg')
        return response

    def stop(self):
        self.t.stop()


dataServer=DataServer()

@app.route('/currenttime')
def current_time():
    return dataServer.current_time()

@app.route('/currentimage.jpg')
def current_image():
    dataServer.current_image()



if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
    dataServer.stop()
