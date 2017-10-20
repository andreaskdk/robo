import runconfiguration as conf

import time
import os

if __name__=="__main__":

    tick=0
    tickTimes=[]
    startTime=time.time()
    #main loop
    while time.time()-startTime<conf.maxTime:
        tickStartTime=time.time()
        tickTimes.append(time.time())

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