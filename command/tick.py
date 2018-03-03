import threading
import time
import configuration as conf

class tick(threading.Thread):

    tick=0
    tickTimes=[]
    camera=None
    move=None
    conf=None

    def __init__(self, camera, move):
        self.camera=camera
        self.move=move

    def doSense(self):
        print(tick)

    def run(self):
        while True:
            tickStartTime = time.time()
            self.tickTimes.append(time.time())
            # doMove(m)
            self.doSense()

            remainingTickTime = tickStartTime + conf.tickTime - time.time()
            if remainingTickTime > 0:
                time.sleep(remainingTickTime)
            self.tick += 1
