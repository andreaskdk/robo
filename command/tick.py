import threading
import time
import configuration as conf
import io
import base64

class tick(threading.Thread):

    t=0
    tickTimes=[]
    camera=None
    move=None
    conf=None
    stopping=False
    mostRecentImageData=None

    def __init__(self, camera, move):
        threading.Thread.__init__(self)
        self.camera=camera
        self.move=move

    def doSense(self):
        imageData={}
        imageData["cameraStartTime"]=time.time()
        image_stream = io.BytesIO()
        self.camera.capture(image_stream, 'jpeg', use_video_port=True)
        imageData["image"]=base64.b64encode(image_stream.getvalue())
        imageData["cameraEndTime"]=time.time()
        self.mostRecentImageData=imageData

    def getData(self):
        data={}
        data["mostRecentImageData"]=self.mostRecentImageData
        return data

    def run(self):
        while not self.stopping:
            tickStartTime = time.time()
            self.tickTimes.append(time.time())
            # doMove(m)
            print("start sense: ", time.time())
            self.doSense()
            print("end sense: ", time.time())
            remainingTickTime = tickStartTime + conf.tickTime - time.time()
            if remainingTickTime > 0:
                print(remainingTickTime)
                time.sleep(remainingTickTime)
            self.t += 1

    def stop(self):
        self.stopping=True