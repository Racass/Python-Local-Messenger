from threading import Thread

import socket

from sockets.Adapters.serverIUAdapter import Adapter
from sockets.Adapters.PyFormsAdapted import PyFormsAdapted

class ReplyHandler(Thread):
    shouldRun = True
    def __init__(self, sock: socket, iuAdapter: Adapter):
        self.sock = sock
        self.adapter = iuAdapter
        super().__init__()
    def killMe(self):
        self.shouldRun = False
    def run(self):
        while self.shouldRun:
            try:
                reply = self.sock.recv(1024)
                self.adapter.receiveMsg(reply.decode())
            except ConnectionResetError:
                self.adapter.receiveSysMsg("Desconectado")
                return