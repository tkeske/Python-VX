# -*- coding: utf-8 -*-

#@Botnet.biz proxifier end client server spawner GUI
#@author Tomas Keske <admin@botnet.biz>
#@since 19.12.2018


import sys
import os
import subprocess
import time
import datetime
import psutil
import urllib.request
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

cpLocation = "http://ports.botnet.biz/"

class Spawner(QWidget):

    def __init__(self, *args, **kwargs):
        super(Spawner, self).__init__(*args, **kwargs)

        self.counter = 0

        socksbtn = QPushButton('Start SOCKS5 PROXY Server')
        socksbtn.clicked.connect(self.spawnSocksProxy)
        socksbtn.resize(socksbtn.sizeHint())
        socksbtn.move(50, 50)

        slaverbtn = QPushButton('Establish gateway connection')
        slaverbtn.clicked.connect(self.spawnSlaverFowarder)
        slaverbtn.resize(slaverbtn.sizeHint())
        slaverbtn.move(50, 100)

        exitbtn = QPushButton('Terminate entire Application')
        exitbtn.clicked.connect(self.eliminateProccess)
        exitbtn.resize(exitbtn.sizeHint())
        exitbtn.move(50, 150) 

        l1 = QLabel()
        l2 = QLabel()
        l3 = QLabel()
        l4 = QLabel()
        l5 = QLabel()
        self.l6 = QLabel()
        self.l7 = QLabel()
        self.l8 = QLabel()

        l1.setText("Menu:")
        l2.setText("Čas běhu aplikace:")
        l3.setText("Botnet.biz Spawner ©2018")
        l4.setText("")
        l5.setText("Author: Tomáš Keske - ver. 0.1")
        self.l6.setText("")
        self.l7.setText("SOCKS server: Offline")
        self.l7.setStyleSheet("color: red")
        self.l8.setText("Gateway connection: Offline")
        self.l8.setStyleSheet("color: red")

        l1.setAlignment(Qt.AlignCenter)
        l2.setAlignment(Qt.AlignCenter)
        l3.setAlignment(Qt.AlignCenter)
        l4.setAlignment(Qt.AlignCenter)
        l5.setAlignment(Qt.AlignCenter)
        self.l6.setAlignment(Qt.AlignCenter)
        self.l7.setAlignment(Qt.AlignCenter)
        self.l8.setAlignment(Qt.AlignCenter)

        form = QFormLayout()
       
        form.addRow(l1)
        form.addRow(l4)
        form.addWidget(socksbtn)
        form.addWidget(l4)
        form.addWidget(slaverbtn)
        form.addWidget(l4)
        form.addWidget(exitbtn)
        form.addWidget(l4)
        form.addWidget(l4)
        form.addWidget(self.l7)
        form.addWidget(l4)
        form.addWidget(self.l8)
        form.addWidget(l4)
        form.addWidget(l2)
        form.addWidget(l4)
        form.addWidget(self.l6)
        form.addWidget(l4)
        form.addWidget(l4)
        form.addWidget(l5)
        form.addWidget(l3)

        self.setLayout(form)
        self.resize(250, 350)
        self.setWindowTitle('Botnet.biz Spawner ©2018') 
        self.show()

        
        self.timer = QTimer()
        self.startTime = time.time()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

        
        self.timer2 = QTimer()
        self.timer2.setInterval(20000)
        self.timer2.timeout.connect(self.report_state)
        self.timer2.start()


 
    def isProcessRunning(self, processName):

        for proc in psutil.process_iter():
            try:
                if processName.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False;

    def amIFullyOnline(self):
        if (self.isProcessRunning("slaver.exe") == True and
         self.isProcessRunning("proxifier_server.exe") == True):
            return True

    def report_state(self):

        if self.amIFullyOnline():
            urllib.request.urlopen("http://ports.botnet.biz/index.php?status=online").read()


    def recurring_timer(self):

        start = self.startTime
        end = time.time()
        hours, rem = divmod(end-start, 3600)
        minutes, seconds = divmod(rem, 60)
  
        self.l6.setText("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

    pids = []

    def spawnSocksProxy(self):

        pid = subprocess.Popen("proxifier_server.exe")
        self.pids.append(pid)
        self.l7.setStyleSheet("color: green")
        self.l7.setText("SOCKS server: Online!!!")

    def spawnSlaverFowarder(self):

        pid = subprocess.Popen("slaver.exe")
        self.pids.append(pid)
        self.l8.setStyleSheet("color: green")
        self.l8.setText("Gateway connection: Online!!!")

    def eliminateProccess(self):
        for process in self.pids:
            process.terminate()
            print("proccess "+str(process.pid)+" killed")
            self.pids.pop(0)

        closeRequest = urllib.request.urlopen(cpLocation+"index.php?status=offline").read()
        sys.exit()

    def closeEvent(self, event):

        closeRequest = urllib.request.urlopen(cpLocation+"index.php?status=offline").read()
        event.accept()
                
if __name__ == '__main__':
    
    app = QApplication([])
    ex = Spawner()
    sys.exit(app.exec_())