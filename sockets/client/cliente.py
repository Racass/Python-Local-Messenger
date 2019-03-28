import socket

from sockets.enums.IUTypes import IUTypes

from sockets.Exceptions.ConnErr import ConnErr
from sockets.Exceptions.ClienteNotFound import ClienteNotFound

from sockets.Adapters.serverIUAdapter import Adapter
from sockets.Adapters.PyFormsAdapted import PyFormsAdapted

from sockets.client.ReplyHandler import ReplyHandler

class cliente():
    def __init__(self, IP: str, porta: int, clientName: str, iuAdapter: Adapter):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((IP, porta,))
        except ConnectionRefusedError as e:
                raise ConnErr
                return
        self.name = clientName
        self.adapter = iuAdapter
        self.sysSendMsg(101, self.name) #Send 101 code to tell name of the client to server
        
    
    def sendMsg(self, message: str): #Send user message
        self.sock.sendall(('[' + self.name + ']: ' + message).encode())
    def sysSendMsg(self, code: int, message: str): #send a system message (not to be shown)
        self.sock.sendall((str(code) + ':' + message).encode())
    def killConn(self):
        self.sysSendMsg(100, "Desconectado")

    def createThread():
        self.thread = ReplyHandler(self.sock, self.adapter)
        self.thread.daemon = True
        self.thread.start()