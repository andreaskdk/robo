import threading
import nxt
import configuration as conf
import time

class Moving(threading.Thread):



    def __init__(self):
        threading.Thread.__init__(self)
        self.stopping = False
        self.powerLeft = 0.0
        self.powerRight = 0.0
        self.miniTick = 0
        self.motorPlan = []
        self.brick = nxt.find_one_brick(method=nxt.locator.Method(bluetooth=False))
        self.leftMotor=nxt.Motor(self.brick, nxt.PORT_C)
        self.rightMotor=nxt.Motor(self.brick, nxt.PORT_A)

    def doMove(self):
        if len(self.motorPlan)==0:
            self.setPower(0.0,0.0)
        else:
            p=self.motorPlan.pop()
            self.setPower(p[0], p[1])

    def run(self):
        while not self.stopping:
            tickStartTime = time.time()
            print("moving before move "+tickStartTime)
            self.doMove()
            print("moving after move")
            remainingTickTime = tickStartTime + conf.miniTickTime - time.time()
            if remainingTickTime > 0:
                time.sleep(remainingTickTime)
            self.miniTick+=1

    def stop(self):
        self.stopping = True
        self.rightMotor.run(0)
        self.leftMotor.run(0)
        self.brick.sock.device.reset()

    def setPower(self, pLeft, pRight):
        self.powerLeft=pLeft
        self.powerRight=pRight
        self.leftMotor.run(self.powerLeft)
        self.rightMotor.run(self.powerRight)

    def setMotorPlan(self, newMotorPlan):
        self.motorPlan=newMotorPlan
