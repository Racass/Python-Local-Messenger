from abc import ABC, abstractmethod
from sockets.client import IUTypes
from sockets.client import cliente
from sockets.Exceptions import ConnErr
from sockets.server import Controller
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

class Access(ABC):
    def __init__(self, IP: str, port: int, clientName: str, InterfaceType: IUTypes, Interface):
        super().__init__()
        pass
    @abstractmethod
    def ConnectStart(self):
        pass
    @abstractmethod
    def sendMsg(self):
        pass
    @abstractmethod
    def connKill(self):
        pass

class ClientAccess(Access):
    def __init__(self, IP: str, port: int, clientName: str, InterfaceType: IUTypes, Interface):
        self.IP = IP
        self.port = port
        self.clientName = clientName
        self.iu = InterfaceType
        self.interface = Interface
        if(self.interface.worker is None):
            self.setupQtThread()
        return
    def ConnectStart(self) -> bool:
        try:
            self.cli = cliente(self.IP, int(self.port), self.clientName, self.iu, self.interface)
            return True
        except Exception as e:
            print(e)
            return False
        except ConnErr:
            self.isConnected = False
            return False
    def sendMsg(self, message: str):
        self.cli.sendMsg(message)
        return
    def connKill(self):
        self.cli.killConn()
        pass
    def setupQtThread(self):
        self.interface.thread = QThread()
        self.interface.worker = QTConnection()
        self.interface.worker.moveToThread(self.interface.thread)
        self.interface.worker.sendErr.connect(self.interface.writeLog)
        self.interface.worker.sendMsg.connect(self.interface.writeMsg)
        self.interface.thread.start()

class ServerAccess(Access):
    def __init__(self, InterfaceType: IUTypes, Interface):
        self.interfaceType = InterfaceType
        self.interface = Interface
        return
    def ConnectStart(self) -> bool:
        self.mySrv = Controller()
        self.mySrv.startServer(self.interfaceType, self.interface)
    def sendMsg(self, message: str):
        self.mySrv.ims.send_message(message)
        return
    def forceDisconnect(self, clientName: str):
        self.mySrv.forceUserDiscon(clientName)
        pass
    def connKill(self):
        raise NotImplementedError
        pass



class QTConnection(QObject):
        sendMsg = pyqtSignal(str)
        sendErr = pyqtSignal(str)
        def __init__(self):
            super().__init__()
        def emitMsg(self, msg: str):
            self.sendMsg.emit(msg)
            return
        def emitErr(self, msg: str):
            self.sendErr.emit(msg)
            return
        def addNewClient(self, client: str):
            self.newClient.emit(client)
            return