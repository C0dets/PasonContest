import math

hitRad = 2
colRad = 2

class Interpreter:
    def __init__(self, status):
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
        distance = self.distance(tank1['position'], tank1['position'])
        if (distance > 100 + hitRad):
            return false

        ## Check that were not firing at self

        ## Check for obstacles

        return true


    def distance(self, point1, point2):
        xDist = point1[0] - point2[0]
        yDist = point1[1] - point2[1]
        return math.sqrt((xDist * xDist) + (yDist * yDist))





