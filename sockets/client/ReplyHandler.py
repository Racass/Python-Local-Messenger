from threading import Thread

import socket

from sockets.Adapters.serverIUAdapter import Adapter
from sockets.Adapters.PyFormsAdapted import PyFormsAdapted
from sockets.objs.message import message
from sockets.Exceptions.ForcedDisconn import ForceDisconnect

import json

class ReplyHandler(Thread):
    shouldRun = True
    def __init__(self, sock: socket, iuAdapter: Adapter, cliente):
        self.client = cliente
        self.sock = sock
        self.adapter = iuAdapter
        super().__init__()
    def killMe(self):
        self.shouldRun = False
    def run(self):
        while self.shouldRun:
            try:
                reply = self.sock.recv(4096)
                if(reply.decode() == ''):
                    raise ForceDisconnect
                self.prepareMessage(reply.decode())
            except ConnectionResetError:
                #self.adapter.receiveSysMsg("Desconectado pelo servidor")
                self.shouldRun = False
                return
            except ForceDisconnect:
                self.shouldRun = False
                return
            except Exception as e:
                print("Erro inesperado. InnerError: " + str(e))
                self.shouldRun = False
            

    def prepareMessage(self, msg: str):
        dic = msg
        dic = json.loads(dic)
        mensg = message(dic)
        if mensg.code == 200:
            #self.interface.receiveClientDscn(mensg.client)
            pass
        elif mensg.code == 201:
            #self.interface.receiveNewClient(mensg.client)
            pass
        elif mensg.code == 202:
            if(mensg.client == self.client.name):
                self.adapter.receiveSysMsg("O servidor forçou sua desconexão")
                self.shouldRun = False
            else:
                self.adapter.receiveMsg("O servidor desconectou: " + mensg.client)
            pass
        elif mensg.code == 300:
            self.adapter.receiveMsg('[' + mensg.client + ']: ' + mensg.msg)
            pass
