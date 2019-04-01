from abc import ABC, abstractmethod
from sockets.Adapters.serverIUAdapter import Adapter

class TerminalAdapted(Adapter):
    def __init__(self):
        super().__init__()
        pass

    def receiveMsg(self, msg: str):
        print(msg)
        pass

    def receiveSysMsg(self, msg: str):
        print('[Mensagem do sistema]: ' + msg)
        pass
    
    def receiveNewClient(self, clientName: str):
        print('[' + clientName +']' + ' conectou-se')
        pass
    
    def receiveClientDscn(self, clientName: str):
        pass
