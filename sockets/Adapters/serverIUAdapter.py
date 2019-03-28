from abc import ABC, abstractmethod

class Adapter(ABC):
    def __init__(self):
        super().__init__()
        pass
    @abstractmethod
    def receiveMsg(self, msg: str):
        pass
    @abstractmethod
    def receiveSysMsg(self, msg: str):
        pass
    @abstractmethod
    def receiveNewClient(self, clientName: str):
        pass
    @abstractmethod
    def receiveClientDscn(self, clientName: str):
        pass
