import credentials

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

        testStarted = False
        print self.myTanks[0]['id'], self.myTanks[0]['turret']
        if not testStarted:
            self.comm.rotateTurret(self.myTanks[0]['id'], 30)
            self.comm.rotateTurret(self.myTanks[0]['id'], -30)


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
        return

    '''
    Should only move tanks not already moved
    '''
    def offensivePositioning(self):
        for myTank in self.myTanks:
            myTank['threats'] = self.intp.getThreatsToA(myTank, self.enemyTanks)

        return

