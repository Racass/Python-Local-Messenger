import socket

class cliente():
    '''
    cliente is a object that holds usefull information and methods about connected clients
    '''
    def __init__(self, peer: socket, name: str, addr: str):
        self.peer = peer #peer is a socket connection of client
        self.name = name #name of the client
        self.addr = addr # IP address of the client
        self.shouldRun = True
    def closeConnection(self):
        self.shouldRun = False
        self.peer.close()
