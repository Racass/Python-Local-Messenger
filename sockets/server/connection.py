from threading import Thread
from sockets.server.serverInfo import serverInfo
from sockets.Adapters.PyFormsAdapted import Adapter
from sockets.server.cliente import cliente
from sockets.Exceptions.ClienteNotFound import ClienteNotFound
import socket

class Connection(Thread):
    def __init__(self, srv: serverInfo, interface: Adapter, servidor):
        self.srv = srv
        self.interface = interface
        Thread.__init__(self)
        self.server = servidor

    def run(self):
        peer, addr = self.srv.sock.accept() #TODO
        meuCli = cliente(peer, '', addr)
        self.srv.clients.append(meuCli)
        while True:
            try:
                message = peer.recv(1024)
            except ConnectionAbortedError:
                print("erro de conexão")
                return
            except Exception as e:
                print(e)
                return
            if(self.checkSysMsgs(message, peer)):
                continue
            self.interface.receiveMsg(message.decode())
            self.transmitMessage(message, peer)

    def transmitMessage(self, message, peer):
        for cliente in self.srv.clients:
                try:
                    if peer != cliente.peer:
                        cliente.peer.sendall(message)
                except ConnectionResetError:
                    self.removeCliente(peer)

    def checkSysMsgs(self, message, peer) -> bool:
        if("101:" in message.decode()):
            self.addNewCliente(message, peer)
            return True
        elif("100" in message.decode()):
            self.removeCliente(peer)
            return True

    def addNewCliente(self, message, peer):
        clientName = message.decode().replace("101:", "")
        self.interface.receiveMsg(clientName + " se conectou")
        self.interface.receiveSysMsg(clientName + " se conectou")
        self.interface.receiveNewClient(clientName)
        try:
            cli = self.srv.searchByPeer(peer)
        except Exception as e:
            print(e)
            return
        except ClienteNotFound:
            print("Cliente não encontrado")
            return
        cli.name = clientName


    def removeCliente(self, message, peer):
        try:
            cliente = self.srv.searchByPeer(peer)
        except Exception as e:
            print(e)
        except ClienteNotFound:
            print("Cliente não encontrado")
            return
        self.interface.receiveMsg(cliente.name + " se desconectou")
        self.interface.receiveSysMsg(cliente.name + " se desconectou")
        self.interface.receiveClientDscn(cliente.name)
        self.srv.clients.remove(cliente)
        self.server.recreateThread()
    def removeCliente(self, peer):
        try:
            cliente = self.srv.searchByPeer(peer)
        except Exception as e:
            print(e)
        except ClienteNotFound:
            print("Cliente não encontrado")
            return
        self.interface.receiveMsg(cliente.name + " se desconectou")
        self.interface.receiveSysMsg(cliente.name + " se desconectou")
        self.interface.receiveClientDscn(cliente.name)
        cliente.peer.close()
        self.srv.clients.remove(cliente)
        self.server.recreateThread()