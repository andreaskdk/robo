import runconfiguration as conf
import move

import time
import os

def doMove(m):
    m.setPower(100,100)


if __name__=="__main__":

    with move.Move() as m:
        tick=0
        tickTimes=[]
        startTime=time.time()
        #main loop
        while time.time()-startTime<conf.maxTime:
            tickStartTime=time.time()
            tickTimes.append(time.time())
            doMove(m)

            remainingTickTime=tickStartTime+conf.tickTime-time.time()
            if remainingTickTime >0:
                time.sleep(remainingTickTime)
            tick=+1

        if conf.collectData:
            dataDir=conf.dataBaseDir+"/data"+str(int(round(startTime*100)))
            os.mkdir(dataDir)
            with open(dataDir+"/tickTimes.csv", "w") as text_file:
                for tickTime in tickTimes:
                    text_file.write(str(tickTime)+"\n")