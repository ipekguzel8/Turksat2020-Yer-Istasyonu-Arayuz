#görüntü aktarım portu
import serial
from PyQt5.QtCore import pyqtSignal,QThread
import time
time.sleep(1)
#print(int(ilks[0]))
syc=2
class serialThreadClass(QThread):
    mesaj=pyqtSignal(str)
    def __init__(self,parent=None):
        super(serialThreadClass,self).__init__(parent)
        self.seriport=serial.Serial()
        #self.seriport.baudrate=int(ilks[0])
        self.seriport.baudrate=19200
        #self.seriport.port=str(ilks[1])
        self.seriport.port='/dev/ttyUSB0'
        self.seriport.open()
    def sendSerial(self):
        for s in range(0, syc):
            dosya = open("asdfg%s.txt" % s,"r")
            for satir in dosya:
                self.seriport.write(satir.encode())
            self.seriport.write(b'')
            self.seriport.write(b'ipek')
            self.seriport.write(b'')
        self.seriport.write(b'son')