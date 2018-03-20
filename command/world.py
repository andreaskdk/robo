import svgwrite
import svgwrite.shapes
import svgwrite.container
import math
import configuration
import cv2
import numpy as np


class world:
    startingX=-13.5/2
    startingY=7.5
    startinDir=0.0

    goalX=50.0
    goalY=50.0
    goalDir=math.pi/2

    rTc=np.array([[1.0, 0.0, 0.0, 2.0],
                  [0.0, 1.0, 0.0, -1.0],
                  [0.0, 0.0, 1.0, 18.0],
                  [0.0, 0.0, 0.0, 1.0]
                  ])

    cTr=np.linalg.inv(rTc)

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

    def rotationMatrixToEulerAngles(self, R) :
        sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
        singular = sy < 1e-6
        if  not singular :
            x = math.atan2(R[2,1] , R[2,2])
            y = math.atan2(-R[2,0], sy)
            z = math.atan2(R[1,0], R[0,0])
        else :
            x = math.atan2(-R[1,2], R[1,1])
            y = math.atan2(-R[2,0], sy)
            z = 0
        return np.array([x, y, z])

    def yawpitchrolldecomposition(self, R):
        sin_x    = math.sqrt(R[2,0] * R[2,0] +  R[2,1] * R[2,1])
        validity  = sin_x < 1e-6
        if not validity:
            z1    = math.atan2(R[2,0], R[2,1])     # around z1-axis
            x      = math.atan2(sin_x,  R[2,2])     # around x-axis
            z2    = math.atan2(R[0,2], -R[1,2])    # around z2-axis
        else: # gimbal lock
            z1    = 0                                         # around z1-axis
            x      = math.atan2(sin_x,  R[2,2])     # around x-axis
            z2    = 0                                         # around z2-axis

        return np.array([[z1], [x], [z2]])

    def eulerAnglesToRotationMatrix(self, theta) :
        R_x = np.array([[1,         0,                  0                   ],
                        [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                        [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                        ])
        R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                        [0,                     1,      0                   ],
                        [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                        ])
        R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                        [math.sin(theta[2]),    math.cos(theta[2]),     0],
                        [0,                     0,                      1]
                        ])
        R = np.dot(R_z, np.dot( R_y, R_x ))
        return R


    def getCameraVectors(self, position):
        camera_position=[position[0], position[1], -18.0]
        rvec0=[ 1.32483378, -1.34834392, 1.08352354]
        euler=self.rotationMatrixToEulerAngles( cv2.Rodrigues(np.array(rvec0))[0] )
        euler[2]+=position[2]
        #euler[0]-=position[2]
        rotation = self.eulerAnglesToRotationMatrix(euler)
        rvec=cv2.Rodrigues(rotation)[0]
        tvec=-rotation.dot(camera_position)
        return tvec, rvec

    def floorBoxToWorldCoordinates(self, b):
        wc=[]
        wc.append([b[0], b[1], 0.0])
        wc.append([b[2], b[1], 0.0])
        wc.append([b[2], b[3], 0.0])
        wc.append([b[0], b[3], 0.0])
        return wc

    def getProjectedSVG(self, pos, height=240, width=320):
        dwg = svgwrite.Drawing('test.svg', profile='tiny')
        dwg.add(svgwrite.shapes.Rect((0.0,0.0),(float(width*10), float(height*10))).stroke(color="#101010"))
        tvec, rvec=self.getCameraVectors(pos)
        for b in self.taperect:
            projected=cv2.projectPoints(np.array(self.floorBoxToWorldCoordinates(b)), rvec, tvec, configuration.camera_matrix, configuration.dist_coefs)[0]
            points=[]
            for x in projected:
                points.append([x[0][0], x[0][1]])
            dwg.add(svgwrite.shapes.Polygon(points).stroke(color="#00FF00"))
        return dwg

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

if __name__=="__main__":
    w=world()
    #w.getProjectedSVG([-41.68129685, 3.91507777, 0.0]).saveas("perspective.svg", True)
    #w.getProjectedSVG([-41.68129685, 3.91507777, 0.2]).saveas("perspective1.svg", True)
    #w.getProjectedSVG([-41.68129685, 3.91507777, 0.4]).saveas("perspective2.svg", True)
   # w.getProjectedSVG([-41.68129685, 3.91507777, 0.6]).saveas("perspective3.svg", True)

    w.getProjectedSVG([0.0,0.0, 0.0]).saveas("perspective.svg", True)
    w.getProjectedSVG([0.0,0.0, 0.2]).saveas("perspective1.svg", True)
    w.getProjectedSVG([0.0,0.0, 0.4]).saveas("perspective2.svg", True)
    w.getProjectedSVG([0.0,0.0, 0.6]).saveas("perspective3.svg", True)


