import math

hitRad = 2
colRad = 2
projRange = 100

class Interpreter:
    def __init__(self, status):
        self.mapSize = status['map']['size']
        self.mapTerrain = status['map']['terrain']
        self.tanks = {}
        self.projectiles = {}
        for player in status['players']:
            for tank in player['tanks']:
                self.tanks[tank['id']] = tank
                for projectile in tank['projectiles']:
                    self.tanks[tank['id']] = tank


    def inRange(self, tank1Id, tank2Id):
        tank1 = self.tanks[tank1Id]
        tank2 = self.tanks[tank2Id]

        ## Check if in range
        distance = distance(tank1['position'], tank2['position'])
        if (distance > projRange + hitRad):
            return False

        ## Check that we are pointing at it
        angle = angleTo(tank1['position'], tank2['position'])
        offset = math.asin(hitRad/distance)
        if (not angleInRange(tank1['turret'], angle + offset, angle - offset)):
            return False

        ## Check that were not firing at self

        ## Check for obstacles

        return True


def distance(point1, point2):
    xDist = point2[0] - point1[0]
    yDist = point2[1] - point1[1]
    return math.sqrt((xDist * xDist) + (yDist * yDist))

## Point1 is the from point, point2 is the to point
## returns 0 to 2pi
def angleTo(point1, point2):
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





