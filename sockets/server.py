from threading import Thread
import socket

class servidor():
    def __init__(self):
        self.IP = '127.0.0.1'
        self.port = '5050'
        pass

sock, peers = None, []
clientes = {} # Add dictionary to peer as key and Cliente Name as value

class IMS(object):
    MAX_CONNECTIONS = 5

    def __init__(self):
        self.setup()
        for i in range(IMS.MAX_CONNECTIONS):
            thread = IMS.Connection()
            thread.daemon = True
            thread.start()

    def setup(self):
        global sock
        self.server = servidor()  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.setsockopt(socket.SOL_SOCKET, 1)
        sock.bind((self.server.IP, int(self.server.port),))
        sock.listen(10)

    def send_message(self, message):
        for peer in peers:
            if(message is bytes):
                peer.sendall('[SERVER]: ' + message)
            else:
                peer.sendall(('[SERVER]: ' + message.decode()).encode())

    class Connection(Thread):
        def __init__(self):
            Thread.__init__(self)
        def run(self):
            peer, addr = sock.accept()
            peers.append(peer)
            while True:
                #try:
                message = peer.recv(1024)
                if("101:" in message.decode()):
                    self.addNewCliente(message, peer)
                    continue
                print(message.decode())
                for other in peers:
                    if peer != other:
                        other.sendall(message)
                #except ConnectionResetError:
                #    print(clientes[peer] + " se desconectou")
                #    peers.remove(peer)
                #    clientes.pop(peer)
        
        def addNewCliente(self, message, peer):
            clienteName = message.decode().replace("101:", "")
            print(clienteName + " se conectou")
            clientes[peer] = clienteName

ims = IMS()
try:
    while 1:
        message = input()
        ims.send_message(message.encode())
except KeyboardInterrupt:
    sock.close()
    for peer in peers:
        peer.close()