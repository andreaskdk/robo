import threading
import time

class tick(threading.Thread):

    tick=0
    tickTimes=[]
    camera=None
    move=None
    conf=None

    def __init__(self, camera, move, conf):
        self.camera=camera
        self.move=move


    def doSense(self):
        pass

    def run(self):
        tickStartTime = time.time()
        self.tickTimes.append(time.time())
        # doMove(m)
        self.doSense()

        remainingTickTime = tickStartTime + self.conf.tickTime - time.time()
        if remainingTickTime > 0:
            time.sleep(remainingTickTime)
        self.tick += 1
