from sockets.server.cliente import cliente
from sockets.Exceptions.ClienteNotFound import ClienteNotFound
import socket

class serverInfo():
    '''
    serverInfo is a object that holds the information and connections of the server
    '''
    def __init__(self):
        self.IP = ''
        self.port = '5050'
        self.sock = None
        self.clients = list() #Should receive a cliente()
        pass
    def searchByName(self, clientName: str) -> cliente:
        '''
        returns first reference found of cliente
        '''
        for cliente in self.clients:
            if(cliente.name == clientName):
                return cliente
        raise ClienteNotFound
    def searchByPeer(self, peer: socket) -> cliente:
        '''
        returns first reference found of cliente
        '''
        for cliente in self.clients:
            if(cliente.peer == peer):
                return cliente
        raise ClienteNotFound
