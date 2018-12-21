# -*- coding: utf-8 -*-

#@Botnet.biz proxifier end client server spawner GUI
#@author Tomas Keske <admin@botnet.biz>
#@since 19.12.2018


import sys
import os
import subprocess
import time
import datetime
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class WorkerSignals(QObject):

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):

        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()



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

        exitbtn = QPushButton('Terminate Servers & Application')
        exitbtn.clicked.connect(self.eliminateProccess)
        exitbtn.resize(exitbtn.sizeHint())
        exitbtn.move(50, 150) 

        l1 = QLabel()
        l2 = QLabel()
        l3 = QLabel()
        l4 = QLabel()
        l5 = QLabel()
        self.l6 = QLabel()

        l1.setText("Menu:")
        l2.setText("Čas běhu aplikace:")
        l3.setText("Botnet.biz Spawner ©2018")
        l4.setText("")
        l5.setText("Author: Tomáš Keske - ver. 0.1")
        self.l6.setText("")

        l1.setAlignment(Qt.AlignCenter)
        l2.setAlignment(Qt.AlignCenter)
        l3.setAlignment(Qt.AlignCenter)
        l4.setAlignment(Qt.AlignCenter)
        l5.setAlignment(Qt.AlignCenter)
        self.l6.setAlignment(Qt.AlignCenter)
        
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
        form.addWidget(l2)
        form.addWidget(l4)
        form.addWidget(self.l6)
        form.addWidget(l4)
        form.addWidget(l4)
        form.addWidget(l5)
        form.addWidget(l3)

        self.setLayout(form)
        self.resize(250, 310)
        self.setWindowTitle('Botnet.biz Spawner ©2018') 
        self.show()

        self.threadpool = QThreadPool()
        self.timer = QTimer()
        self.startTime = time.time()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            time.sleep(1)
            progress_callback.emit(n*100/4)

        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def oh_no(self):
        
        worker = Worker(self.execute_this_fn) 
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        
        self.threadpool.start(worker)

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

    def spawnSlaverFowarder(self):

        pid = subprocess.Popen("slaver.exe")
        self.pids.append(pid)

    def eliminateProccess(self):
        for process in self.pids:
            process.terminate()
            print("proccess "+str(process.pid)+" killed")
            self.pids.pop(0)

        sys.exit()
        
if __name__ == '__main__':
    
    app = QApplication([])
    ex = Spawner()
    sys.exit(app.exec_())