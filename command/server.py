from flask import Flask
from flask import make_response
from flask import request
import time
from picamera import PiCamera
import io
from tick import tick
from moving import Moving


app = Flask(__name__)

class DataServer:

    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (320, 240)
        self.camera.framerate = 30
        self.camera.start_preview()
        self.m = Moving()
        time.sleep(2)
        self.t=tick(self.camera, self.m)
        self.t.start()
        self.m.start()
        self.m.setMotorPlan([[100,100],[100,100],[100,100],[100,100],[100,100],[100,100],[100,100],[100,100],[100,100],[100,100]])

    def current_time(self):
        return str(time.time())

    def current_image(self):
        image_stream = io.BytesIO()
        self.camera.capture(image_stream, 'jpeg')
        response = make_response(image_stream.getvalue())
        response.headers.set('Content-Type', 'image/jpeg')
        return response

    def set_current_plan(self, motorPlan):
        self.m.setMotorPlan(motorPlan)

    def stop(self):
        self.m.stop()
        self.t.stop()


dataServer=DataServer()

@app.route('/currenttime')
def current_time():
    return dataServer.current_time()

@app.route('/currentimage.jpg')
def current_image():
    dataServer.current_image()

@app.route('/setcurrentplan', methods=['GET', 'POST'])
def set_current_plan():
    json=request.get_json()
    print(json)
    dataServer.set_current_plan(json['plan'])

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
    dataServer.stop()
