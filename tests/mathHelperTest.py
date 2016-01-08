import sys
sys.path.insert(0, '../')  ## Add interpreter's path
import mathHelper

def angleInRange():
    ## Should return true
    if (not mathHelper.angleInRange(2, 3, 1) == True):
        raise Exception('Failed angleInRange')
    if (not mathHelper.angleInRange(1, 2, -1) == True):
        raise Exception('Failed angleInRange')
    if (not mathHelper.angleInRange(6, 1, -1) == True):
        raise Exception('Failed angleInRange')
    if (not mathHelper.angleInRange(1, 8, 6) == True):
        raise Exception('Failed angleInRange')
    if (not mathHelper.angleInRange(6, 8, 5) == True):
        raise Exception('Failed angleInRange')

    ## Should return false
    if (not mathHelper.angleInRange(4, 3, 1) == False):
        raise Exception('Failed angleInRange')
    if (not mathHelper.angleInRange(4, 2, -1) == False):
        raise Exception('Failed angleInRange')
    if (not mathHelper.angleInRange(4, 8, 5) == False):
        raise Exception('Failed angleInRange')

def circleOnLine():
    ## Should return the distance to an intersection point
    if (mathHelper.circleOnLine([0,0],[10,0],[5,1],1) != 5):
        raise Exception('Failed circleOnLine')    
    if (mathHelper.circleOnLine([0,5],[10,5],[5,5],1) != 4):
        raise Exception('Failed circleOnLine')    
    if (mathHelper.circleOnLine([0,5],[10,5],[0,5],1) != 1):
        raise Exception('Failed circleOnLine')    
    if (mathHelper.circleOnLine([0,5],[10,5],[10,5],1) != 9):
        raise Exception('Failed circleOnLine')

    ## Should return false
    if (not mathHelper.circleOnLine([4.5,12.5],[14.5,5.5],[12,9],1.414) == False):
        raise Exception('Failed circleOnLine')
    if (not mathHelper.circleOnLine([4.5,12.5],[14.5,5.5],[2,3],2) == False):
        raise Exception('Failed circleOnLine')

def test():
    angleInRange()
    circleOnLine()
    print 'All mathHelper tests passed!'
