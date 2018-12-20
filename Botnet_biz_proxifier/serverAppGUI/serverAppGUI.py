# -*- coding: utf-8 -*-

#@Botnet.biz proxifier end client server spawner GUI
#@author Tomas Keske <admin@botnet.biz>
#@since 19.12.2018


import sys
import os
import subprocess
import psutil
import time
import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget,  QPushButton, QDesktopWidget, QApplication, QLabel


class TimeThread(QThread):


    def __init__(self, timelabel, app):
        QThread.__init__(self)
        self.timelabel = timelabel
        self.app = app

    def __del__(self):
        self.wait()

    def timeElapsed(self):
        start = time.time()

        while 1:
            end = time.time()
            hours, rem = divmod(end-start, 3600)
            minutes, seconds = divmod(rem, 60)
            time.sleep(0.5)
            self.timelabel.setText("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
            self.app.processEvents()

    def run(self):
        self.timeElapsed()
        self.sleep(2)

class Spawner(QWidget):

    pids = []

    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()

    def spawnSocksProxy(self):

        pid = subprocess.Popen("proxifier_server.exe").pid
        self.pids.append(pid)

    def spawnSlaverFowarder(self):

        pid = subprocess.Popen("slaver.exe").pid
        self.pids.append(pid)

    def eliminateProccess(self):

        for pid in self.pids:

            try: 
                p = psutil.Process(pid)
                p.terminate()
            except:
                print("Proccess already terminated")

        QApplication.instance().quit
        
        
    def initUI(self):

        socksbtn = QPushButton('Start SOCKS5 PROXY Server', self)
        socksbtn.clicked.connect(self.spawnSocksProxy)
        socksbtn.resize(socksbtn.sizeHint())
        socksbtn.move(50, 50)   

        slaverbtn = QPushButton('Establish gateway connection', self)
        slaverbtn.clicked.connect(self.spawnSlaverFowarder)
        slaverbtn.resize(slaverbtn.sizeHint())
        slaverbtn.move(50, 100) 

        exitbtn = QPushButton('Terminate Servers & Application', self)
        exitbtn.clicked.connect(self.eliminateProccess)
        exitbtn.resize(exitbtn.sizeHint())
        exitbtn.move(50, 150) 

        l1 = QLabel("Čas běhu aplikace", self)
        l1.setAlignment(Qt.AlignCenter) 
        l1.resize(255, 400)  


        timelabel = QLabel("",self)
        timelabel.setAlignment(Qt.AlignCenter) 
        timelabel.resize(255,470) 

        self.get_thread = TimeThread(timelabel, self.app)
        self.get_thread.start()


        l2 = QLabel("Botnet.biz Spawner ©2018", self)
        l2.setAlignment(Qt.AlignCenter) 
        l2.resize(255, 540)     
        
        self.resize(250, 310)
        self.center()
        
        self.setWindowTitle('Botnet.biz Spawner ©2018')    
        self.show()

    
        
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Spawner(app)
    sys.exit(app.exec_())