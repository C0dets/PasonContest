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
                angle = 2*np.pi/i
                if i == 0:
                    newPosition = myTank['position']
                else:
                    newPosition = getLineEndpoint(myTank['position'], myTank['hitRadius'], angle)
                for projectile in self.intp.projectiles:
                    A = projectile['position']
                    B = mathHelper.getLineEndpoint(A, projectile['range'], projectile['direction'])
                    if mathHelper.circleOnLine(A, B, newPosition, myTank['hitRadius']):
                        threatGrid[i] = max(1/projectile['range'], threatGrid[i])
            
                if self.intp.obstacleInWay(newPosition, myTank['collisionRadius']):
                    threatGrid[i] = max(10, threatGrid[i])

            i = np.min(threatGrid)
        
            if i != 0:
                reqAngle = 2*np.pi/i
                myAngle = myTank['tracks']
                diff = myAngle-reqAngle
                rotationReq = np.arctan(np.sin(diff)/ np.cos(diff))

                self.comm.rotateTank(myTank['id'], rotationReq)

                myNewAngle = myAngle+rotationReq            

                if myNewAngle < 0:
                    myNewAngle += 2*np.pi
                if myNewAngle > 2*np.pi:
                    myNewAngle -= 2*np.pi

                if myNewAngle != reqAngle:
                    direction = "FWD"
                else:
                    direction = "REV"

                self.comm.move(myTank['id'], direction, 10)

                predictedDist = self.inp.avgPeriod * myTank['speed']
    
                myTank['predictedPosition'] = mathHelper.getLineEndpoint(myTank['position'], predictedDist, myNewAngle)



    '''
    Should only move tanks not already moved
    '''
    def offensivePositioning(self):
        correlationArr = []
        for myTank in self.myTanks:
            for enTank in self.enemyTanks:
                tempCor = self.intp.correlationAtoB(myTank, enTank)
                tempCor['turrentChange'] = mathHelper.smallestAngleBetween(myTank['turret'], tempCor['angle'])
                correlationArr.append(tempCor)
        # Sort the array, smallest abs angle chang first
        sorted(correlationArr, key=lambda entry:np.absolute(entry['turrentChange']))


        return

