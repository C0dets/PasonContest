import zmq
import time
import sys

from  multiprocessing import Process

context = zmq.Context()
 
commandPort = "5557"
statePort = "5556"

def stateChannel():
    context = zmq.Context()
    stateChannel = context.socket(zmq.SUB)
    stateChannel.connect("tcp://localhost:%s" % statePort)
    topicfilter = "10001"
    stateChannel.setsockopt(zmq.SUBSCRIBE, topicfilter)

    print "Running state channel on port: ", statePort

    while True:
        state = stateChannel.recv()
        print "Received state: %s" % message
         
def commandChannel():
    context = zmq.Context()
    print "Starting up command channel on port %s" % commandPort
    commandChannel = context.socket(zmq.REQ)
    commandChannel.connect("tcp://localhost:%s" % commandPort)
    while True:
        print "Sending command"
        command = "Hello"
        commandChannel.send(command)
        message = socket.recv()
        print "Received reply ", "[", message, "]"
        time.sleep(1) 


if __name__ == "__main__":
    Process(target=stateChannel).start()
        
    Process(target=commandChannel).start()
