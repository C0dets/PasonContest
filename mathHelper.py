import math

def distanceBetween(point1, point2):
    xDist = point2[0] - point1[0]
    yDist = point2[1] - point1[1]
    return math.sqrt((xDist * xDist) + (yDist * yDist))

## Point1 is the from point, point2 is the to point
## returns 0 to 2pi
def angleFromAToB(point1, point2):
    xDist = point2[0] - point1[0]
    yDist = point2[1] - point1[1]

    if (xDist == 0):
        if (yDist >= 0):
            return math.pi/2
        else:
            return math.pi * 1.5

    angle = math.atan(yDist/xDist)
    ## Both left quads
    if (xDist < 0):
        return angle + math.pi
    ## the bottom right quad
    if (xDist > 0 and yDist < 0):
        return angle + (2 * math.pi)
    ## the top right quad
    return angle

def angleInRange(act, upper, lower):
    altUpper = 0
    altLower = 1
    if (upper > 2 * math.pi):
        altUpper = upper - 2 * math.pi
        altLower = lower - 2 * math.pi
    elif (lower < 0):
        altUpper = upper + 2 * math.pi
        altLower = lower + 2 * math.pi

    if ((act < upper and act > lower) or (act < altUpper and act > altLower)):
        return True
    return False

def circleOnLine(lineStart, lineEnd, circleCentre, circleRadius):
    Ax = lineStart[0]
    Ay = lineStart[1]
    Bx = lineEnd[0]
    By = lineEnd[1]
    Cx = circleCentre[0]
    Cy = circleCentre[1]

    distAB = distanceBetween(lineStart, lineEnd) 

    ## find direction vector D from A to B
    Dx = (Bx-Ax)/distAB
    Dy = (By-Ay)/distAB

    ## line equation is x = Dx*t + Ax, y = Dy*t + Ay with 0 <= t <= 1
    ## find t for closest point to circle centre
    t = Dx*(Cx-Ax) + Dy*(Cy-Ay)    

    ## find point on line closes to circle
    Ex = t*Dx+Ax
    Ey = t*Dy+Ay

    distEC = distanceBetween([Cx,Cy], [Ex,Ey])
    
    if (distEC <= circleRadius):
        dt = math.sqrt(circleRadius*circleRadius - distEC*distEC)

        # find first intersection point
        Fx = (t-dt)*Dx + Ax
        Fy = (t-dt)*Dy + Ay

        # find first intersection point
        Gx = (t+dt)*Dx + Ax
        Gy = (t+dt)*Dy + Ay

        return  min(distanceBetween(lineStart, [Fx,Fy]), distanceBetween(lineStart, [Gx,Gy]))

    else:
        return False

def getLineEndpoint(lineStart, lineLength, lineAngle):
        x = lineLength * math.cos(lineAngle)
        y = lineLength * math.sin(lineAngle)
        
        return [lineStart[0]+x,lineStart[1]+y]
        



