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
    stateChannel.connect("tcp://ip-10-0-0-149.ec2.internal:%s" % statePort)
    topicfilter = "a10bf4bf-0705-4da9-947e-c016f8d77d0a"
    stateChannel.setsockopt(zmq.SUBSCRIBE, topicfilter)

    print "Running state channel on port: ", statePort

    while True:	
        #string = stateChannel.recv()
        #topic, messagedata = string.split()
        #total_value += int(messagedata)
        #print topic, messagedata
        [address, contents] = stateChannel.recv_multipart()
        print("[%s] %s\n" % (address, contents))
         
def commandChannel():
    print "hello2"
    context = zmq.Context()
    print "Starting up command channel on port %s" % commandPort
    commandChannel = context.socket(zmq.REQ)
    commandChannel.connect("tcp://ip-10-0-0-149.ec2.internal:%s" % commandPort)
    matchConnectReq = json.dumps({"comm_type" : "MatchConnect",
 "match_token" : "a10bf4bf-0705-4da9-947e-c016f8d77d0a",
 "team_name" : "Codets",
 "password" : "theeleventhfrog"
})
    message = commandChannel.send(matchConnectReq)
    print "Received reply ", "[", message, "]"
    while True:
        print "Sending match connect command"
        command = "Hello"
        message = commandChannel.recv()
        print "Received reply ", "[", message, "]"
        time.sleep(1) 


if __name__ == "__main__":

    Process(target=stateChannel).start()
        
    Process(target=commandChannel).start()
