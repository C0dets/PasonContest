import math
import numpy as np

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

'''
Finds the smallest angle between two angles
'''
def smallestAngleBetween(angA, angB):
    dif = angB - angA
    altDif = np.pi ## angle between in other direction
    if dif > 0:
        altDif = -2 * np.pi + dif
    else:
        altDif = 2 * np.pi + dif

    if np.absolute(dif) < np.absolute(altDif):
        return dif
    else:
        return altDif

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

def rectOnLine(lineStart, lineEnd, rectStartPoint, rectDimensions):

    Ax = lineStart[0]
    Ay = lineStart[1]
    Bx = lineEnd[0]
    By = lineEnd[1]

    rectTop = rectStartPoint[1]+rectDimensions[1]
    rectBottom = rectStartPoint[1]
    rectRight = rectStartPoint[0]+rectDimensions[0]
    rectLeft = rectStartPoint[0]

    if np.max(Ax, Bx) < rectLeft or np.min(Ax, Bx) > rectRight:
        return False
    if np.max(Ay, By) < rectBottom or np.min(Ay, By) > rectTop:
        return False

    if (Bx == Ax):
        return True
    else:
        m = (By - Ay) / (Bx - Ax)
        b = By - m*Bx

        yAtRectLeft = m*rectLeft + b
        yAtRectRight = m*rectRight + b

    if (rectBottom > yAtRectRight and rectBottom > yAtRectLeft):
        return False
    if (rectTop > yAtRectRight and rectTop > yAtRectLeft):
        return False

    return True

def circleOnRect(corner, size, centre, radius):
    if circleOnLine(corner, [corner[0]+size[0], corner[1]], centre, radius):
        return True
    if circleOnLine(corner, [corner[0], corner[1]+size[1]], centre, radius):
        return True
    if circleOnLine([corner[0], corner[1]+size[1]], [corner[0]+size[0], corner[1]+size[1]], centre, radius):
        return True
    if circleOnLine([corner[0]+size[0], corner[1]], [corner[0]+size[0], corner[1]+size[1]], centre, radius):
        return True
    return False

