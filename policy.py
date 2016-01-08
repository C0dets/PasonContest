import credentials
import mathHelper
import numpy as np

from interpreter import Interpreter

class Policy:
    def __init__(self, comm):
        self.comm = comm
        self.intp = Interpreter()

    def newStatus(self, status):
        if (not self.processStatus(status)):
            return
        self.intp.statusUpdate(status)

        self.doAttacks()

    ##    Check if any tank is in danger, move away  (Do predictive calculations by observing past status and extrapolating?)
        self.evade()

        self.offensivePositioning()

        self.testStarted = False
        print self.myTanks[0]['id'], self.myTanks[0]['tracks']
        if not self.testStarted:
            self.testStarted = True
            self.comm.rotateTurret(self.myTanks[0]['id'], 300)
            self.comm.rotateTank(self.myTanks[0]['id'], 300)


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
            else:
                self.enemyTanks += player['tanks']

        return True

    def gameRefresh(self):
        self.intp.refresh()

    def doAttacks(self):
        ## Check if any tank should attack
        for myTank in self.myTanks:
            targetId = self.intp.whoWouldIShoot(myTank)
            if (targetId and targetId not in self.myTankIds):
                self.comm.fire(myTank['id'])

    '''
    Makes neccessary evasion movements
    if evading the "predictedLocation" for the next update is appended to the tank
    '''
    def evade(self):
        threatGrid = np.zeros(7)
        
        for myTank in self.myTanks:
            for i in range(7):
                for projectile in self.intp.projectiles:
                    angle = 2*np.pi/i
                    if i == 0:
                        newPosition = myTank['position']
                    else:
                        newPosition = getLineEndpoint(myTank['position'], hitRadius, angle)
                    A = projectile['position']
                    B = mathHelper.getLineEndpoint(A, projectile['range'], projectile['direction'])
                    if mathHelper.circleOnLine(A, B, newPosition, myTank['hitRadius'])
                        threatGrid[i] = max(1/projectile['range'], threatGrid[i])
            
            i = np.min(threatGrid)
        
            ##if i != 0:
            ##    angle = 2*np.pi/i
            ##    rotationDirection = myTank['tracks']-angle
            ##    if rotationDirection > 0:
                    

    '''
    Should only move tanks not already moved
    '''
    def offensivePositioning(self):
        for myTank in self.myTanks:
            myTank['threats'] = self.intp.getThreatsToA(myTank, self.enemyTanks)

        return

