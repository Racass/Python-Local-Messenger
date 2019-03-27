from pyforms.controls   import ControlTextArea
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from sockets.Exceptions import *

import socket
from threading import Thread
from sockets.enums.IUTypes import IUTypes

class cliente():
    def __init__(self, IP: str, porta: int, clientName: str, clientType: IUTypes, interfaceRef='0'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((IP, porta,))
        except ConnectionRefusedError as e:
                raise ConnErr
                return
        self.name = clientName
        self.sysSendMsg(101, self.name) #Send 101 code to tell name of the client to server
        if(clientType == IUTypes.PyForms): #Generates a thread ready to write on Qt Objects
            self.qwd = interfaceRef    
        self.thread = ReplyHandler(self.sock, self.qwd.worker)
        self.thread.daemon = True
        self.thread.start()
    
    def sendMsg(self, message: str): #Send user message
        self.sock.sendall(('[' + self.name + ']: ' + message).encode())
    def sysSendMsg(self, code: int, message: str): #send a system message (not to be shown)
        self.sock.sendall((str(code) + ':' + message).encode())
    def killConn(self):
        self.sysSendMsg(100, "Desconectado")
    

class ReplyHandler(Thread):
    shouldRun = True
    def __init__(self, sock, qtConn):
        self.sock = sock
        self.qtConn = qtConn
        super().__init__()
    def killMe(self):
        self.shouldRun = False
    def run(self):
        while self.shouldRun:
            try:
                reply = self.sock.recv(1024)
                self.qtConn.sendMsg.emit(reply.decode())
            except ConnectionResetError:
                self.qtConn.sendErr.emit("Desconectado")
                return
