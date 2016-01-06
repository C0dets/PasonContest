class Interpreter:
    def __init__(self, status):
        self.mapSize = status['map']['size']
        self.mapTerrain = status['map']['terrain']
        self.tanks = {}
        for player in status['players']:
            for tank in player['tanks']:
                self.tanks[tank['id']] = tank
                if tank['projectiles'].length > 0:
                    print tank['type']
                    print tank['projectiles']


def inRange(tank1, tank2):
    print 'inRangeCall'

##    Check if any tank can be attacked

##    Check if any tank is in danger, move away  (Do predictive calculations by observing past status and extrapolating?)

##    For each opponenet tank, find own tank that is closest, and assign opponent to own tank and move agressively





