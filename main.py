import os
import sys

from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlLabel
from pyforms.controls   import ControlText
from pyforms.controls   import ControlButton
from pyforms.controls   import ControlTextArea
from pyforms.controls   import ControlList
from pyforms.controls   import ControlCombo

from PyQt5.QtCore import *
from PyQt5 import QtWidgets

from sockets.client import cliente
from sockets.enums.IUTypes import IUTypes

from SocketAccess import ClientAccess
from SocketAccess import ServerAccess

class RafacaMsg(BaseWidget):
    worker = None
    isConn = False

    def __init__(self, *args, **kwargs):
        super().__init__("")
        self.Title    = ControlLabel("Rafaca's messenger")
        self.createTabConn()
        self.createTabMensagens()
        self.createTabClientes()
        self._formset = [ 
            (' ', 'Title', ' '),
            {
                'Tab1:Conexao': [('User'), ('IP', 'host', 'conn'), (' ', 'srv', ' '), ('Errors'), ' '],
                'Tab2:Mensagens': ['mensagens', ('mensagem', 'sendMsg'), ' '],
                'Tab3:Clientes': [('clients'), ('clientesCombo', 'clientDisconn')]
            }
        ]
        if(len(sys.argv) > 1):
            self.debugStart(int(sys.argv[1].upper()))
            pass
    
    def createTabClientes(self):
        self.clients = ControlList('Clientes conectados')
        self.clientesCombo = ControlCombo()
        self.clientDisconn = ControlButton("Desconectar")
        self.clientDisconn.value = self.forceDescon
        self.clients.readonly = True
    
    def createTabConn(self):
        self.User = ControlText("NomeUsuario: ")
        self.IP = ControlText("Endereço IP: ")
        self.host = ControlText("Porta do servidor: ")
        self.conn = ControlButton("Conectar")
        self.srv = ControlButton("Iniciar servidor")
        self.Errors = ControlTextArea("")
        self.conn.value = self.connClick
        self.srv.value = self.srvClick
        self.Errors.enabled = False
        self.Errors.autoscroll = True
    
    def createTabMensagens(self):
        self.mensagens = ControlTextArea('Mensagens')
        self.mensagem = ControlText('Sua mensagem')
        self.sendMsg = ControlButton('Enviar')
        self.mensagens.autoscroll = True
        self.mensagens.enabled = False
        self.sendMsg.value = self.sendMsgClick
        pass
    
    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return):
            if(self._tabs[0].currentIndex() == 0):
                self.conn.click()
            elif(self._tabs[0].currentIndex() == 1):
                self.sendMsg.click()
        event.accept()
    
    def sendMsgClick(self):
        if(self.isConn == False): 
            self.writeLog("Você não está conectado e não é um servidor.")
            return
        self.access.sendMsg(self.mensagem.value)
        self.saveMsg()
        return
    
    def connClick(self):
        if(self.isConn):
            self.isConn = False
            self.writeLog("Desconectado")
            self.conn.label = 'Conectar'
            self.setConnInputs(True)
            self.access.connKill()
            return
        if(self.ValidateConnInputs() == False):
            return
        self.access = ClientAccess(self.IP.value, int(self.host.value), self.User.value, IUTypes.PyForms, self)
        if(self.access.ConnectStart() == True):
            self.isConn = True
            self.writeLog('Conectado em: ' + self.IP.value + ':' + self.host.value)
            self.conn.label = 'Desconectar'
            self.setConnInputs(False)
        else:
            self.isConn = False
            self.writeLog('Erro ao conectar em: ' + self.IP.value + ':' + self.host.value)
            self.writeLog('Favor tentar novamente em alguns minutos.')
            return
        return
    
    def srvClick(self):
        if(self.isConn == False):
            self.access = ServerAccess(IUTypes.PyForms, self)
            self.access.ConnectStart()
            self.setConnInputs(False)
            self.isConn = True
            self.writeLog("Servidor iniciado")
        return

    def ValidateConnInputs(self) -> bool:
        if(self.IP.value == ''):
            self.Errors.value += '\nFavor colocar um endereço IP!'
            return False
        elif(self.host.value == ''):
            self.Errors.value += '\nFavor colocar uma porta!'
            return False
        elif(self.User.value == ''):
            self.Errors.value += '\nFavor colocar um usuario!'
            return False
        return True

    def setConnInputs(self, status: bool):
        self.IP.enabled = status
        self.host.enabled = status
        self.User.enabled = status
        self.srv.enabled = status
    
    def saveMsg(self):
        self.writeMsg("[Você]: " + self.mensagem.value)
        self.mensagem.value = ''
    
    @pyqtSlot(str)
    def writeLog(self, value):
        self.Errors.enabled = True
        self.Errors.__add__('[Log]: ' + value) 
        self.Errors.enabled = False
    
    @pyqtSlot(str)
    def writeMsg(self, value):
        self.mensagens.enabled = True
        self.mensagens.__add__(value)
        self.mensagens.enabled = False
    
    @pyqtSlot(str)
    def receiveClient(self, value):
        x = [value]
        self.clients.__add__(x)
        self.clientesCombo.add_item(value)
        pass
    
    @pyqtSlot(str)
    def removeCliente(self, clientName: str):
        '''tempList = []
        for cli in self.clients.value:
            if(cli[0] != clientName):
                tempList.append(cli[0])
                pass
        self.clients.clear()
        self.clientesCombo.clear()
        for cliente in tempList:
            cli = [cliente]
            self.clients.__add__(cli)
            self.clientesCombo.add_item(cliente)'''
        return
    
    def forceDescon(self):
        self.access.forceDisconnect(self.clientesCombo.value)
        self.removeCliente(str(self.clientesCombo.value))
        pass

    def debugStart(self, type: int):
        if(type == 0): #Debug type SERVER
            self.writeLog('started debug with server state')
            self.srvClick()
        elif(type == 1): #Debug type CLIENT
            self.writeLog("Started debug with client state")
            self.IP.value = 'localhost'
            self.User.value = str(type)
            self.host.value = '5050'            
            self.connClick()
        elif(type == 2): #Debug type CLIENT
            self.writeLog("Started debug with client state")
            self.IP.value = 'localhost'
            self.User.value = str(type)
            self.host.value = '5050'            
            self.connClick()

    #End of class   
if __name__ == '__main__':
    from pyforms import start_app
    start_app(RafacaMsg, geometry=(300, 200, 700, 400 ))