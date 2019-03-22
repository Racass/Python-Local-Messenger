from threading import Thread
from pyforms.controls   import ControlTextArea
from PyQt5.QtCore import *

import socket
class cliente():

    def __init__(self, IP: str, porta: int, clientName: str, qwd):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.qwd = qwd
        try:
            self.sock.connect((IP, porta,))
        except ConnectionRefusedError as e:
                print(e)
                return
        self.name = clientName
        self.sysSendMsg(101, self.name)
        self.setupThread()
        pass
    def sendMsg(self, message: str):
        self.sock.sendall(('[' + self.name + ']: ' + message).encode())

    def sysSendMsg(self, code: int, message: str):
        self.sock.sendall((str(code) + ':' + message).encode())

    def setupThread(self):
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
