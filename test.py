import zmq
import time
import sys
import json

from  multiprocessing import Process

context = zmq.Context()
 
commandPort = "5557"
statePort = "5556"

def stateChannel():
    print "hello1"
    context = zmq.Context()
    stateChannel = context.socket(zmq.SUB)
    stateChannel.connect("tcp://ip-10-0-0-229.ec2.internal:%s" % statePort)
    topicfilter = "10001"
    stateChannel.setsockopt(zmq.SUBSCRIBE, topicfilter)

    print "Running state channel on port: ", statePort

    while True:	
        #string = stateChannel.recv()
        #topic, messagedata = string.split()
        #total_value += int(messagedata)
        #print topic, messagedata
        state = stateChannel.recv()
        print "Received state: %s" % message
         
def commandChannel():
    print "hello2"
    context = zmq.Context()
    print "Starting up command channel on port %s" % commandPort
    commandChannel = context.socket(zmq.REQ)
    commandChannel.connect("tcp://ip-10-0-0-229.ec2.internal:%s" % commandPort)
    command = json.dumps({"comm_type" : "MatchConnect",
 "match_token" : "eb973698-91d0-4c44-9fb4-dca21b849f16",
 "team_name" : "Codets",
 "password" : "theeleventhfrog"
})
    while True:
        print "Sending command"
        #command = "Hello"
        commandChannel.send(command)
        message = commandChannel.recv()
        print "Received reply ", "[", message, "]"
        time.sleep(1) 


if __name__ == "__main__":
    Process(target=stateChannel).start()
        
    Process(target=commandChannel).start()
