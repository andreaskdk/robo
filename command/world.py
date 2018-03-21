import io
import svgwrite
import svgwrite.shapes
import svgwrite.container
import math
import random
import time

import configuration
import cv2
import numpy as np
from PIL import Image, ImageDraw
import cairosvg

class world:
    startingX=-13.5/2
    startingY=7.5
    startinDir=0.0

    goalX=50.0
    goalY=50.0
    goalDir=math.pi/2

    taperect=[]

    positions=None

    def addVerticalTape(self, x, y1, y2):
        self.taperect.append([x, y1, x+3.8, y2])

    def addHorizontalTape(self, y, x1, x2):
        self.taperect.append([x1, y, x2, y+3.8])

    def __init__(self):
        self.addVerticalTape(0.0, 0.0, 14.0)
        self.addHorizontalTape(0.0, 0.0, 101.6)
        self.addVerticalTape(101.6-3.8, 0.0, 74.4)
        self.addHorizontalTape(74.4-3.8, 101.6-3.8-6.1, 101.6-3.8-6.1+16.5)

        self.addHorizontalTape(27.4, 30.0, 30.0+17.0)
        self.addHorizontalTape(51.0-3.8, 30.0, 30.0+17.0)
        self.addVerticalTape(30.0, 27.4, 51.0)
        self.addVerticalTape(30.0+17.0-3.8, 27.4, 51.0)


    def getRotation(self, thetaz):
        return np.array([
             [math.cos(thetaz), -math.sin(thetaz), 0.0, 0.0],
             [math.sin(thetaz), math.cos(thetaz), 0.0, 0.0],
             [0.0, 0.0, 1.0, 0.0],
             [0.0, 0.0, 0.0, 1.0]
        ])

    def getTranslation(self, x, y):
        return np.array([
            [1.0, 0.0, 0.0, x],
            [0.0, 1.0, 0.0, y],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

    def getwTr(self, position):
        return np.array([
            [math.cos(position[2]), -math.sin(position[2]), 0.0, position[0]],
            [math.sin(position[2]), math.cos(position[2]), 0.0, position[1]],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

    def getrTw(self, position):
            return np.linalg.inv(self.getwTr(position))

    def getSVG(self, height=400, width=800):
        boundMinX, boundMinY, boundMaxX, boundMaxY=self.getBoundingBox()
        dwg = svgwrite.Drawing('test.svg', profile='tiny')
        dwg.add(svgwrite.shapes.Rect((0.0,0.0),(float(width), float(height))).stroke(color="#101010"))
        group=svgwrite.container.Group()
        scaleFactor=min(height/(boundMaxY-boundMinY), width/(boundMaxX-boundMinX))
        group.translate(-boundMinX*scaleFactor, boundMinY*scaleFactor+height)
        group.scale(scaleFactor, -scaleFactor)
        for b in self.taperect:
            group.add(svgwrite.shapes.Rect((b[0], b[1]), ((b[2]-b[0]), (b[3]-b[1]))).stroke(color="#FFFFFF").fill(color="#FFFFFF"))

        if self.positions:
            prevX=self.startingX
            prevY=self.startingY
            for point in self.positions:
                group.add(svgwrite.shapes.Line((prevX, prevY), (point[0], point[1])).stroke(color="#FF0000"))
                prevX=point[0]
                prevY=point[1]
        dwg.add(group)
        return dwg

    def W2C(self, p, position):
        return configuration.cTr.dot(self.getrTw(position)).dot(p)

    def floorBoxToWorldCoordinates(self, b, position):
        wc=[]
        wc.append(self.W2C(np.array([b[0], b[1], 0.0, 1.0]), position).tolist()[0:3])
        wc.append(self.W2C(np.array([b[2], b[1], 0.0, 1.0]), position).tolist()[0:3])
        wc.append(self.W2C(np.array([b[2], b[3], 0.0, 1.0]), position).tolist()[0:3])
        wc.append(self.W2C(np.array([b[0], b[3], 0.0, 1.0]), position).tolist()[0:3])
        return wc

    def getProjectedSVG(self, pos, height=240, width=320):
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.add(svgwrite.shapes.Rect((0.0,0.0),(float(width), float(height))).fill(color="#7f757a"))
        tvec=np.array([0,0,0], dtype=float)
        rvec=np.array([0,0,0], dtype=float)

        for b in self.taperect:

            projected=cv2.projectPoints(np.array(self.floorBoxToWorldCoordinates(b,pos)), rvec, tvec,
                                        configuration.camera_matrix, configuration.dist_coefs)[0]
            points=[]
            i=0
            for x in projected:
                #print(i,([x[0][0], x[0][1]]))
                points.append([x[0][0], x[0][1]])
            dwg.add(svgwrite.shapes.Polygon(points).stroke(color="#bec5bf").fill(color="#bec5bf"))
        return dwg

    def drawOnImage(self, img, pos):
        tvec=np.array([0,0,0], dtype=float)
        rvec=np.array([0,0,0], dtype=float)
        draw = ImageDraw.Draw(img)
        for b in self.taperect:
            projected=cv2.projectPoints(np.array(self.floorBoxToWorldCoordinates(b,pos)), rvec, tvec,
                                        configuration.camera_matrix, configuration.dist_coefs)[0]
            for i in range(len(projected)):
                #print(i, (projected[i][0][0], projected[i][0][1],
                #          projected[(i+1)%len(projected)][0][0], projected[(i+1)%len(projected)][0][1]))
                draw.line((projected[i][0][0], projected[i][0][1],
                           projected[(i+1)%len(projected)][0][0], projected[(i+1)%len(projected)][0][1]), fill=128)
        del draw
        return img

    def getBoundingBox(self):
        minX= float("inf")
        maxX= - float("inf")
        minY = float("inf")
        maxY = - float("inf")
        for b in self.taperect:
            x= min(b[0], b[2])
            if x < minX:
                minX=x
            x= max(b[0], b[2])
            if x > maxX:
                maxX=x
            y = min(b[1], b[3])
            if y < minY:
                minY=y
            y = max(b[1], b[3])
            if y> maxY:
                maxY=y

        for x,y in [[self.startingX, self.startingY], [self.goalX, self.goalY]]:
            if x - 10 < minX:
                minX=x-10
            if x + 10 > maxX:
                maxX=x+10
            if y - 10 < minY:
                minY=y-10
            if y + 10 > maxY:
                maxY=y+10

        return [minX, minY, maxY, maxY]

    def imageDiff(self, im1, im2):
        imdiff=np.array(im1, dtype=float)-np.array(im2, dtype=float)
        return sum(sum(sum(abs(imdiff))))

if __name__=="__main__":
    w=world()
    #w.getProjectedSVG([-41.68129685, 3.91507777, 0.0]).saveas("perspective.svg", True)
    #w.getProjectedSVG([-41.68129685, 3.91507777, 0.2]).saveas("perspective1.svg", True)
    #w.getProjectedSVG([-41.68129685, 3.91507777, 0.4]).saveas("perspective2.svg", True)
   # w.getProjectedSVG([-41.68129685, 3.91507777, 0.6]).saveas("perspective3.svg", True)

    #w.getProjectedSVG([-40.0,7.5, 0.0]).saveas("perspective.svg", True)
    # w.getProjectedSVG([-40.0,7.5, 0.2]).saveas("perspective1.svg", True)
    # w.getProjectedSVG([-40.0,7.5, 0.4]).saveas("perspective2.svg", True)
    # w.getProjectedSVG([-40.0,7.5, 0.6]).saveas("perspective3.svg", True)
    # w.getProjectedSVG([-40.0,7.5, 0.8]).saveas("perspective4.svg", True)
    #w.getProjectedSVG([0.0,0.0, 0.2]).saveas("perspective1.svg", True)
    #w.getProjectedSVG([0.0,0.0, 0.4]).saveas("perspective2.svg", True)
    #w.getProjectedSVG([0.0,0.0, 0.6]).saveas("perspective3.svg", True)


    im=w.drawOnImage(Image.open("../jupyter/currentimage_40_75.jpg"),[-40.02813321721587, 8.96339210197052, -0.030133771199697536])
    im.save("drawedOn.png")

    trueImage=Image.open("../jupyter/currentimage_40_75.jpg")
    lowestDiff=float("inf")
    bestPosition=None
    startTime=time.time()
    for i in range(1000):
        position=[-40.0+(random.random()-0.5)*15,7.5+(random.random()-0.5)*15, 0.0+(random.random()-0.5)*0.8]
        s=w.getProjectedSVG(position)
        #print("svg: ",(time.time()-startTime))
        #startTime=time.time()
        image=Image.open(io.BytesIO(cairosvg.svg2png(s.tostring())))
        #print("image: ",(time.time()-startTime))
        #startTime=time.time()
        diff=w.imageDiff(image, trueImage)
        #print("diff: ",(time.time()-startTime))
        #startTime=time.time()
        if lowestDiff > diff:
            lowestDiff=diff
            bestPosition=position
    print(time.time() - startTime)
    print(bestPosition)

