

import sys
from time import time
from PyQt5.QtWidgets import QApplication, QMainWindow,QAction, QFileDialog
from PyQt5.QtCore import QTimer,pyqtSignal,QObject
from PyQt5.QtGui import QColor,QIcon
from uart import *
#from uart_cmd import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo



class uart_ui(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() & QtCore.Qt.CustomizeWindowHint)#hide min and max button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
        self.setFixedSize(self.width(), self.height())#禁止调整窗口大小
        self.setWindowTitle("uart tools v0.1.0")
        self.serial = QSerialPort()
        self.open = False
        self.serial.readyRead.connect(self.readFromPort)

        self.dataBits = 8
        #self.dataBits.addItems(['5 bit', '6 bit', '7 bit', '8 bit'])
   
        #self._parity.addItems(['No Parity', 'Even Parity', 'Odd Parity', 'Space Parity', 'Mark Parity'])
        self._parity = 0

        #self.stopBits = QtWidgets.QComboBox(self)
        #self.stopBits.addItems(['One Stop', 'One And Half Stop', 'Two Stop'])
        self.stopBits = 0

        #self._flowControl.addItems(['No Flow Control', 'Hardware Control', 'Software Control'])
        self._flowControl = 0
        

        #self.messageChanged.connect(self.WriteText)
        self.uart_update_the_baudrates()
        self.uart_update_the_port()
        #self.ui.statusbar.showMessage("connect")
        self.ui.pushButton.clicked.connect(self.portOpen)

        self.show()

    def appendSerialText(self, appendText, color):
        self.ui.textBrowser_3.setTextColor(color)
        self.ui.textBrowser_3.insertPlainText(appendText)

    def readFromPort(self):
        data = self.serial.readAll()
        if len(data) > 0:
            self.appendSerialText( QtCore.QTextStream(data).readAll(), QtGui.QColor(255, 0, 0) )


    def portOpen(self):
        if False == self.open:
            self.serial.setBaudRate( self.baudRate() )
            self.serial.setPortName( self.portName() )
            self.serial.setDataBits( self.dataBits )
            self.serial.setParity( self._parity )
            self.serial.setStopBits( self.stopBits )
            self.serial.setFlowControl( self._flowControl )
            r = self.serial.open(QtCore.QIODevice.ReadWrite)
            if not r:
                self.ui.statusbar.showMessage('Port open error')
                self.open = False
            else:
                self.ui.statusbar.showMessage('Port opened')
                self.open = True
        else:
            self.serial.close()
            self.ui.statusbar.showMessage('Port closed')
            self.open = False


  




    def serialControlEnable(self, flag):
        self.ui.comboBox_2.setEnabled(flag)
        self.ui.comboBox.setEnabled(flag)
        
    def baudRate(self):
        return int(self.ui.comboBox.currentText())

    def portName(self):
        return self.ui.comboBox_2.currentText()

   

    def uart_update_the_baudrates(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems([
            '110', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '28800', 
            '31250', '38400', '51200', '56000', '57600', '76800', '115200', '128000', '230400', '256000', '921600'
        ])
        self.ui.comboBox.setCurrentText('115200')



    def uart_update_the_port(self):
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItems([ port.portName() for port in QSerialPortInfo().availablePorts() ])

    def WriteText(self, text):
        #if self.settings.unprintable:
            #text = ''.join([c if (c >= ' ' and c != '\x7f') else unichr(0x2400 + ord(c)) for c in text])
        self.ui.textBrowser_3.setText(text)
"""
    def uart_connect_disconnect_event(self):
        if(True == ):

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
 """                  







if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    w = uart_ui()
    w.show()
    sys.exit(app.exec_())