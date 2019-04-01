from sockets.server.serverInfo import serverInfo
from sockets.server.threadControl import ThreadControl
from sockets.enums.IUTypes import IUTypes
from sockets.Adapters.serverIUAdapter import Adapter
from sockets.Adapters.PyFormsAdapted import PyFormsAdapted
from sockets.objs.message import message

class Controller():
    '''
    Controller is the principal method of the server
    Start the server, stop it, force disconnections, hold references for serverInfo and cliente
    '''
    def startServer(self, interfaceAdapter: Adapter):
        self.srv = serverInfo()
        self.adapter = interfaceAdapter
        self.server = ThreadControl(self.srv, interfaceAdapter)

    def sendMessage(self, msg: str, clientName: str):
        self.server.sendMsg(message(code=300, msg=msg, client=clientName))

    def sendSysMsg(self, code: int, msg: str, clientName: str):
        self.server.sendMsg(message(code=code, msg=msg, client=clientName))

    def stopServer(self):
        self.sock.close()
        for cliente in self.srv.clients:
            cliente.closeConnection()

    def forceUserDiscon(self, clientName: str):
        for cliente in self.srv.clients:
            if(cliente.name == clientName):
                self.sendSysMsg(202, "server wanted to disconnect you", cliente.name)
                self.adapter.receiveClientDscn(clientName)
                cliente.closeConnection()
                self.srv.clients.remove(cliente)