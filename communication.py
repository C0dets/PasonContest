import zmq
import time
import traceback
import sys
import json
import thread
import credentials

from  multiprocessing import Process


class Comm:
    def __init__(self, matchToken, commandServer, stateServer):
        self.matchToken = matchToken

        context = zmq.Context()

        self.commandChannel = context.socket(zmq.REQ)
        print "tcp://%s:5557" % commandServer
        self.commandChannel.connect("tcp://%s:5557" % commandServer)

        self.stateChannel = context.socket(zmq.SUB)
        self.stateChannel.connect("tcp://%s:5556" % stateServer)
        self.stateChannel.setsockopt(zmq.SUBSCRIBE, self.matchToken)

    def start(self, policy):
        self.policy = policy
        self.matchConnect()
        self.monitor()

        self.stateChannel.close()
        self.commandChannel.close()
        context.term()

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
        if (message["comm_type"] == "MatchConnectResp" and message["resp"] == "ok"):
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
                message = json.loads(contents)
                if (message["comm_type"] == "GAME_END"):
                    self.policy.gameRefresh()
                elif (message["comm_type"] == "MATCH_END"):
                    break
                elif (message["comm_type"] == "GAMESTATE"):
                    if (latestStatus):
                        print "Discrading status"
                    latestStatus = message
            except zmq.ZMQError:
                if(latestStatus):
                    try:
                        self.policy.newStatus(latestStatus)
                        latestStatus = 0
                    except:
                        print "Unexpected error:", traceback.format_exc()

    def sendCommand(self, command):
        command["client_token"] = self.clientToken
##        print 'sending', command
        self.commandChannel.send(json.dumps(command))
##        print 'sent'
        message = json.loads(self.commandChannel.recv())
##        print 'recieved'
        if (message["comm_type"] == "ErrorResp"):
            print command
            print message

    def move(self, tankId, direction, distance):
        command = {
            "tank_id" : tankId,
            "comm_type" : "MOVE",
            "direction" : direction,
            "distance" : str(distance)
            }
        self.sendCommand(command)

    def rotateTank(self, tankId, direction, rads):
        command = {
            "tank_id" : tankId,
            "comm_type" : "ROTATE",
            "direction" : direction,
            "rads" : str(rads)
            }
        self.sendCommand(command)

    def rotateTurret(self, tankId, rads):
        if rads > 0:
            direction = 'CCW'
        else:
            direction = 'CW'
            rads = rads * -1  #Make positive
        command = {
            "tank_id" : tankId,
            "comm_type" : "ROTATE_TURRET",
            "direction" : direction,
            "rads" : str(rads)
            }
        self.sendCommand(command)

    def fire(self, tankId):
        command = {
            "tank_id" : tankId,
            "comm_type" : "FIRE"
            }
        self.sendCommand(command)

    def stop(self, tankId, control):
        command = {
            "tank_id" : tankId,
            "comm_type" : "STOP",
            "control" : control
            }
        self.sendCommand(command)
