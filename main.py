import os
import sys

from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlLabel
from pyforms.controls   import ControlText
from pyforms.controls   import ControlButton
from pyforms.controls   import ControlTextArea

from PyQt5.QtCore import *
from PyQt5 import QtWidgets

from sockets.client import cliente
from sockets.client import IUTypes

from SocketAccess import ClientAccess
from SocketAccess import ServerAccess

class RafacaMsg(BaseWidget):
    isConn = False
    def __init__(self, *args, **kwargs):
        super().__init__("")
        self.Title    = ControlLabel("Rafaca's messenger")
        self.mensagens = ControlTextArea('Mensagens')
        self.mensagem = ControlText('Sua mensagem')
        self.sendMsg = ControlButton('Enviar')

        self.User = ControlText("NomeUsuario: ")
        self.IP = ControlText("Endereço IP: ")
        self.host = ControlText("Porta do servidor: ")
        self.conn = ControlButton("Conectar")
        self.srv = ControlButton("Iniciar servidor")
        self.Errors = ControlTextArea("")
        
        self.Errors.enabled = False
        self.mensagens.enabled = False

        self.sendMsg.value = self.sendMsgClick
        self.conn.value = self.connClick
        self.srv.value = self.srvClick

        self._formset = [ 
            (' ', 'Title', ' '),
            {
                'Tab1:Conexao': [('User'), ('IP', 'host', 'conn'), (' ', 'srv', ' '), ('Errors'), ' '],
                'Tab2:Mensagens': ['mensagens', ('mensagem', 'sendMsg'), ' ']
            }
        ]
        #For debug
        if(len(sys.argv > 1)):
            if(sys.argv[1].upper() == 'client' or sys.argv[1].upper() == '1'):
                debugStart(1)
            elif(sys.argv[1].upper() == 'server' or sys.argv[1].upper() == '0'):
                debugStart(0)
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
            self.writeLog('Desconecte-se antes de tentar conectar novamente.')
        if(self.ValidateConnInputs() == False):
            return
        self.access = ClientAccess(self.IP.value, int(self.host.value), self.User.value, IUTypes.PyForms, self)
        if(self.access.ConnectStart() == True):
            self.isConn = True
            self.writeLog('Conectado em: ' + self.IP.value + ':' + self.host.value)
            self.disableConnInputs()
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
            self.disableConnInputs()
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

    def disableConnInputs(self):
        self.IP.enabled = False
        self.host.enabled = False
        self.User.enabled = False
        self.conn.enabled = False
        self.srv.enabled = False
    
    def saveMsg(self):
        self.writeMsg("[Você]: " + self.mensagem.value)
        self.mensagem.value = ''

    @pyqtSlot(str)
    def writeLog(self, value):
        self.Errors.enabled = True
        self.Errors.value += '\n[Log]: ' + value
        self.Errors.enabled = False
    @pyqtSlot(str)
    def writeMsg(self, value):
        self.mensagens.enabled = True
        self.mensagens.value += '\n' + value
        self.mensagens.enabled = False
    
    def debugStart(self, type: int):
        if(type == 0): #Debug type SERVER
            self.writeLog('started debug with server state')
            self.srvClick()
        elif(type == 1): #Debug type CLIENT
            self.writeLog("Started debug with client state")
            self.IP.value = 'localhost'
            self.User.value = 'Tester'
            self.host.value = '5050'            
            self.connClick()

if __name__ == '__main__':
    from pyforms import start_app
    start_app(RafacaMsg, geometry=(300, 200, 700, 400 ))
