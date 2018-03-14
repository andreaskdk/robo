import requests
import math

#r = requests.post('http://robo:5000/setcurrentplan', data = {'plan':'[[-100,-100], [-100,-100], [-100,-100], [-100,-100], [-100,-100], [-100,-100]]'})


#r = requests.post('http://robo:5000/setcurrentplan', data = {'plan': str([[100,70] for x in range(10)])})


import command.planning
#path=[1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1]
#path=[1 for _ in range(10)]+[2 for _ in range(10)]+[3 for _ in range(20)]+[2 for _ in range(10)]+[1 for _ in range(10)]
path=[4 for _ in range(50)]
mp=command.planning.getMotorPlan(path)
print(command.planning.getPositions(path, 0.0,0.0,math.pi/2)[-1])
#r = requests.post('http://robo:5000/setcurrentplan', data = {'plan': str(mp)})

import command.world
w=command.world.world()
w.positions=command.planning.getPositions(path, 0.0, 0.0, math.pi/2)
w.getSVG(800,800).saveas("curpath.svg")