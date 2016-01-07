import math
import mathHelper

hitRad = 2
colRad = 2
projRange = 100

class Interpreter:
    def __init__(self):
        self.lastTimeStamp = False
        self.period = 1
        self.avgPeriod = 1
        self.statusUpdates = 0
        return

    def statusUpdate(status):
        self.periodCalculator(status["timestamp"])
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
        distance = mathHelper.distanceBetween(tank1['position'], tank2['position'])
        if (distance > projRange + hitRad):
            return False

        ## Check that we are pointing at it
        angle = mathHelper.angleFromAToB(tank1['position'], tank2['position'])
        offset = math.asin(hitRad/distance)
        if (not mathHelper.angleInRange(tank1['turret'], angle + offset, angle - offset)):
            return False

        ## Check that no other tanks are in the way
##        for tank in self.tanks:
##            if (self.inPath(angle, distance, tank['position'], )):
##                return False


        ## Check for obstacles

        return True

    def periodCalculator(timeStamp):
        ## Up our status updates
        if (self.statusUpdates < 10):
            self.statusUpdates += 1

        ## Calc current period
        if (self.lastTimeStamp != False):
            self.period = timeStamp - self.lastTimeStamp

        ## Calc avg period
        if (self.statusUpdates > 1):
            self.avgPeriod = (self.avgPeriod * (self.statusUpdates - 1) + self.period) / self.statusUpdates

        ## Move timestamp
        self.lastTimeStamp = timeStamp





