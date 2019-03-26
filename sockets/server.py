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
                thread = IMS.Connection(self.srv, self.qwd.worker, self)
                thread.daemon = True
                thread.start()
        elif(interfaceType == IUTypes.Terminal):
            for i in range(IMS.MAX_CONNECTIONS):
                thread = IMS.Connection(self.srv, IMS.TerminalConnection(), self)
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
        self.qwd.worker.newClient.connect(self.qwd.receiveClient)
        self.qwd.worker.removeClient.connect(self.qwd.removeCliente)
    class TerminalConnection():
        def emitMsg(self, msg: str):
            raise NotImplementedError
            #TODO create emitMsg
        def emitErr(self, msg: str):
            raise NotImplementedError
            #TODO create emitErr
        def addNewClient(self, clientName: str):
            raise NotImplementedError
            #TODO create addnewClient
            pass
    class QTConnection(QObject):
        sendMsg = pyqtSignal(str)
        sendErr = pyqtSignal(str)
        newClient = pyqtSignal(str)
        removeClient = pyqtSignal(str)
        def __init__(self):
            super().__init__()
        def emitMsg(self, msg: str):
            self.sendMsg.emit(msg)
            return
        def emitErr(self, msg: str):
            self.sendErr.emit(msg)
            return
        def addNewClient(self, client: str):
            self.newClient.emit(client)
            return
        def emitRemoveClient(self, client: str):
            self.removeClient.emit(client)
            pass
    class Connection(Thread):
        def __init__(self, srv: servidor, qtconn, im):
            self.srv = srv
            self.conn = qtconn
            Thread.__init__(self)
            self.ims = im

        def run(self):
            peer, addr = sock.accept()
            self.srv.peers.append(peer)
            while True:
                #try:
                try:
                    message = peer.recv(1024)
                except ConnectionAbortedError:
                    return
                except Exception as e:
                    print(e)
                    return
                if(self.checkSysMsgs(message, peer)):
                    continue
                self.conn.emitMsg(message.decode())
                for other in self.srv.peers:
                    try:
                        if peer != other:
                            other.sendall(message)
                    except ConnectionResetError:
                        #self.conn.emitMsg(self.srv.clientes[peer] + " se desconectou")
                        self.srv.peers.remove(peer)
                        self.srv.clientes.pop(peer)
        def checkSysMsgs(self, message, peer) -> bool:
            if("101:" in message.decode()):
                self.addNewCliente(message, peer)
                return True
            elif("100" in message.decode()):
                self.removeCliente(message, peer)
                return True

        def addNewCliente(self, message, peer):
            clienteName = message.decode().replace("101:", "")
            self.conn.emitMsg(clienteName + " se conectou")
            self.conn.emitErr(clienteName + " se conectou")
            self.conn.addNewClient(clienteName)
            self.srv.clientes[peer] = clienteName

        def removeCliente(self, message, peer):
            clienteName = self.srv.clientes[peer]
            self.conn.emitMsg(clienteName + " se desconectou")
            self.conn.emitErr(clienteName + " se desconectou")
            self.conn.emitRemoveClient(clienteName)
            self.srv.clientes.pop(peer)
            self.srv.peers.remove(peer)
            self.ims.recreateThread()
    def recreateThread(self):
        thread = IMS.Connection(self.srv, self.qwd.worker, self)
        thread.daemon = True
        thread.start()


class Controller():
    def startServer(self, interfaceType: IUTypes , qwd='0'):
        self.srv = servidor()
        self.ims = IMS(self.srv, interfaceType, qwd)
        self.interfaceType = interfaceType
        self.qwd = qwd

    def stopServer(self):
        sock.close()
        for peer in self.srv.peers:
            peer.close()

    def forceUserDiscon(self, clientName: str):
        for peer in self.srv.clientes:
            if(self.srv.clientes[peer] == str(clientName)):
                if(self.interfaceType == IUTypes.PyForms):
                    self.qwd.worker.emitErr("Cliente: " + str(clientName) + " desconectado")
                peer.close()
