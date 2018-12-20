# -*- coding: utf-8 -*-

#@Botnet.biz proxifier end client server spawner GUI
#@author Tomas Keske <admin@botnet.biz>
#@since 19.12.2018


import sys
import os
import subprocess
from PyQt5.QtWidgets import QWidget,  QPushButton, QDesktopWidget, QApplication


class Spawner(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def spawnSocksProxy(self):

        pid = subprocess.Popen("proxifier_server.exe").pid

    def spawnSlaverFowarder(self):

        pid = subprocess.Popen("slaver.exe").pid
    
        
        
    def initUI(self):

        socksbtn = QPushButton('Start SOCKS5 PROXY Server', self)
        socksbtn.clicked.connect(self.spawnSocksProxy)
        socksbtn.resize(socksbtn.sizeHint())
        socksbtn.move(50, 50)   

        slaverbtn = QPushButton('Establish gateway connection', self)
        slaverbtn.clicked.connect(self.spawnSlaverFowarder)
        slaverbtn.resize(slaverbtn.sizeHint())
        slaverbtn.move(50, 100) 

        minbtn = QPushButton('Minimize to system tray', self)
        minbtn.clicked.connect(QApplication.instance().quit)
        minbtn.resize(minbtn.sizeHint())
        minbtn.move(50, 150)       

        exitbtn = QPushButton('Terminate Server & Application', self)
        exitbtn.clicked.connect(QApplication.instance().quit)
        exitbtn.resize(exitbtn.sizeHint())
        exitbtn.move(50, 200)              
        
        self.resize(300, 300)
        self.center()
        
        self.setWindowTitle('Botnet.biz Spawner')    
        self.show()

    
        
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Spawner()
    sys.exit(app.exec_())