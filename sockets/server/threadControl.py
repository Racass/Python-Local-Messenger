from sockets.enums import IUTypes
from sockets.server import serverInfo
from sockets.server.connection import Connection
from sockets.Adapters.serverIUAdapter import Adapter
from sockets.objs.message import message
import socket
import json

class ThreadControl(object):
    MAX_CONNECTIONS = 5
    def __init__(self, srv: serverInfo, interface: Adapter):
        self.srv = srv
        self.interface = interface
        self.setup()
        for i in range(self.MAX_CONNECTIONS):
            thread = Connection(self.srv, self.interface, self)
            thread.daemon = True
            thread.start()

    def setup(self):
        global sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.srv.IP, int(self.srv.port),))
        sock.listen(10)
        self.srv.sock = sock
        
    def sendMsg(self, message: message):
        js_objc = json.dumps(message.__dict__)
        for cliente in self.srv.clients:
                cliente.peer.sendall((js_objc).encode())
        pass
    
    def recreateThread(self):
        thread = Connection(self.srv, self.interface, self)
        thread.daemon = True
        thread.start()