from flask import Flask
from flask import make_response
from flask import request
import time
from picamera import PiCamera
import io
from tick import tick
from moving import Moving
import json
import traceback



app = Flask(__name__)

class DataServer:

    def __init__(self):
        try:
            self.camera = PiCamera()
            self.camera.resolution = (320, 240)
            self.camera.framerate = 30
            self.camera.start_preview()
            self.m=None
            #self.m = Moving()
            time.sleep(2)
            self.t=tick(self.camera, self.m)
            self.t.start()
            #self.m.start()
    #        self.m.setMotorPlan([[100,100],[100,100],[100,100],[100,100],[100,100],[100,100],[100,100],[100,100],[100,100],[100,100]])
        except:
            print("FAILED")
            traceback.print_exc()

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
        try:
            self.camera.stop_preview()
            self.camera.close()
        except:
            pass
        #self.m.stop()
        self.t.stop()


dataServer=DataServer()

@app.route('/currenttime')
def current_time():
    return dataServer.current_time()

@app.route('/currentimage.jpg')
def current_image():
    try:
        return dataServer.current_image()
    except:
        traceback.print_stack()

@app.route('/setcurrentplan', methods=['GET', 'POST'])
def set_current_plan():
    values=request.values
    print(values)
    dataServer.set_current_plan(json.loads(values['plan']))

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, threaded=False)
    dataServer.stop()
