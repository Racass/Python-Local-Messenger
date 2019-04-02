from abc import ABC, abstractmethod
from sockets.enums.IUTypes import IUTypes
from sockets.client.cliente import cliente
from sockets.Exceptions import ConnErr
from sockets.server.controller import Controller
from sockets.Adapters.TerminalAdapted import TerminalAdapted


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
    adapter = None
    def __init__(self, IP: str, port: int, clientName: str, interfaceType: IUTypes, Interface):
        self.IP = IP
        self.port = port
        self.clientName = clientName
        self.iu = interfaceType
        self.interface = Interface
        if(ClientAccess.adapter is None and self.iu == IUTypes.PyForms):
            from sockets.Adapters.PyFormsAdapted import PyFormsAdapted
            ClientAccess.adapter = PyFormsAdapted(self.interface)
        elif(self.iu == IUTypes.Terminal):
            ClientAccess.adapter = TerminalAdapted()
        return
    def ConnectStart(self) -> bool:
        try:
            self.cli = cliente(self.IP, int(self.port), self.clientName, ClientAccess.adapter)
            return True
        except Exception as e:
            print(e)
            return False
        except ConnErr as e:
            self.isConnected = False
            print(e)
            return False
    def sendMsg(self, message: str):
        self.cli.sendMsg(message)
        return
    def connKill(self):
        self.cli.killConn()
        pass

class ServerAccess(Access):
    adapter = None
    def __init__(self, InterfaceType: IUTypes, Interface):
        self.interfaceType = InterfaceType
        self.interface = Interface
        return
    def ConnectStart(self) -> bool:
        self.mySrv = Controller()
        if(self.adapter is None and self.interfaceType == IUTypes.PyForms):
            from sockets.Adapters.PyFormsAdapted import PyFormsAdapted
            self.adapter = PyFormsAdapted(self.interface)
        elif(self.interfaceType == IUTypes.Terminal):
            self.adapter = TerminalAdapted()
         #self.adapter = PyFormsAdapted(self.interface)
        self.mySrv.startServer(self.adapter)
        pass
    def sendMsg(self, message: str):
        self.mySrv.sendMessage(message, 'SERVER')
        return
    def forceDisconnect(self, clientName: str):
        self.mySrv.forceUserDiscon(clientName)
        pass
    def connKill(self):
        raise NotImplementedError
        pass


'''class QTConnection(QObject):
        sendMsg = pyqtSignal(str)
        sendErr = pyqtSignal(str)
        def __init__(self):
            from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
            super().__init__()
        def emitMsg(self, msg: str):
            self.sendMsg.emit(msg)
            return
        def emitErr(self, msg: str):
            self.sendErr.emit(msg)
            return
        def addNewClient(self, client: str):
            self.newClient.emit(client)
            return'''
