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

        self.monitor()

    def matchConnect(self):
        print 'Connecting...'
        command = json.dumps({
             "comm_type" : "MatchConnect",
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
                if (latestStatus):
                    print "Discrading status"
                latestStatus = json.loads(contents)
                #print "Received status"
                #print("[%s] %s\n" % (address, contents))
            except zmq.ZMQError:
                if(latestStatus):
                    try:
                        self.policy(latestStatus, self)
                        latestStatus = 0
                    except:
                        print "Unexpected error:", sys.exc_info()[0]

    def move(self, tankId, direction, distance):
        command = json.dumps({
            "tank_id" : tankId,
            "comm_type" : "MOVE",
            "direction" : direction,
            "distance" : str(distance),
            "client_token" : self.clientToken
            })
        self.commandChannel.send(command)
        message = json.loads(self.commandChannel.recv())
        if (message["comm_type"] != "MoveResp" or "resp" not in message or message["resp"] != "ok"):
            print "Move failed"
            print message


    def rotateTank(self, tankId, direction, rads):
        command = json.dumps({
            "tank_id" : tankId,
            "comm_type" : "ROTATE",
            "direction" : direction,
            "rads" : str(rads),
            "client_token" : self.clientToken
            })
        self.commandChannel.send(command)
        message = json.loads(self.commandChannel.recv())
        if (message["comm_type"] != "MoveResp" or "resp" not in message or message["resp"] != "ok"):
            print command
            print "Tank rotation failed"
            print message

    def rotateTurret(self, tankId, direction, rads):
        command = json.dumps({
            "tank_id" : tankId,
            "comm_type" : "ROTATE_TURRET",
            "direction" : direction,
            "rads" : str(rads),
            "client_token" : self.clientToken
            })
        self.commandChannel.send(command)
        message = json.loads(self.commandChannel.recv())
        if (message["comm_type"] != "MoveResp" or "resp" not in message or message["resp"] != "ok"):
            print command
            print "Turret rotation failed"
            print message

    def fire(self, tankId):
        command = json.dumps({
            "tank_id" : tankId,
            "comm_type" : "FIRE",
            "client_token" : self.clientToken
            })
        self.commandChannel.send(command)
        message = json.loads(self.commandChannel.recv())
        if (message["comm_type"] != "MoveResp" or "resp" not in message or message["resp"] != "ok"):
            print command
            print "Fire failed"
            print message

    def stop(self, tankId, command):
        command = json.dumps({
            "tank_id" : tankId,
            "comm_type" : "STOP",
            "control" : command,
            "client_token" : self.clientToken
            })
        self.commandChannel.send(command)
        message = json.loads(self.commandChannel.recv())
        if (message["comm_type"] != "MoveResp" or "resp" not in message or message["resp"] != "ok"):
            print command
            print "Stopping failed"
            print message
