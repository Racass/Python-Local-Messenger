from threading import Thread
from sockets.server.serverInfo import serverInfo
from sockets.Adapters.serverIUAdapter import Adapter
from sockets.server.cliente import cliente
from sockets.Exceptions.ClienteNotFound import ClienteNotFound
from sockets.objs.message import message
import socket
import json
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
        while meuCli.shouldRun:
            try:
                message = peer.recv(1024)
            except ConnectionAbortedError as e:
                print("Conexão abortada. InnerError: " + str(e)) 
                return
            except Exception as e:
                print("Erro inesperado. InnerError: " + str(e))
                return
            self.prepareMessage(message, peer)
            self.transmitMessage(message, peer)
    
    def transmitMessage(self, message, peer):
        for cliente in self.srv.clients:
                try:
                    if peer != cliente.peer:
                        cliente.peer.sendall(message)
                except ConnectionResetError:
                    self.removeCliente(peer)

    def addNewCliente(self, msg: message, peer):
        clientName = msg.client
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
            self.interface.receiveSysMsg("Grave: cliente adicionado não está na lista de conexões. Não sei como isso aconteceu e nem se pode acontecer, mas enfim")
            return
        cli.name = clientName

    def prepareMessage(self, msg, peer):
        dic = msg
        dic = json.loads(dic)
        mensg = message(dic)
        if mensg.code == 100:
            self.removeCliente(peer)
            #TODO retransmit that the client has disconnect
            pass
        elif mensg.code == 101:
            self.addNewCliente(mensg, peer)
            #TODO retransmit that the client has connected
            pass
        elif mensg.code == 300:
            self.interface.receiveMsg('[' + mensg.client + ']: ' + mensg.msg)
            pass

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
        cliente.shouldRun = False
        self.srv.clients.remove(cliente)
        self.server.recreateThread()
