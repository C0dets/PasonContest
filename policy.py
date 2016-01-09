from __future__ import division
import credentials
import mathHelper
import numpy as np
import copy

from interpreter import Interpreter

PROJECTILE_DAMAGE = 100
PROJECTILE_RANGE = 100
PROJECTILE_SPEED = 30
ROTATION_SPEED = 1.5

class Policy:
    def __init__(self, comm, predictionFactor):
        self.comm = comm
        self.predictionFactor = predictionFactor
        self.intp = Interpreter()
        self.tankPlans = {}

    def newStatus(self, status):
        if (not self.processStatus(status)):
            return
        self.intp.statusUpdate(status)

        self.doAttacks()

    ##    Check if any tank is in danger, move away  (Do predictive calculations by observing past status and extrapolating?)
        self.evade()

        self.offensivePositioning()


    def processStatus(self, status):
        if ("map" not in status):
            print 'missing map'
            print status
            return False
        if ("players" not in status):
            print 'missing players'
            print status
            return False

        self.myTanks = []
        self.myTankIds = []
        self.enemyTanks = []

        for player in status['players']:
            if (player['name'] == credentials.username):
                self.myTanks = player['tanks']
                for tank in self.myTanks:
                    self.myTankIds.append(tank['id'])
                    if tank['id'] not in self.tankPlans:
                        self.tankPlans[tank['id']] = {
                                'lasti': 0,
                                'lastDirection': 0,
                                'lastAngle': 0,
                                'lastThreat': 0
                            }
            else:
                self.enemyTanks += player['tanks']

        return True

    def gameRefresh(self):
        self.tankPlans = {}

        self.intp.refresh()

    def doAttacks(self):
        ## Check if any tank should attack
        for myTank in self.myTanks:
            target = self.intp.whoWouldIShoot(myTank)
            # Check that we would be firing at enemy
            if target:
                if target['id'] not in self.myTankIds:
                    self.comm.fire(myTank['id'])
                else:
                    self.comm.stop(myTank['id'], 'FIRE')

    '''
    Makes neccessary evasion movements
    if evading the "predictedPosition" for the next update is appended to the tank
    '''
    def evade(self):
        for myTank in self.myTanks:
            threatGrid = np.zeros(7)
            for i in range(7):
                if i == 0:
                    newPosition = myTank['position']
                else:
                    angle = 2*np.pi*i/6
                    newPosition = mathHelper.getLineEndpoint(myTank['position'], 2*myTank['hitRadius'], angle)
                # TODO: Dodge enemy turrets
                enemyThreats = self.intp.getThreatsToA(myTank, self.enemyTanks)
                for enemyTank in enemyThreats:
                    if self.intp.canAshootB(enemyTank['tank']['id'], myTank['id']):
                        strikeDist = mathHelper.distanceBetween(myTank['position'], enemyTank['tank']['position'])
                        strikeDist -= self.intp.avgPeriod * enemyTank['tank']['speed']
                        threatGrid[i] = max(1/strikeDist, threatGrid[i])
                for projectile in self.intp.projectiles:
                    A = projectile['position']
                    B = mathHelper.getLineEndpoint(A, projectile['range'], projectile['direction'])
                    strikeDist = mathHelper.circleOnLine(A, B, newPosition, myTank['hitRadius'])
                    if strikeDist != False:
                        threatGrid[i] = max(1/strikeDist, threatGrid[i])
                if self.intp.obstacleInWay(newPosition, myTank['collisionRadius']):
                    threatGrid[i] = max(10, threatGrid[i])

            i = np.argmin(threatGrid)

            #if self.tankPlans[myTank['id']]['lastThreat'] <= threatGrid[i]:
            #    i = self.tankPlans[myTank['id']]['lasti']

            #direction = 0
            #myNewAngle = 0

            #if i == self.tankPlans[myTank['id']]['lasti'] and i!= 0:
            #    direction = self.tankPlans[myTank['id']]['lastDirection']
            #    self.comm.move(myTank['id'], direction, 2*myTank['hitRadius'])

            #    predictedDist = self.intp.avgPeriod * myTank['speed']

            #    myTank['predictedPosition'] = mathHelper.getLineEndpoint(myTank['position'], predictedDist, self.tankPlans[myTank['id']]['lastAngle'])

            if i != 0:
                reqAngle = 2*np.pi*i/6
                myAngle = myTank['tracks']
                diff = myAngle - reqAngle
                rotationReq = np.arctan(np.sin(diff)/ np.cos(diff))

                self.comm.rotateTank(myTank['id'], rotationReq)

                myNewAngle = myAngle+rotationReq

                if myNewAngle < 0:
                    myNewAngle += 2*np.pi
                if myNewAngle > 2*np.pi:
                    myNewAngle -= 2*np.pi

                if myNewAngle != reqAngle:
                    direction = "REV"
                else:
                    direction = "FWD"

                self.comm.move(myTank['id'], direction, 2*myTank['hitRadius'])

                predictedDist = self.intp.avgPeriod * myTank['speed']

                myTank['predictedPosition'] = mathHelper.getLineEndpoint(myTank['position'], predictedDist, myNewAngle)

            else:
                myTank['predictedPosition'] = myTank['position']

            #self.tankPlans[myTank['id']]['lastDirection'] = direction
            #self.tankPlans[myTank['id']]['lasti'] = i
            #self.tankPlans[myTank['id']]['lastAngle'] = myNewAngle
            #self.tankPlans[myTank['id']]['lastThreat'] = threatGrid[i]



    '''
    Should only move tanks not with a "predictedPosition" (because evade has already dictated a movement)

    This tries to account for predictedPosition in it's turret placing.
    Basically if we end up using the predicted and not the actual the prediction
    will pretend the enemy is not moving, otherwise the prediction will assume we
    are stationary and that the enmeny will continue to move.  Essentially, either
    way the prediction will overshoot it's exact required rotation by one period's
    to hopefully account for some movement.
    '''
    def offensivePositioning(self):
        correlationArr = []
        myPredictedTanks = copy.deepcopy(self.myTanks)
        for myTank in myPredictedTanks:
            # Account for the predicted position
            myTank['actualPosition'] = myTank['position']
            if 'predictedPosition' in myTank:
                myTank['position'] = myTank['predictedPosition']
            for enTank in self.enemyTanks:
                tempCor = self.intp.correlationAtoB(myTank, enTank)
                if tempCor['distance'] > PROJECTILE_RANGE + self.intp.avgPeriod * enTank['speed'] * 3:
                    tempCor['shootable'] = False
                else:
                    tempCor['shootable'] = self.intp.isShotClear(myTank['position'], enTank['position'])
                tempCor['turretChange'] = mathHelper.smallestAngleBetween(myTank['turret'], tempCor['angle'])
                correlationArr.append(tempCor)
        # Sort the array, smallest abs angle chang first
        correlationArr = sorted(correlationArr, key=lambda entry:np.absolute(entry['turretChange']))

        remainingAttackers = copy.deepcopy(self.myTankIds)
        usedAttackers = {}
        enemyAttacked = {}
        for entry in correlationArr:
            # Check that the enemy is shootable
            if entry['shootable']:
                # Check if attacking tank is available
                if entry['tankA']['id'] not in usedAttackers:
                    # Check that enemy doesn't have too many attackers (max attackers = roundUp(remainingHeath/ProjDmg) + 1)
                    if entry['tankB']['id'] not in enemyAttacked or enemyAttacked[entry['tankB']['id']] <= np.ceil(entry['tankB']['health'] / PROJECTILE_DAMAGE) + 1:
                        # Check that attacker is actually close enough
                        if entry['distance'] < PROJECTILE_RANGE + self.intp.avgPeriod * entry['tankB']['speed']:
                            # assign the attaker to the enemy tank
                            remainingAttackers.remove(entry['tankA']['id'])
                            entry['targetId'] = entry['tankB']['id']
                            usedAttackers[entry['tankA']['id']] = entry
                            if entry['tankB']['id'] in enemyAttacked:
                                enemyAttacked[entry['tankB']['id']] += 1
                            else:
                                enemyAttacked[entry['tankB']['id']] = 0

        # assign any remaining attackers to enemies
        for attacker in remainingAttackers:
            # nobody to fire at so stop firinging
            self.comm.stop(myTank['id'], 'FIRE')
            # Find closest enemy via path finding and assign that enemy
            myCorrelations = [cor for cor in correlationArr if cor['tankA']['id'] == attacker]
            myCorrelations = sorted(myCorrelations, key=lambda entry:entry['distance'])
            for cor in myCorrelations:
                if cor['distance'] < PROJECTILE_RANGE + self.intp.avgPeriod * cor['tankB']['speed'] * 2:
                    cor['targetId'] = cor['tankB']['id']
                    usedAttackers[attacker] = entry

            # find closest shootable friend and move somewhat close to them  (like 30 away?)

        # Rotate turret appropriately
        for attacker in usedAttackers:
            # add predicitve factor to rotation
            angleToRotate = usedAttackers[attacker]['turretChange'] * self.predictionFactor
            self.comm.rotateTurret(attacker, angleToRotate)


        return
