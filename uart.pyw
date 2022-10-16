

import sys
from time import time
from PyQt5.QtWidgets import QApplication, QMainWindow,QAction, QFileDialog
from PyQt5.QtCore import QTimer,pyqtSignal,QObject
from PyQt5.QtGui import QColor,QIcon
from uart import *
#from uart_cmd import *
import serial
import serial.tools.list_ports
import threading

class uart_ui(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() & QtCore.Qt.CustomizeWindowHint)#hide min and max button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
        self.setFixedSize(self.width(), self.height())#禁止调整窗口大小
        self.setWindowTitle("uart tools v0.1.0")
        self.serial = serial.Serial()
        self.serial.timeout = 0.5   # make sure that the alive event can be checked from time to time
        self.serial.bytesize = 8
        #self.serial.stopbits = 1
        #self.serial.parity = NONE
        self.serial.rtscts = False
        self.serial.xonxoff = False


        #self.messageChanged.connect(self.WriteText)
        self.uart_update_the_baudrates()
        self.uart_update_the_port()
        #self.ui.statusbar.showMessage("connect")
        self.ui.pushButton.clicked.connect(self.uart_connect_disconnect_event)
        self.show()

    def uart_update_the_baudrates(self):
        self.ui.comboBox.clear()
        #self.baudrates = []
        preferred_index = 0
        for n, baudrate in enumerate(self.serial.BAUDRATES):
            self.ui.comboBox.addItem(str(baudrate))
            if self.serial.baudrate == baudrate:
                preferred_index = n


    def uart_update_the_port(self):
        self.ui.comboBox_2.clear()
        #self.ui.comboBox_2.addItems
        self.ports = []
        preferred_index = 0
        for n,(portname, desc, hwid) in enumerate(sorted(serial.tools.list_ports.comports())):
            self.ui.comboBox_2.addItem(u'{} - {}'.format(portname, desc))
            self.ports.append(portname)
            if self.serial.name == portname:
                preferred_index = n

    def uart_connect_disconnect_event(self):
        if(True == self.serial.is_open):
            self.StopThread()
            self.serial.close()
            self.ui.statusbar.showMessage("closed "+ u'{} - {}'.format(self.ui.comboBox_2.currentText(), 
            self.ui.comboBox.currentText()))
        else:
            self.serial.port = self.ports[self.ui.comboBox_2.currentIndex()]
            self.serial.baudrate = int(self.ui.comboBox.currentText())
            self.ui.statusbar.showMessage("connecting... "+ u'{} - {}'.format(self.ui.comboBox_2.currentText(), 
            self.ui.comboBox.currentText()))
            try:
                self.serial.open()
            except serial.SerialException as e:
                self.ui.statusbar.showMessage("connecting faild! "+ u'{} - {}'.format(self.ui.comboBox_2.currentText(), 
            self.ui.comboBox.currentText()))        
            else:
                self.ui.statusbar.showMessage("connected "+ u'{} - {}'.format(self.ui.comboBox_2.currentText(), 
            self.ui.comboBox.currentText()))   
            self.StartThread()
                   


    
    def WriteText(self, text):
        #if self.settings.unprintable:
            #text = ''.join([c if (c >= ' ' and c != '\x7f') else unichr(0x2400 + ord(c)) for c in text])
        self.ui.textBrowser_3.setText(text)

    def OnSerialRead(self, event):
        """Handle input from the serial port."""
        self.WriteText(event.data.decode('UTF-8'))






class uart_reciver(QObject):
    def __init__(self):
        self.serial = serial.Serial()
        self.serial.timeout = 0.5   # make sure that the alive event can be checked from time to time
        self.messageChanged = pyqtSignal(str)
        self.thread = None
        self.alive = threading.Event()
    
    def write_event(self, message):
        self.messageChanged.emit(message)
    
    def ComPortThread(self):
        """\
        Thread that handles the incoming traffic. Does the basic input
        transformation (newlines) and generates an SerialRxEvent
        """
        while self.alive.isSet():
            b = self.serial.read(self.serial.in_waiting or 1)
            if b:
                # newline transformation
                """
                if self.settings.newline == NEWLINE_CR:
                    b = b.replace(b'\r', b'\n')
                elif self.settings.newline == NEWLINE_LF:
                    pass
                elif self.settings.newline == NEWLINE_CRLF:
                """
                b = b.replace(b'\r\n', b'\n')
                self.write_event(b)
                #self.ui.textBrowser_3.setText(b.decode('UTF-8', 'replace'))

    def StartThread(self):
        """Start the receiver thread"""
        self.reciver = uart_reciver()
        self.reciver.messageChanged.connect(self.WriteText)
        self.thread = threading.Thread(target=self.ComPortThread)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()
        #self.thread.join()
        self.serial.rts = True
        self.serial.dtr = True
        
    def StopThread(self):
        """Stop the receiver thread, wait until it's finished."""
        if self.thread is not None:
            self.alive.clear()          # clear alive event for thread
            self.thread.join()          # wait until thread has finished
            self.thread = None






if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    w = uart_ui()
    w.show()
    sys.exit(app.exec_())