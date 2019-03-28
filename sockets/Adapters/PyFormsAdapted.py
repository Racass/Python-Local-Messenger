from abc import ABC, abstractmethod
from sockets.Adapters.serverIUAdapter import Adapter
from PyQt5.QtCore import pyqtSignal, QThread, QObject
from pyforms.basewidget import BaseWidget

class PyFormsAdapted(Adapter):
    
    def __init__(self, pyFormsRef: BaseWidget):
        self.interface = pyFormsRef
        self.setupQtThread()
        super().__init__()
    def receiveMsg(self, msg: str):
        self.interface.worker.receiveMsg(msg)
        pass
    def receiveSysMsg(self, msg: str):
        self.interface.worker.receiveSysMsg(msg)
        pass
    def receiveNewClient(self, clientName: str):
        self.interface.worker.receiveNewClient(clientName)
        pass
    def receiveClientDscn(self, clientName: str):
        self.interface.worker.receiveClientDscn(clientName)
        pass
    def setupQtThread(self):
        self.interface.thread = QThread()
        self.interface.worker = QTConnection()
        self.interface.worker.moveToThread(self.interface.thread)
        self.interface.worker.sendErr.connect(self.interface.writeLog)
        self.interface.worker.sendMsg.connect(self.interface.writeMsg)
        self.interface.worker.newClient.connect(self.interface.receiveClient)
        self.interface.worker.removeClient.connect(self.interface.removeCliente)
        self.interface.thread.start()
        pass

class QTConnection(QObject):
    sendMsg = pyqtSignal(str)
    sendErr = pyqtSignal(str)
    newClient = pyqtSignal(str)
    removeClient = pyqtSignal(str)
    def __init__(self):
        super().__init__()
    def receiveMsg(self, msg: str):
        self.sendMsg.emit(msg)
        pass
    def receiveSysMsg(self, msg: str):
        self.sendErr.emit(msg)
        pass
    def receiveNewClient(self, clientName: str):
        self.newClient.emit(clientName)
        pass
    def receiveClientDscn(self, clientName: str):
        self.removeClient.emit(clientName)
        pass