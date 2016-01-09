from __future__ import division
import numpy as np
import sys
sys.path.insert(0, '../')  ## Add interpreter's path
import mathHelper
from tester import Tester


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

def smallestAngleBetween():
    tester = Tester('smallestAngleBetween')
    twoPi = np.pi * 2
    def truncate(num):
        return '%.4f'%(num)
    tester.compare(truncate(-twoPi*2/6), truncate(mathHelper.smallestAngleBetween(twoPi*1/6, twoPi*5/6)))
    tester.compare(truncate(twoPi*2/6), truncate(mathHelper.smallestAngleBetween(twoPi*5/6, twoPi*1/6)))

    tester.compare(truncate(twoPi*1/6), truncate(mathHelper.smallestAngleBetween(twoPi*1/6, twoPi*2/6)))
    tester.compare(truncate(-twoPi*1/6), truncate(mathHelper.smallestAngleBetween(twoPi*2/6, twoPi*1/6)))

    tester.compare(truncate(-twoPi*3/6), truncate(mathHelper.smallestAngleBetween(twoPi*2/6, twoPi*5/6)))
    tester.compare(truncate(twoPi*3/6), truncate(mathHelper.smallestAngleBetween(twoPi*5/6, twoPi*2/6)))

def rectOnLine():
    '''
    args: lineStart, lineEnd, rectStartPoint, rectDimensions
    '''
    tester = Tester('rectOnLine')
    rectPos = [5, 5]
    rectSize = [5, 5]

    tester.compare(True, mathHelper.rectOnLine(rectPos, rectSize, [6, 11], [6, 4]))
    tester.compare(True, mathHelper.rectOnLine(rectPos, rectSize, [6, 6], [6, 4]))
    tester.compare(True, mathHelper.rectOnLine(rectPos, rectSize, [6, 11], [7, 4]))
    tester.compare(True, mathHelper.rectOnLine(rectPos, rectSize, [6, 11], [6, 6]))
    tester.compare(True, mathHelper.rectOnLine(rectPos, rectSize, [6, 4], [6, 11]))

    tester.compare(True, mathHelper.rectOnLine(rectPos, rectSize, [11, 9], [6, 4]))
    tester.compare(False, mathHelper.rectOnLine(rectPos, rectSize, [6, 1], [7, 1]))
    tester.compare(False, mathHelper.rectOnLine(rectPos, rectSize, [6, 1], [7, 2]))
    tester.compare(False, mathHelper.rectOnLine(rectPos, rectSize, [9, 1], [15, 6]))
    tester.compare(False, mathHelper.rectOnLine(rectPos, rectSize, [1, 11], [11, 11]))

    tester.compare(False, mathHelper.rectOnLine(rectPos, rectSize, [1, 11], [11, 12]))

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
    smallestAngleBetween()
    rectOnLine()
    circleOnLine()
    print 'mathHelper tests Finished!'

if __name__ == "__main__":
    test()



