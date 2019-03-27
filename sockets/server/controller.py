from sockets.server.serverInfo import serverInfo
from sockets.server.threadControl import ThreadControl
from sockets.enums.IUTypes import IUTypes
from sockets.server.Adapters.serverIUAdapter import Adapter
from sockets.server.Adapters.PyFormsAdapted import PyFormsAdapted

class Controller():
    '''
    Controller is the principal method of the server
    Start the server, stop it, force disconnections, hold references for serverInfo and cliente
    '''
    def startServer(self, interfaceAdapter: Adapter):
        self.srv = serverInfo()
        self.adapter = interfaceAdapter
        self.server = ThreadControl(self.srv, interfaceAdapter)
    def sendMessage(self, message: str):
        self.server.send_message(message)
        pass

    def stopServer(self):
        self.sock.close()
        for cliente in self.srv.clients:
            cliente.closeConnection()

    def forceUserDiscon(self, clientName: str):
        for cliente in self.srv.clients:
            if(cliente.name == clientName):
                self.adapter.receiveClientDscn(clientName)
                cliente.closeConnection()