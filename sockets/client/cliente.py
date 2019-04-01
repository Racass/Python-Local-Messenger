import socket

from sockets.enums.IUTypes import IUTypes

from sockets.Exceptions import ConnErr, ClienteNotFound

from sockets.Adapters.serverIUAdapter import Adapter
from sockets.Adapters.PyFormsAdapted import PyFormsAdapted

from sockets.client.ReplyHandler import ReplyHandler

from sockets.objs.message import message

import json

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
        self.createThread()
        
    
    def sendMsg(self, msg: str): #Send user message
        data = message(code=300, msg=msg, client=self.name)
        data = json.dumps(data.__dict__)
        self.sock.sendall(data.encode())
    def sysSendMsg(self, code: int, msg: str): #send a system message
        data = message(code=code, msg=msg, client=self.name)
        data = json.dumps(data.__dict__)
        self.sock.sendall(data.encode())
    def killConn(self):
        self.sysSendMsg(100, "Desconectado")

    def createThread(self):
        self.thread = ReplyHandler(self.sock, self.adapter, self)
        self.thread.daemon = True
        self.thread.start()