import math
import mathHelper

hitRad = 2
colRad = 2
projRange = 100

class Interpreter:
    def __init__(self):
        self.period = 1
        self.avgPeriod = 1
        self.statusUpdates = 0
        return

    def periodCalculator(timeStamp):
        return
        if (self.statusUpdates < 10 and self.statusUpdates):
            if (self.statusUpdates == 0):
                self.avgPeriod

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

        ## Check that were not firing at self

        ## Check for obstacles

        return True





