
import nxt

class Move:

    powerLeft=0.0
    powerRight=0.0
    brick=None
    leftMotor=None
    rightMotor=None

    def __enter__(self):
        self.brick = nxt.find_one_brick(method=nxt.locator.Method(bluetooth=False))
        self.leftMotor=nxt.Motor(self.brick, nxt.PORT_C)
        self.rightMotor=nxt.Motor(self.brick, nxt.PORT_A)

    def __exit__(self, exc_type, exc_value, traceback):
        self.rightMotor.run(0)
        self.leftMotor.run(0)
        self.brick.sock.device.reset()

    def setPower(self, pLeft, pRight):
        self.powerLeft=pLeft
        self.powerRight=pRight
        self.leftMotor.run(self.powerLeft)
        self.rightMotor.run(self.powerRight)
