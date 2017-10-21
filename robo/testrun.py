import runconfiguration as conf
import move

import time
import os

from picamera import PiCamera


def doMove(m):
    m.setPower(100,100)

def doSense(tick, dataDir):
    camera.capture(dataDir+"/image"+str(tick)+".jpg")


if __name__=="__main__":

    camera = PiCamera()
    camera.start_preview()
    time.sleep(1)
    camera.resolution = (320, 240)
    camera.framerate = 30

    with move.Move() as m:
        tick=0
        tickTimes=[]
        startTime=time.time()

        dataDir=conf.dataBaseDir+"/data"+str(int(round(startTime*100)))
        if conf.collectData:
            os.mkdir(dataDir)

        #main loop
        while time.time()-startTime<conf.maxTime:
            tickStartTime=time.time()
            tickTimes.append(time.time())
            doMove(m)
            doSense(tick, dataDir)

            remainingTickTime=tickStartTime+conf.tickTime-time.time()
            if remainingTickTime >0:
                time.sleep(remainingTickTime)
            tick+=1

        m.setPower(0,0)

        if conf.collectData:
            with open(dataDir+"/tickTimes.csv", "w") as text_file:
                for tickTime in tickTimes:
                    text_file.write(str(tickTime)+"\n")

