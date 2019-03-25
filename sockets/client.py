from pyforms.controls   import ControlTextArea
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from sockets.Exceptions import *
from enum import Enum
import socket

class IUTypes(Enum):
    PyForms = 1,
    Terminal = 2

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
            self.setupQtThread()
        pass
    
    def sendMsg(self, message: str): #Send user message
        self.sock.sendall(('[' + self.name + ']: ' + message).encode())

    def sysSendMsg(self, code: int, message: str): #send a system message (not to be shown)
        self.sock.sendall((str(code) + ':' + message).encode())

    def setupQtThread(self):
        self.qwd.thread = QThread()
        self.qwd.worker = ReplyHandler(self.sock)
        self.qwd.worker.moveToThread(self.qwd.thread)
        self.qwd.worker.sendErr.connect(self.qwd.writeLog)
        self.qwd.worker.sendMsg.connect(self.qwd.writeMsg)
        self.qwd.thread.started.connect(self.qwd.worker.run)
        self.qwd.thread.start()

class ReplyHandler(QObject):
    sendMsg = pyqtSignal(str)
    sendErr = pyqtSignal(str)
    def __init__(self, sock):
        self.sock = sock
        super().__init__()
    @pyqtSlot()
    def run(self):
        while True:
            try:
                reply = self.sock.recv(1024)
                self.sendMsg.emit(reply.decode())
            except ConnectionResetError:
                self.sendErr.emit("Desconectado")
                return
