from sockets.client import cliente
from sockets.enums.IUTypes import IUTypes

from SocketAccess import ClientAccess
from SocketAccess import ServerAccess

class TerminalServer():
    def __init__(self):
        self.serverAcc = ServerAccess(IUTypes.Terminal, self)
        self.serverAcc.ConnectStart()
        print("Servidor Iniciado. Para desativar aperte CTRL+C e ENTER")
        try:
            while(True):
                msg = input()
                self.serverAcc.sendMsg(msg)
        except KeyboardInterrupt as e:
            print("Servidor desligado")
        pass
    
srv = TerminalServer()
