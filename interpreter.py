import math
import mathHelper

PROJECTILE_RANGE = 100

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

    '''
    Returns an object:
        {
            tankA: tankA,
            tankB: tankB,
            angle: 1.2, #the angle in rads from A to B
            distance: 50.1 #the distance from A to B
        }

    '''
    def correlationAtoB(self, tankA, tankB):
        result = {
            'tankA': tankA,
            'tankB': tankB
            }
        result['distance'] = mathHelper.distanceBetween(tankA['position'], tankB['position'])
        result['angle'] = mathHelper.angleFromAToB(tankA['position'], tankB['position'])

        return result

    '''
    Checks if A is threatened by any enemyTanks
    Returns an array of the threatening tanks, most threatening first
    '''
    def getThreatsToA(self, tankA, enemyTanks):
        threats = []
        for enTank in enemyTanks:
            ## Check if in dangerous range
            dangerousRange = PROJECTILE_RANGE + self.avgPeriod * enTank['speed'] * 1.1
            distance = mathHelper.distanceBetween(tankA['position'], enTank['position'])
            if (distance < dangerousRange):
                ## Check if obstacles in the way
                if not self.isSolidOnLine(tankA['position'], enTank['position']):
                    threats.append({'tank': enTank, 'distance': distance})
        return sorted(threats, key=lambda threat:threat['distance'])

    def canAshootB(self, tank1Id, tank2Id):
        tank1 = self.tanks[tank1Id]
        tank2 = self.tanks[tank2Id]

        ## Check if in range
        distance = mathHelper.distanceBetween(tank1['position'], tank2['position'])
        if (distance > PROJECTILE_RANGE + tank2['hitRadius']):
            return False

        ## Check that we are pointing at it
        angle = mathHelper.angleFromAToB(tank1['position'], tank2['position'])
        offset = math.asin(tank2['hitRadius']/distance)
        if (not mathHelper.angleInRange(tank1['turret'], angle + offset, angle - offset)):
            return False

        ## get the end point for tank1's range
        endPoint = mathHelper.getLineEndpoint(tank1['position'], distance, tank1['turret'])

# Don't want to check if other tanks are blocking because they could move
##        ## Check that no other tanks are in the way
##        for tank in self.tanks:
##            ## Don't consider the original 2 tanks
##            if (tank['id'] == tank1Id or tank['id'] == tank2Id):
##                continue
##            if (mathHelper.circleOnLine(tank1['position'], endPoint, tank['position'], tank['hitRadius'])):
##                return False

        ## Ensure path is clear of solids
        if self.isShotClear(tank1['position'], endPoint):
            return True

        return False

    def whoWouldIShoot(self, tank1):
        target = False
        targetDistance = PROJECTILE_RANGE * 2 ## Just put it at a ridiculous range to start
        ## get the end point for tank1's range
        endPoint = mathHelper.getLineEndpoint(tank1['position'], PROJECTILE_RANGE, tank1['turret'])

        for tankId in self.tanks:
            tank = self.tanks[tankId]
            ## Don't consider self
            if (tank['id'] == tank1['id']):
                continue
            distanceToIntersection = mathHelper.circleOnLine(tank1['position'], endPoint, tank['position'], tank['hitRadius'])
            if (distanceToIntersection != False and distanceToIntersection < targetDistance):
                targetDistance = distanceToIntersection
                target = tank

        ## Ensure path is clear of solids
        if self.isShotClear(tank1['position'], endPoint):
            return target
        else:
            return False

    def isShotClear(self, startPoint, endPoint):
        for terrain in self.mapTerrain:
            if terrain['type'] == 'SOLID':
                if mathHelper.rectOnLine(terrain['boundingBox']['corner'], terrain['boundingBox']['size'], startPoint, endPoint):
                    return False
        return True

    def statusUpdate(self, status):
        self.periodCalculator(status["timestamp"])
        self.mapSize = status['map']['size']
        self.mapTerrain = status['map']['terrain']
        self.tanks = {}
        self.projectiles = []
        for player in status['players']:
            for tank in player['tanks']:
                self.tanks[tank['id']] = tank
                for projectile in tank['projectiles']:
                    self.projectiles.append(projectile)


    def periodCalculator(self, timeStamp):
        ## Up our status updates
        if (self.statusUpdates < 10):
            self.statusUpdates += 1

        ## Calc current period
        if (self.lastTimeStamp != False):
            self.period = (timeStamp - self.lastTimeStamp) / 1000

        ## Calc avg period
        if (self.statusUpdates >= 1):
            self.avgPeriod = (self.avgPeriod * (self.statusUpdates - 1) + self.period) / self.statusUpdates

        ## Move timestamp
        self.lastTimeStamp = timeStamp

    def projectilesPaths(self):
        threats = []
        for projectile in self.projectiles:
            A = projectile['position']
            B = mathHelper.getLineEndpoint(A, projectile['range'], projectile['direction'])
            threats.append([A,B])

        return threats

    def obstacleInWay(self, position, size):
        for terrain in self.mapTerrain:
            if mathHelper.circleOnRect(terrain['boundingBox']['corner'], terrain['boundingBox']['size'], position, size):
                return True
        return False

