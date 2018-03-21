import cv2
import numpy as np
import command.configuration


world_coordinate=[]
screen_coordinates=[]


world_coordinate.append([0.0,0.0,0.0])
screen_coordinates.append([206.0,178.3])

world_coordinate.append([0.0,14.0,0.0])
screen_coordinates.append([112.0,180.0])

world_coordinate.append([3.8,0.0,0.0])
screen_coordinates.append([202.7,168.7])

world_coordinate.append([3.8,14.0,0.0])
screen_coordinates.append([115.7,168.7])

world_coordinate.append([101.6,0.0,0.0])
screen_coordinates.append([172.7,99.0])

world_coordinate.append([101.6-3.8,0.0,0.0])
screen_coordinates.append([174.0,101.0])

world_coordinate.append([101.6-3.8,3.8,0.0])
screen_coordinates.append([166.0,101.7])

world_coordinate.append([101.6-3.8-6.1+16.5, 74.4,0.0])
screen_coordinates.append([39.7,97.0])

world_coordinate.append([101.6-3.8-6.1, 74.4-3.8,0.0])
screen_coordinates.append([32.7,101.3])

world_coordinate.append([30.0, 27.4,0.0])
screen_coordinates.append([85.0,132.0])

world_coordinate.append([30.0+3.8, 27.4+3.8,0.0])
screen_coordinates.append([74.7,129.0])

world_coordinate.append([30.0+17.0, 27.4,0.0])
screen_coordinates.append([98.3,118.7])

world_coordinate.append([30.0+17.0-3.8, 27.4+3.8,0.0])
screen_coordinates.append([81.0,122.3])

world_coordinate.append([30.0+17.0, 51.0,0.0])
screen_coordinates.append([26.0,119.0])

world_coordinate.append([30.0+17.0-3.8, 51.0-3.8,0.0])
screen_coordinates.append([31.7,122.3])


retval, rvec, tvec=cv2.solvePnP(np.array(world_coordinate), np.array(screen_coordinates),
                                command.configuration.camera_matrix, command.configuration.dist_coefs)

print(retval)
print(rvec)
print(tvec)

def translateWorldCoords(ws, t):
    newW=[]
    for w in ws:
        newW.append([w[0]+t[0], w[1]+t[1], w[2]+t[2]])
    return newW

print(world_coordinate)



rTw=np.array([
    [1, 0, 0, 40],
    [0, 1, 0, -7.5],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
], dtype=float)

wTr=np.linalg.inv(rTw)

pr=rTw.dot(np.array([0,0,0,1], dtype=float))

rotation=cv2.Rodrigues(rvec)[0]

position=-rotation.transpose().dot(tvec)

cTw=np.concatenate((np.concatenate((rotation, tvec), axis=1), np.array([[0,0,0,1]], dtype=float)), axis=0)
wTc=np.linalg.inv(cTw)
print(cTw)


print(cTw.dot(np.array([0,0,0,1], dtype=float)))

print(cTw.dot(wTr))
