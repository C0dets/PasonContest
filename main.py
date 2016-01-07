import sys
from communication import Comm
from policy import Policy


if len(sys.argv) < 3:
    sys.exit("Please provide in this order the match token and server addres(es)")
else:
    matchToken = sys.argv[1]
    commandServerAdd = sys.argv[2]
    stateServerAdd = sys.argv[2]
if len(sys.argv) == 4:
    stateServerAdd = sys.argv[3]

Comm(matchToken, commandServerAdd, stateServerAdd, Policy())


