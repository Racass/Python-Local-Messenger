import os

from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlLabel
from pyforms.controls   import ControlText
from pyforms.controls   import ControlButton
from pyforms.controls   import ControlTextArea

from PyQt5.QtCore import *
from PyQt5 import QtWidgets

from sockets.client import cliente

class RafacaMsg(BaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__("")
        #Definition of the forms fields
        self.Title    = ControlLabel("Rafaca's messenger")
        self.mensagens = ControlTextArea('Mensagens')
        self.mensagem = ControlText('Sua mensagem')
        self.sendMsg = ControlButton('Enviar')

        self.User = ControlText("NomeUsuario: ")
        self.IP = ControlText("Endereço IP: ")
        self.host = ControlText("Porta do servidor: ")
        self.conn = ControlButton("Conectar")
        self.Errors = ControlTextArea("")
        
        self.Errors.enabled = False
        self.mensagens.enabled = False

        self.sendMsg.value = self.sendMsgClick
        self.conn.value = self.connClick

        self._formset = [ 
            (' ', 'Title', ' '),
            {
                'Conexao': [('User'), ('IP', 'host', 'conn'), ('Errors'), ' '],
                'Mensagens': ['mensagens', ('mensagem', 'sendMsg'), ' ']
            }
        ]
    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return):
            if(self._tabs[0].currentIndex() == 0):
                self.conn.click()
            elif(self._tabs[0].currentIndex() == 1):
                self.sendMsg.click()
        event.accept()
    def sendMsgClick(self):
        self.cli.sendMsg(self.mensagem.value)
        self.mensagens.value += "\n[Você]: " + self.mensagem.value
        self.mensagem.value = ''
        pass
    def connClick(self):
        print("Conexão chamada")

        if(self.IP.value == ''):
            self.Errors.value += '\nFavor colocar um endereço IP!'
            return
        elif(self.host.value == ''):
            self.Errors.value += '\nFavor colocar uma porta!'
            return
        elif(self.User.value == ''):
            self.Errors.value += '\nFavor colocar um usuario!'
            return

        self.cli = cliente(self.IP.value, int(self.host.value), self.User.value, self)
        self.Errors.value += '\nConectado em: ' + self.IP.value + ':' + self.host.value
        pass
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
        
if __name__ == '__main__':
    from pyforms import start_app
    start_app(RafacaMsg)
