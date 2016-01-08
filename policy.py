import credentials

from interpreter import Interpreter

class Policy:
    def __init__(self, comm):
        self.comm = comm
        self.intp = Interpreter()

    def newStatus(status, comm):
        if (not self.processStatus):
            return
        self.intp.statusUpdate(status)

        self.doAttacks()

    ##    Check if any tank is in danger, move away  (Do predictive calculations by observing past status and extrapolating?)
        self.evade()

    ##    For each opponenet tank, find own tank that is closest, and assign opponent to own tank and move+rotate agressively
        self.offensivePositioning()

    def processStatus(status):
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

    def refresh(self):
        self.intp.refresh()

    def doAttacks(self):
        ## Check if any tank should attack
        for myTank in self.myTanks:
            targetId = self.intp.whoWouldIShoot(myTank)
            if (targetId and targetId not in self.myTankIds):
                self.comm.fire(myTank['id'])

    ## Makes neccessary evasion movements
    ## if evading the "predictedLocation" for the next update is appended to the tank
    def evade(self):
        return

    def offensivePositioning():
        ## Should only move tanks not already moved
        return

