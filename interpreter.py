import math
import mathHelper

projRange = 100

class Interpreter:
    def __init__(self):
        self.lastTimeStamp = False
        self.period = 0.10002
        self.avgPeriod = 0.10002
        self.statusUpdates = 0
        return

    ## Should wipe memory of previous game
    def refresh(self):
        return

    def canAshootB(self, tank1Id, tank2Id):
        tank1 = self.tanks[tank1Id]
        tank2 = self.tanks[tank2Id]

        ## Check if in range
        distance = mathHelper.distanceBetween(tank1['position'], tank2['position'])
        if (distance > projRange + tank2['hitRadius']):
            return False

        ## Check that we are pointing at it
        angle = mathHelper.angleFromAToB(tank1['position'], tank2['position'])
        offset = math.asin(tank2['hitRadius']/distance)
        if (not mathHelper.angleInRange(tank1['turret'], angle + offset, angle - offset)):
            return False

        ## Check that no other tanks are in the way
        for tank in self.tanks:
            ## Don't consider the original 2 tanks
            if (tank['id'] == tank1Id or tank['id'] == tank2Id):
                continue
            ## get the end point for tank1's range
            endPoint = [
                tank1['position'][0] + distance * math.sin(tank1['turret']),
                tank1['position'][1] + distance * math.cos(tank1['turret'])
            ]
            if (mathHelper.circleOnLine(tank1['position'], endPoint, tank['position'], tank['hitRadius'])):
                return False

        ## Check for obstacles

        return True

    def whoWouldIShoot(self, tank1):
        targetId = False
        targetDistance = projRange * 2 ##Just put it a ridiculous range to start
        for tankId in self.tanks:
            tank = self.tanks[tankId]
            ## Don't consider self
            if (tank['id'] == tank1['id']):
                continue
            ## get the end point for tank1's range
            endPoint = [
                tank1['position'][0] + projRange * math.sin(tank1['turret']),
                tank1['position'][1] + projRange * math.cos(tank1['turret'])
            ]
            distanceToIntersection = mathHelper.circleOnLine(tank1['position'], endPoint, tank['position'], tank['hitRadius'])
            if (distanceToIntersection != False and distanceToIntersection < targetDistance):
                targetDistance = distanceToIntersection
                targetId = tank['id']
        return targetId

    def statusUpdate(self, status):
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


    def periodCalculator(self, timeStamp):
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





