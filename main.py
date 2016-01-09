from __future__ import division
import sys
from communication import Comm
from policy import Policy


if len(sys.argv) < 4:
    sys.exit("Please provide in this order the match token and server addres(es)")
else:
    predictionFactor = sys.argv[1]
    matchToken = sys.argv[2]
    commandServerAdd = sys.argv[3]
    stateServerAdd = sys.argv[3]
if len(sys.argv) == 5:
    stateServerAdd = sys.argv[4]

## creaate com and policy
comm = Comm(matchToken, commandServerAdd, stateServerAdd)
policy = Policy(comm, predictionFactor)

## Start the match
comm.start(policy)


