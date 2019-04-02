from sockets.client import cliente
from sockets.enums.IUTypes import IUTypes

from SocketAccess import ClientAccess
from SocketAccess import ServerAccess

class TerminalClient():
    def __init__(self):
        self.getInfo()
        self.clientAcc = ClientAccess(self.ip, int(self.port), self.user, IUTypes.Terminal, self)
        self.clientAcc.ConnectStart()
        print("Conectado... Para sair aperte CTRL+C e ENTER")
        try:
            while(True):
                msg = input()
                self.clientAcc.sendMsg(msg)
        except KeyboardInterrupt as e:
            print("Desconectado")
        pass

    def getInfo(self):
        print("IP:")
        self.ip = input()
        print("PORTA:")
        self.port = input()
        print("USUARIO:")
        self.user = input()

cli = TerminalClient()