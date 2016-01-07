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




