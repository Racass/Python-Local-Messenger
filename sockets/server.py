from threading import Thread
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import socket
from sockets.client import IUTypes

class servidor():
    def __init__(self):
        self.IP = ''
        self.port = '5050'
        self.sock = None
        self.peers = []
        self.clientes = {}
        pass

class IMS(object):
    MAX_CONNECTIONS = 5

    def __init__(self, srv: servidor, interfaceType: IUTypes, qwd='0'):
        self.srv = srv
        self.qwd = qwd
        self.setup()
        if(interfaceType == IUTypes.PyForms):
            self.setupThread()
            for i in range(IMS.MAX_CONNECTIONS):
                thread = IMS.Connection(self.srv, self.qwd.worker)
                thread.daemon = True
                thread.start()
        elif(interfaceType == IUTypes.Terminal):
            for i in range(IMS.MAX_CONNECTIONS):
                thread = IMS.Connection(self.srv, IMS.TerminalConnection())
                thread.daemon = True
                thread.start()

    def setup(self):
        global sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.srv.IP, int(self.srv.port),))
        sock.listen(10)

    def send_message(self, message):
        for peer in self.srv.peers:
            if(isinstance(message, str)):
                peer.sendall(('[SERVER]: ' + message).encode())
            else:
                peer.sendall(('[SERVER]: ' + message.decode()).encode())
    def setupThread(self):
        self.qwd.thread = QThread()
        self.qwd.worker = IMS.QTConnection()
        self.qwd.worker.moveToThread(self.qwd.thread)
        self.qwd.worker.sendErr.connect(self.qwd.writeLog)
        self.qwd.worker.sendMsg.connect(self.qwd.writeMsg)

    class TerminalConnection():
        def emitMsg(self, msg: str):
            print(msg)
        def emitErr(self, msg: str):
            print(msg)

    class QTConnection(QObject):
        sendMsg = pyqtSignal(str)
        sendErr = pyqtSignal(str)
        def __init__(self):
            super().__init__()
        def emitMsg(self, msg: str):
            self.sendMsg.emit(msg)
            pass
        def emitErr(self, msg: str):
            self.sendErr.emit("Desconectado")
            pass
    class Connection(Thread):
        def __init__(self, srv: servidor, qtconn):
            self.srv = srv
            self.conn = qtconn
            Thread.__init__(self)
    
        def run(self):
            peer, addr = sock.accept()
            self.srv.peers.append(peer)
            while True:
                #try:
                message = peer.recv(1024)
                if("101:" in message.decode()):
                    self.addNewCliente(message, peer)
                    continue
                self.conn.emitMsg(message.decode())
                for other in self.srv.peers:
                    try:
                        if peer != other:
                            other.sendall(message)
                    except ConnectionResetError:
                        self.conn.emitMsg(self.srv.clientes[peer] + " se desconectou")
                        self.srv.peers.remove(peer)
                        self.srv.clientes.pop(peer)
        
        def addNewCliente(self, message, peer):
            clienteName = message.decode().replace("101:", "")
            self.conn.emitMsg(clienteName + " se conectou")
            self.srv.clientes[peer] = clienteName

class Controller():
    def startServer(self, interfaceType: IUTypes , qwd='0'):
        self.srv = servidor()
        self.ims = IMS(self.srv, interfaceType, qwd)
    def stopServer(self):
        sock.close()
        for peer in self.srv.peers:
            peer.close()