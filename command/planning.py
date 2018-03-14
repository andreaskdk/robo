import math

moves=[{"motor": [0, 0], "delta": [0.0, 0.0, 0.0]},
       {"motor": [100, 100], "delta": [2.56, 0.0, 0.0]},
       {"motor": [70, 100], "delta": [2.0, 0.0, 90.0/43.5/360*2*math.pi]},
       {"motor": [100, 70], "delta": [2.0, 0.0, -90.0/43.5/360*2*math.pi]},
       {"motor": [80, 100], "delta": [2.1, 0.0, 90.0/50/360*2*math.pi]},
       {"motor": [100, 80], "delta": [2.1, 0.0, -90.0/50/360*2*math.pi]}]

def getPositions(path, startX, startY, startDir):
    positions=[]
    positions.append([startX, startY, startDir])
    for p in path:
        prev=positions[-1]
        moveDelta=moves[p]["delta"]
        deltaX=moveDelta[0]*math.cos(prev[2]+moveDelta[2]/2)
        deltaY=moveDelta[0]*math.sin(prev[2]+moveDelta[2]/2)
        deltaDir=moveDelta[2]
        positions.append([prev[0]+deltaX, prev[1]+deltaY, (prev[2]+deltaDir)%(2*math.pi)])
    return positions


def getMotorPlan(ps):
    motorPlan=[];
    for p in ps:
        motorPlan.append(moves[p]["motor"])
    return motorPlan