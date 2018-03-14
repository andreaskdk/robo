import svgwrite
import svgwrite.shapes
import svgwrite.container
import math

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

    import planning
    path=[1 for _ in range(20)]+[2 for _ in range(43)]+[1 for _ in range(3)]
    w.positions=planning.getPositions(path,w.startingX, w.startingY, w.startinDir)

    w.getSVG().saveas("test.svg", True)

