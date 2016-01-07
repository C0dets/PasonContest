import sys
sys.path.insert(0, '../')  ## Add interpreter's path
import interpreter

def angleInRange():
    ## Should return true
    if (not interpreter.angleInRange(2, 3, 1) == True):
        raise Exception('Failed angleInRange')
    if (not interpreter.angleInRange(1, 2, -1) == True):
        raise Exception('Failed angleInRange')
    if (not interpreter.angleInRange(6, 1, -1) == True):
        raise Exception('Failed angleInRange')
    if (not interpreter.angleInRange(1, 8, 6) == True):
        raise Exception('Failed angleInRange')
    if (not interpreter.angleInRange(6, 8, 5) == True):
        raise Exception('Failed angleInRange')

    ## Should return false
    if (not interpreter.angleInRange(4, 3, 1) == False):
        raise Exception('Failed angleInRange')
    if (not interpreter.angleInRange(4, 2, -1) == False):
        raise Exception('Failed angleInRange')
    if (not interpreter.angleInRange(4, 8, 5) == False):
        raise Exception('Failed angleInRange')


def test():
    angleInRange()
    print 'All interpreter tests passed!'
