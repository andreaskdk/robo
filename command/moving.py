import threading
import nxt
import configuration as conf
import time

class Moving(threading.Thread):

    powerLeft=0.0
    powerRight=0.0
    brick=None
    leftMotor=None
    rightMotor=None
    miniTick=0

    motorPlan=[]

    def __init__(self):
        pass

    def doMove(self):
        if len(self.motorPlan)==0:
            self.setPower(0.0,0.0)
        else:
            pass

    def run(self):
        while True:
            tickStartTime = time.time()
            self.doMove()
            remainingTickTime = tickStartTime + conf.miniTickTime - time.time()
            if remainingTickTime > 0:
                time.sleep(remainingTickTime)
            self.miniTick+=1


    def __enter__(self):
        self.brick = nxt.find_one_brick(method=nxt.locator.Method(bluetooth=False))
        self.leftMotor=nxt.Motor(self.brick, nxt.PORT_C)
        self.rightMotor=nxt.Motor(self.brick, nxt.PORT_A)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.rightMotor.run(0)
        self.leftMotor.run(0)
        self.brick.sock.device.reset()

    def setPower(self, pLeft, pRight):
        self.powerLeft=pLeft
        self.powerRight=pRight
        self.leftMotor.run(self.powerLeft)
        self.rightMotor.run(self.powerRight)
