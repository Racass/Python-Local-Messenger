from abc import ABC, abstractmethod
from sockets.client import IUTypes
from sockets.client import cliente
from sockets.Exceptions import ConnErr
from sockets.server import Controller

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

class ClientAccess(Access):
    def __init__(self, IP: str, port: int, clientName: str, InterfaceType: IUTypes, Interface):
        self.IP = IP
        self.port = port
        self.clientName = clientName
        self.iu = InterfaceType
        self.interface = Interface
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

class ServerAccess(Access):
    def __init__(self, InterfaceType: IUTypes, Interface):
        self.interface = Interface
        return
    def ConnectStart(self) -> bool:
        self.mySrv = Controller()
        self.mySrv.startServer(self.interface)
    def sendMsg(self, message: str):
        self.mySrv.ims.send_message(message)
        return
