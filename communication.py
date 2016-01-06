import zmq
import time
import sys
import json
import thread
import credentials

from  multiprocessing import Process

context = zmq.Context()

class Comm:
    def __init__(self, matchToken, commandServer, stateServer, policy):
        self.policy = policy
        self.matchToken = matchToken

        context = zmq.Context()

        self.commandChannel = context.socket(zmq.REQ)
        print "tcp://%s:5557" % commandServer
        self.commandChannel.connect("tcp://%s:5557" % commandServer)

        self.stateChannel = context.socket(zmq.SUB)
        self.stateChannel.connect("tcp://%s:5556" % stateServer)
        self.stateChannel.setsockopt(zmq.SUBSCRIBE, self.matchToken)

        self.matchConnect()

        sleep(1)        

        self.monitor()

    def matchConnect(self):
        print 'Connecting...'
        command = json.dumps({"comm_type" : "MatchConnect",
             "match_token" : self.matchToken,
             "team_name" : credentials.username,
             "password" : credentials.password
            })
        self.commandChannel.send(command)
        message = json.loads(self.commandChannel.recv())
        if ("resp" in message and message["resp"] == "ok"):
            print 'Conected to match!'
            self.clientToken = message["client_token"]
        else:
            print 'Failed to connect. :('
            print "Connection status: ", message["message"]

    def monitor(self):
        latestStatus = 0
        while True:
            try:
                [address, contents] = self.stateChannel.recv_multipart(zmq.NOBLOCK)
                latestStatus = json.loads(contents)
                print "Received status"
                #print("[%s] %s\n" % (address, contents))
            except zmq.ZMQError:
                if(latestStatus):
                    self.policy(latestStatus, self)
                    latestStatus = 0

#    def move(self, direction, distance):

#    def 


