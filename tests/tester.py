from __future__ import division

class Tester:
    def __init__(self, testName):
        self.testName = testName
        self.testNum = 0

    def compare(self, expected, actual):
        self.testNum += 1
        if expected != actual:
            print 'Test #', self.testNum, ' of ', self.testName, ' failed. :('
            print 'Expected: ', expected
            print 'Actual:   ', actual
