import serial
import matplotlib.pyplot as plt
import os
from PyQt5 import QtWidgets, QtCore, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import pyqtgraph.exporters
import numpy as np
import sys
import vtk
from qtpy.QtGui import QPainter, QColor, QPen, QBrush, QPixmap
from qtpy.QtWidgets import QMainWindow, QGraphicsView, QGraphicsItem, QGraphicsSimpleTextItem, QApplication
from pytilemap import MapGraphicsView, MapTileSourceHere, MapTileSourceOSM
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import glob
from PyQt5.QtCore import Qt,QThread, pyqtSignal
import requests
import json
from PyQt5.QtWidgets import (QApplication, QDialog, QProgressBar, QPushButton)
from tkinter import *
from tkinter import filedialog
import cv2
import qimage2ndarray
import csv
import base64
from PIL import Image
from binascii import hexlify
from subprocess import call
import math
import _thread
from serialThreadFile import serialThreadClass
misst=list()
ser = serial.Serial(bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
camera_index=2
fps=30
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('kamera_kaydi.avi',fourcc, 30.0, (640,480))

class Pencere(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kalibredurumu=0
        self.stopflag =False
        self.dosya_yol=''
        self.resize(1926, 1006)
        self.frame_gl=QFrame()    
        opengl=QOpenGLWidget(parent=self.frame_gl)
        self.setWindowIcon(QIcon("logo1.png"))
        self.setAutoFillBackground(True)      
        oImage=QImage("ekran8.png")
        sImage=oImage.scaled(QSize(1926, 1020))
        palette=QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)
        self.bosluk=QLabel("    ")
        self.genelhbox=QHBoxLayout()
        self.firstvb=QVBoxLayout()
        self.logo=QLabel()
        self.motorkontrolu = QGroupBox("Manuel Tahrik Komutu")
        self.motorbasla=QPushButton("BAŞLA")
        self.motordur=QPushButton("DUR")
        self.motorbasla.setFixedHeight(27)
        self.motordur.setFixedHeight(27)
        self.motorbasla.clicked.connect(self.motorBasla)
        self.motordur.clicked.connect(self.motorDur)
        self.motor=QVBoxLayout()
        self.motor.addWidget(self.motorbasla)
        self.motor.addWidget(self.motordur)
        self.motorkontrolu.setLayout(self.motor)
        self.splitter8 = QSplitter()
        self.splitter8.setOrientation(Qt.Vertical)
        self.logo.setFixedHeight(150)
        self.logo.setFixedWidth(190)
        self.logo.setPixmap(QPixmap("logo4.PNG"))        
        self.logo.setAlignment(Qt.AlignTop)
        self.takimno=QLabel("Takım No:56701")
        self.takimno.setFont(QFont("Comic Sans MS",11,QFont.Bold))
        self.hata1=0
        self.portyap=QHBoxLayout()
        scene2 = QGraphicsScene(self)
        self.gpslongitude=[33.7115]
        self.gpslatitude=[38.3980]
        try:
            self.capture = cv2.VideoCapture(camera_index)
            self.dimensions = self.capture.read()[1].shape[1::-1]
            pixmap2 = QPixmap(*self.dimensions)
            self.pixmapItem2 = scene2.addPixmap(pixmap2) 
        except AttributeError:
            self.hata1=1
        self.view2 = QGraphicsView(self)
        self.view2.setScene(scene2)
        self.view2.setFixedHeight(430)
        self.view2.setFixedWidth(335)
        self.view3 = MapGraphicsView(tileSource=MapTileSourceHere()) #tileSource=MapTileSourceOSM("map.osm")
        self.view3.scene().setCenter(self.gpslongitude[0], self.gpslatitude[0])
        self.view3.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        self.view3.setRenderHint(QPainter.Antialiasing, True)
        self.view3.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.z=0
        self.y=0
        self.frame=QFrame()
        self.resize(1926, 1006)
        self.view3.setFixedWidth(335)
        self.view3.setFixedHeight(407)
        self.twovb=QVBoxLayout()
        self.view3.setStyleSheet("border:1px solid #000000")
        self.threevb=QVBoxLayout()
        self.threevbh=QHBoxLayout()
        self.threevbh.addWidget(self.logo) 
        self.threevbh.addWidget(self.takimno)
        self.firstvb.addLayout(self.threevbh)
        self.firstvb.addWidget(self.view2)
        self.tableWidget3=QTableWidget()
        self.tableWidget3.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget3.setColumnCount(17)
        self.tableWidget3.setHorizontalHeaderLabels(str("TAKIM NO;PAKET NUMARASI;GÖNDERME SAATİ;BASINÇ;YÜKSEKLİK;İNİŞ HIZI;SICAKLIK;PİL GERİLİMİ;GPS LATITUDE;GPS LONGITUDE;GPS ALTITUDE;UYDU STATÜSÜ;PITCH;ROLL;YAW;DÖNÜŞ SAYISI;VİDEO AKTARIM BİLGİSİ").split(";"))
        self.tableWidget3.verticalHeader().hide()
        self.tableWidget3.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableWidget3.horizontalScrollBar().hide()
        self.tableWidget3.setStyleSheet("font:9px;")
        self.tableWidget3.setColumnWidth(0,59)
        self.tableWidget3.setColumnWidth(1,98)
        self.tableWidget3.setColumnWidth(2,95)
        self.tableWidget3.setColumnWidth(3,45)
        self.tableWidget3.setColumnWidth(4,60)
        self.tableWidget3.setColumnWidth(5,53)
        self.tableWidget3.setColumnWidth(6,51)
        self.tableWidget3.setColumnWidth(7,71)
        self.tableWidget3.setColumnWidth(8,77)
        self.tableWidget3.setColumnWidth(9,89)
        self.tableWidget3.setColumnWidth(10,77)
        self.tableWidget3.setColumnWidth(11,84)
        self.tableWidget3.setColumnWidth(12,38)
        self.tableWidget3.setColumnWidth(13,32)
        self.tableWidget3.setColumnWidth(14,31)
        self.tableWidget3.setColumnWidth(15,80)
        self.tableWidget3.setColumnWidth(16,151)
        self.splitter10 = QSplitter()
        self.splitter10.setOrientation(Qt.Vertical)
        self.twovbhb1=QHBoxLayout()
        self.twovbhb12=QHBoxLayout()
        self.twovbhb13=QHBoxLayout()
        self.twovbhb14=QHBoxLayout()
        self.twovbhb15=QHBoxLayout()
        self.twovbhb16=QHBoxLayout()
        self.twovbvb1=QVBoxLayout()
        self.twovbhb2=QHBoxLayout()
        self.twovbhb3=QHBoxLayout()
        self.twovbvb2=QVBoxLayout()
        self.uydu_statu=["Görev Başladı","Uçuş Bekleniyor","Model Uydu Yükselmekte","Model Uydu İnişte","Görev Yükü Taşıyıcıdan Ayrıldı","Görev Yükü Kurtarılmayı Bekliyor","Görev Tamamlandı"]
        self.port=QLabel("Port:")
        self.port2=QLabel("Port:")
        self.port.setFixedWidth(50)
        
        self.port.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.ports=QComboBox()
        self.ports.setFixedWidth(150)
        self.ports.addItems([''])
        self.ports.addItems(self.portlar())
        self.ports.setStyleSheet("font: bold 15px;")
        self.groupbox2 = QGroupBox("1. Seri Port Yapılandırması")     
        self.groupbox1 = QGroupBox("Ayrılma Yüksekliği Değiştirme") 
        self.groupbox5 = QGroupBox("2. Seri Port Yapılandırması")
        self.yukseklikQHB=QHBoxLayout()        
        self.yukseklikd=QLabel("Ayrılma Yüksekliğini Giriniz:")
        self.yukseklikd.setFixedWidth(240)
        self.yukseklik=QLineEdit()
        self.yukseklikgonder=QPushButton("GÖNDER")
        self.yukseklikgonder.clicked.connect(self.yukseklikGonder)
        self.yukseklikQHB.addWidget(self.yukseklikd)
        self.yukseklikQHB.addWidget(self.yukseklik)
        self.yukseklikQHB.addWidget(self.yukseklikgonder)
        self.groupbox1.setLayout(self.yukseklikQHB)
        self.start=QPushButton("BAŞLA")
        self.start.setFont(QFont("Comic Sans MS",9,))
        self.start.clicked.connect(self.Start)
        self.start.setInputMethodHints(Qt.ImhNone)
        
        self.baudrates=QLabel("Baudrate:")
        self.baudrates.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.baudrate=QComboBox()
        self.baudrate.setFixedWidth(100)
        self.baudrate.addItems(["","9600","19200","115200", "38400"])
        self.baudrate.setStyleSheet("font: bold 15px;")
        self.baudrates.setFixedWidth(80)
        
        self.port2.setFixedWidth(50)
        self.port2.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.ports2=QComboBox()
        self.ports2.setFixedWidth(150)
        self.ports2.addItems([''])
        self.ports2.addItems(self.portlar())
        self.ports2.setStyleSheet("font: bold 15px;")
        self.groupbox11 = QGroupBox("Seri Port Yapılandırması")        
        self.start2=QPushButton("BAŞLA")
        self.start2.setFont(QFont("Comic Sans MS",9,))
        self.start2.clicked.connect(self.Start2)
        self.baudrates2=QLabel("Baudrate:")
        self.baudrates2.setFont(QFont("Comic Sans MS",10,QFont.Bold))
        self.baudrate2=QComboBox()
        self.baudrate2.setFixedWidth(100)
        self.baudrate2.addItems(["","9600","19200","115200", "38400"])
        self.baudrate2.setStyleSheet("font: bold 15px;")
        self.baudrates2.setFixedWidth(80)
        
        self.gerial=QPushButton("GERİ AL")
        self.gerial.setFixedHeight(27)
        self.twovbhb15.addWidget(self.gerial)
        self.kalibrasyon=QPushButton("KALİBRE ET")
        self.kalibrasyon.setFixedHeight(27)
        self.kalibrasyon.setFixedWidth(85)
        self.kalibrasyon.clicked.connect(self.KalibrEt)
        self.ayarlar=QVBoxLayout()
        self.diger_ayarlar_ac=QPushButton("AÇ")
        self.diger_ayarlar_kapat=QPushButton("KAPAT")
        self.diger_ayarlar_ac.setFixedHeight(27)
        self.diger_ayarlar_kapat.setFixedHeight(27)
        self.ayarlar.addWidget(self.diger_ayarlar_ac)
        self.ayarlar.addWidget(self.diger_ayarlar_kapat)
        self.diger_ayarlar_ac.clicked.connect(self.ayarlarAc)
        self.diger_ayarlar_kapat.clicked.connect(self.ayarlarKapat)
        self.gerial.clicked.connect(self.geriAl)
        self.iletimdurumu=QLabel("Video İletim Durumu:")
        self.ayırma=QPushButton("AYIR")
        self.ayırma.clicked.connect(self.Ayir)
        self.kalibrasyon.setFont(QFont("Comic Sans MS",9))
        self.ayırma.setFixedWidth(85)
        self.ayırma.setFixedHeight(27)
        self.gerial.setFixedWidth(113)
        self.groupbox4 = QGroupBox("Ayrılma Komutu")
        self.groupbox10 = QGroupBox("Ayarlar")
        self.groupbox8 = QGroupBox("Kalibrasyon Komutu")
        self.groupbox3 = QGroupBox("Verileri Arayüze Geri Alma Komutu")
        self.groupbox10.setLayout(self.ayarlar)
        self.groupbox8.setLayout(self.twovbhb16)
        self.groupbox3.setLayout(self.twovbhb15)
        self.twovbhb14.addWidget(self.ayırma)
        self.twovbhb16.addWidget(self.kalibrasyon)
        self.groupbox4.setLayout(self.twovbhb14)
        self.ayırma.setFont(QFont("Comic Sans MS",9))
        self.gerial.setFont(QFont("Comic Sans MS",9))
        self.packetcount=QLabel("Paket Numarası:")
        self.packetcount2=QLabel()
        self.packetcount.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.packetcount2.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.packetcount.setFixedWidth(137)
        self.missiontime=QLabel("Gönderme Saati:")
        self.missiontime2=QLabel()
        self.missiontime2.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.missiontime.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.missiontime.setFixedWidth(157)
        self.start.setInputMethodHints(Qt.ImhNone)
        self.dosyasecs=QLabel("Dosya Seç:")
        self.dosyasecs.setFixedHeight(20)
        self.dosyasecs.setFixedWidth(90)
        self.dosyasecs.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.dosyasec=QPushButton("...")
        self.dosyasec.setFixedHeight(27)
        self.dosyasec.clicked.connect(self.Dosyasec)
        self.stop=QPushButton("DUR")
        self.stop.setInputMethodHints(Qt.ImhNone)
        self.stop.clicked.connect(self.Stop)
        self.stop.setFont(QFont("Comic Sans MS",9))
        
        self.stop2=QPushButton("DUR")
        self.stop2.setInputMethodHints(Qt.ImhNone)
        self.stop2.clicked.connect(self.Stop2)
        self.stop2.setFont(QFont("Comic Sans MS",9))
        
        self.dosyasec.setFixedHeight(20)
        self.dosyasec.setFixedWidth(20)
        self.gonder=QPushButton("GÖNDER")
        self.gonder.setFixedHeight(27)
        self.gonder.setDisabled(True)
        self.gonder.setFixedWidth(110)
        self.gonder.setFont(QFont("Comic Sans MS",9,))
        self.groupbox = QGroupBox("Video Aktarımı")
        self.iletimdurumu.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.gbvx=QVBoxLayout()
        self.gbx=QHBoxLayout()
        self.gbx.addWidget(self.dosyasecs)
        self.gbx.addWidget(self.dosyasec)
        self.gbx.addWidget(self.gonder)
        self.gbvx.addLayout(self.gbx)
        self.gbvx.addWidget(self.iletimdurumu)
        self.groupbox.setLayout(self.gbvx) 
        self.gonder.clicked.connect(self.Gonder)
        self.twovbhb18=QHBoxLayout()
        self.twovbhb18.addWidget(self.port2)
        self.twovbhb18.addWidget(self.ports2)
        self.twovbhb18.addWidget(self.baudrates2)
        self.twovbhb18.addWidget(self.baudrate2)
        
        self.twovbhb19=QHBoxLayout()
        self.twovbhb19.addWidget(self.start2)
        self.twovbhb19.addWidget(self.stop2)
        
        self.twovbhb13.addWidget(self.port)
        self.twovbhb13.addWidget(self.ports)
        self.twovbhb13.addWidget(self.baudrates)
        self.twovbhb13.addWidget(self.baudrate)
        self.twovbhb12.addWidget(self.start)
        self.twovbhb12.addWidget(self.stop)
        self.twovbvb1.addLayout(self.twovbhb13)
        self.twovbvb1.addLayout(self.twovbhb12)
        self.twovbvb2.addLayout(self.twovbhb18)
        self.twovbvb2.addLayout(self.twovbhb19)
        self.groupbox2.setLayout(self.twovbvb1)
        self.groupbox5.setLayout(self.twovbvb2)
        self.portyap.addWidget(self.groupbox2)  
        self.portyap.addWidget(self.groupbox5)
        self.groupbox11.setLayout(self.portyap)
        self.splitter10.addWidget(self.groupbox11)
        self.splitter10.addWidget(self.groupbox1)
        self.twovbhb1.addWidget(self.groupbox4)
        self.twovbhb1.addWidget(self.groupbox10)
        self.twovbhb1.addWidget(self.motorkontrolu)
        self.twovbhb1.addWidget(self.groupbox3)
        self.twovbhb1.addWidget(self.groupbox8)
        self.twovbhb1.addWidget(self.groupbox)
        scene = QGraphicsScene(self)
        try:
            pixmap = QPixmap(*self.dimensions)
            self.pixmapItem = scene.addPixmap(pixmap)
        except AttributeError:
            print('devam')
        view = QGraphicsView(self)
        view.setScene(scene)
        if self.hata1==0:
            timer = QTimer(self)
            timer.setInterval(int(1000/fps))
            timer.timeout.connect(self.get_frame)
            timer.start()
        self.temp=[]
        self.pressure=list()
        self.voltage=list()
        self.altitude=list()
        self.inishiz=list()
        self.gpsaltitude=list()
        self.timer=list()
        self.tableWidget2=QTableWidget()
        self.tableWidget2.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget2.setColumnCount(17)   
        self.tableWidget2.setHorizontalHeaderLabels(str("TAKIM NO;PAKET NUMARASI;GÖNDERME SAATİ;BASINÇ;YÜKSEKLİK;İNİŞ HIZI;SICAKLIK;PİL GERİLİMİ;GPS LATITUDE;GPS LONGITUDE;GPS ALTITUDE;UYDU STATÜSÜ;PITCH;ROLL;YAW;DÖNÜŞ SAYISI;VİDEO AKTARIM BİLGİSİ").split(";"))
        self.tableWidget2.verticalHeader().hide()
        self.tableWidget2.horizontalHeader().setStyleSheet("font: bold 7px;")
        self.tableWidget2.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableWidget2.horizontalScrollBar().hide()
        self.tableWidget2.setStyleSheet("font:9px;")
        self.tableWidget2.setColumnWidth(0,59)
        self.tableWidget2.setColumnWidth(1,98)
        self.tableWidget2.setColumnWidth(2,97)
        self.tableWidget2.setColumnWidth(3,49)
        self.tableWidget2.setColumnWidth(4,61)
        self.tableWidget2.setColumnWidth(5,52)
        self.tableWidget2.setColumnWidth(6,52)
        self.tableWidget2.setColumnWidth(7,70)
        self.tableWidget2.setColumnWidth(8,80)
        self.tableWidget2.setColumnWidth(9,90)
        self.tableWidget2.setColumnWidth(10,77)
        self.tableWidget2.setColumnWidth(11,85)
        self.tableWidget2.setColumnWidth(12,38)
        self.tableWidget2.setColumnWidth(13,34)
        self.tableWidget2.setColumnWidth(14,33)
        self.tableWidget2.setColumnWidth(15,81)
        self.tableWidget2.setColumnWidth(16,134)
        self.tableWidget2.horizontalHeader().setStyleSheet("font: bold 9px;")
        self.tableWidget2.setFixedHeight(195)
        self.tableWidget=QTableWidget()
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setColumnCount(17)
        self.tableWidget.setHorizontalHeaderLabels(str("TAKIM NO;PAKET NUMARASI;GÖNDERME SAATİ;BASINÇ;YÜKSEKLİK;İNİŞ HIZI;SICAKLIK;PİL GERİLİMİ;GPS LATITUDE;GPS LONGITUDE;GPS ALTITUDE;UYDU STATÜSÜ;PITCH;ROLL;YAW;DÖNÜŞ SAYISI;VİDEO AKTARIM BİLGİSİ").split(";"))
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableWidget.horizontalScrollBar().hide()
        self.tableWidget.setStyleSheet("font:9px;")
        self.tableWidget.setColumnWidth(0,59)
        self.tableWidget.setColumnWidth(1,98)
        self.tableWidget.setColumnWidth(2,95)
        self.tableWidget.setColumnWidth(3,45)
        self.tableWidget.setColumnWidth(4,60)
        self.tableWidget.setColumnWidth(5,53)
        self.tableWidget.setColumnWidth(6,51)
        self.tableWidget.setColumnWidth(7,71)
        self.tableWidget.setColumnWidth(8,77)
        self.tableWidget.setColumnWidth(9,89)
        self.tableWidget.setColumnWidth(10,77)
        self.tableWidget.setColumnWidth(11,84)
        self.tableWidget.setColumnWidth(12,38)
        self.tableWidget.setColumnWidth(13,32)
        self.tableWidget.setColumnWidth(14,31)
        self.tableWidget.setColumnWidth(15,80)
        self.tableWidget.setColumnWidth(16,151)
        self.tableWidget.horizontalHeader().setStyleSheet("font: bold 9px;")
        self.splitter1 = QSplitter()
        self.splitter1.setOrientation(Qt.Vertical)
        self.splitter2 = QSplitter()
        self.splitter2.setOrientation(Qt.Horizontal)
        self.ayarlarbolum=QVBoxLayout()
        self.ayarlarbolum.addWidget(self.groupbox11)
        self.splitter3 = QSplitter()
        self.splitter3.setOrientation(Qt.Horizontal)
        self.splitter4 = QSplitter()
        self.splitter4.setOrientation(Qt.Horizontal)
        self.dates2=[]
        self.brush = pg.mkBrush(color=(128,128,128))
        self.axis = DateAxis(orientation='bottom')
        self.axis2 = DateAxis(orientation='bottom')
        self.axis3 = DateAxis(orientation='bottom')
        self.axis4 = DateAxis(orientation='bottom')
        self.axis5 = DateAxis(orientation='bottom')
        self.axis6 = DateAxis(orientation='bottom')
        self.pw = pg.PlotWidget(axisItems={'bottom': self.axis},  title="PlotItem")
        self.pw2 = pg.PlotWidget(axisItems={'bottom': self.axis2},  title="PlotItem")
        self.pw3 = pg.PlotWidget(axisItems={'bottom': self.axis3}, title="PlotItem")
        self.pw4 = pg.PlotWidget(axisItems={'bottom': self.axis4}, title="PlotItem")
        self.pw5 = pg.PlotWidget(axisItems={'bottom': self.axis5},  title="PlotItem")
        self.pw6 = pg.PlotWidget(axisItems={'bottom': self.axis6},  title="PlotItem")
        self.pen = pg.mkPen(color=(0, 0, 0))
        self.pw.setBackground('w')
        self.pw.setTitle('<span style=\"color:black;font-size:17px\">YÜKSEKLİK(m)</span>')
        self.pw.setLabel('left', '<span style=\"color:black;font-size:17px\">m</span>')
        self.pw.setLabel('bottom', '<span style=\"color:black;font-size:17px\">Gönderme Saati(h:min:s)</span>')
        self.data_line =  self.pw.plot(self.dates2, self.altitude,pen=self.pen,symbol='o', symbolSize=10, symbolBrush=(self.brush))
        self.pw2.setBackground('w')
        self.pw2.setTitle('<span style=\"color:black;font-size:17px\">SICAKLIK(°C)</span>')
        self.pw2.setLabel('left', '<span style=\"color:black;font-size:17px\">°C</span>')
        self.pw2.setLabel('bottom', '<span style=\"color:black;font-size:17px\">Gönderme Saati(h:min:s)</span>')
        self.data_line2 =  self.pw2.plot(self.dates2, self.temp,pen=self.pen,symbol='o', symbolSize=10, symbolBrush=(self.brush))
        self.pw3.setBackground('w')
        self.pw3.setTitle('<span style=\"color:black;font-size:17px\">BASINÇ(Pa)</span>')
        self.pw3.setLabel('left', '<span style=\"color:black;font-size:17px\">Pa</span>')
        self.pw3.setLabel('bottom', '<span style=\"color:black;font-size:17px\">Gönderme Saati(h:min:s)</span>')
        self.data_line3 =  self.pw3.plot(self.dates2, self.pressure,pen=self.pen,symbol='o', symbolSize=10, symbolBrush=(self.brush))
        self.pw4.setBackground('w')
        self.pw4.setTitle('<span style=\"color:black;font-size:17px\">PİL GERİLİMİ(V)</span>')
        self.pw4.setLabel('left', '<span style=\"color:black;font-size:17px\">V</span>')
        self.pw4.setLabel('bottom', '<span style=\"color:black;font-size:17px\">Gönderme Saati(h:min:s)</span>')
        self.data_line4 =  self.pw4.plot(self.dates2, self.voltage,pen=self.pen,symbol='o', symbolSize=10, symbolBrush=(self.brush))
        self.pw5.setBackground('w')
        self.pw5.setTitle('<span style=\"color:black;font-size:17px\">İNİŞ HIZI(m/s)</span>')
        self.pw5.setLabel('left', '<span style=\"color:black;font-size:17px\">m/s</span>')
        self.pw5.setLabel('bottom', '<span style=\"color:black;font-size:17px\">Gönderme Saati(h:min:s)</span>')
        self.data_line5 =  self.pw5.plot(self.dates2, self.gpsaltitude,pen=self.pen,symbol='o', symbolSize=10, symbolBrush=(self.brush))
        self.pw6.setBackground('w')
        self.pw6.setTitle('<span style=\"color:black;font-size:17px\">GPS ALTITUDE(m)</span>')
        self.pw6.setLabel('left','<span style=\"color:black;font-size:17px\">m</span>')
        self.pw6.setLabel('bottom', '<span style=\"color:black;font-size:17px\">Gönderme Saati(h:min:s)</span>')
        self.data_line6 =  self.pw6.plot(self.dates2, self.inishiz,pen=self.pen,symbol='o', symbolSize=10, symbolBrush=(self.brush))
        self.splitter3.addWidget(self.pw)
        self.splitter3.addWidget(self.pw2)
        self.splitter3.addWidget(self.pw3)
        self.splitter2.addWidget(self.pw4)
        self.splitter2.addWidget(self.pw5)
        self.splitter2.addWidget(self.pw6)
        self.splitter1.addWidget(self.splitter3)
        self.splitter1.addWidget(self.splitter2)
        self.splitter4.addWidget(self.tableWidget2)
        self.splitter1.addWidget(self.splitter4)
        self.kamera2=QLabel()
        self.splitter8.addWidget(self.kamera2)
        layout = QGridLayout()
        self.view5 = MapGraphicsView(tileSource=MapTileSourceHere()) #tileSource=MapTileSourceOSM("map.osm")
        self.view5.scene().setCenter(self.gpslongitude[0], self.gpslatitude[0])
        self.view5.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        self.view5.setRenderHint(QPainter.Antialiasing, True)
        self.view5.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.tabwidget = QTabWidget()
        self.capture4 = cv2.VideoCapture()
        self.kamera3=QLabel()
        self.tabwidget.addTab(self.splitter1, "GRAFİKLER")
        self.tabwidget.addTab(self.tableWidget, "TELEMETRİ VERİLERİ")
        self.tabwidget.addTab(self.view5, "HARİTA")
        self.tabwidget.addTab(view, "KAMERA KAYDI")        
        self.tabwidget.setStyleSheet("font: bold 14px;")
        layout.addWidget(self.tabwidget, 0, 0) 
        self.tabwidget.blockSignals(False)
        self.twovbhb3.addWidget(self.packetcount)
        self.twovbhb3.addWidget(self.packetcount2)
        self.twovbhb3.addWidget(self.missiontime)
        self.twovbhb3.addWidget(self.missiontime2)
        self.twovb.addLayout(self.twovbhb1)
        self.twovb.addLayout(self.twovbhb3)
        self.twovb.addLayout(layout)     
        self.prog=QProgressBar(self)
        self.prog.setMaximum(100)
        self.prog.setUpdatesEnabled(True)
        self.prog.setValue(0)
        self.prog.setAlignment(Qt.AlignCenter)
        self.prog.setStyleSheet("QProgressBar{border: 2px solid grey; border-radius: 5px;}")
        self.prog.setStyleSheet("::chunk{background-color: #42C9EB; width: 10px; margin:1.2px; align:center}")
        self.prog.setFixedWidth(335)
        self.prog.setFixedHeight(42)
        self.prog.setFont(QFont("Comic Sans MS",13,QFont.Bold))
        self.listem=QListWidget()
        self.addg=QBrush(QColor(0,255,127))#(156, 239, 130)
        self.listem.setStyleSheet("font:bold 13px rgb(4, 199, 234)")
        self.listem.setFont(QFont("Comic Sans MS",10))
        self.listem.setFixedHeight(163)
        self.listem.setFixedWidth(335)
        self.listem.setSelectionMode(QListWidget.MultiSelection)
        self.listem.setAutoFillBackground(True)
        self.softws=QLabel("       UYDU STATÜSÜ")
        self.softws.setFont(QFont("Comic Sans MS",18,QFont.Bold))
        self.listemitem=["Görev Başladı","Uçuş Bekleniyor","Model Uydu Yükselmekte","Model Uydu İnişte","Görev Yükü Taşıyıcı'dan Ayrıldı","Görev Yükü Kurtarılmayı Bekliyor","Görev Tamamlandı"]
        self.listem.setFont(QFont("Comic Sans MS",14))
        self.z=0
        for i in self.listemitem:
            self.listem.addItem(i)
        self.softws.setFixedWidth(335)
        self.softws.setFixedHeight(60)
        self.softws.setStyleSheet("background-color: #e6e6e6; border:1px solid #000000")
        self.listem.setStyleSheet("background-color: #e6e6e6")
        filename = "gorevyuku.STL"
        self.frames =QFrame()
        self.vl =QVBoxLayout()
        self.reader = vtk.vtkSTLReader()
        self.reader.SetFileName(filename)
        self.coneMapper2 = vtk.vtkPolyDataMapper()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frames)
        self.vl.addWidget(self.vtkWidget)
        self.iren =self.vtkWidget.GetRenderWindow().GetInteractor()
        self.ren = vtk.vtkRenderer()
        self.prev=0
        WIDTH=335
        HEIGHT=400       
        self.frames.setFixedWidth(335)
        self.frames.setFixedHeight(330)
        self.start.setDisabled(False)
        self.transform = vtk.vtkTransform()
        self.transform.RotateX(-90)
        self.transform.RotateY(0)
        self.transform.RotateZ(0)
        self.transformFilter=vtk.vtkTransformPolyDataFilter()
        self.transformFilter.SetTransform(self.transform)
        self.transformFilter.SetInputConnection(self.reader.GetOutputPort())
        self.transformFilter.Update()
        if vtk.VTK_MAJOR_VERSION <= 5:
            self.coneMapper2.SetInput(self.transformFilter.GetOutput())
        else:
            self.coneMapper2.SetInputConnection(self.transformFilter.GetOutputPort())
        self.actor2 = vtk.vtkActor()
        self.actor2.SetMapper(self.coneMapper2)
        self.frames.setLayout(self.vl)
        self.frames.setLineWidth(0.6)
        self.frames.setStyleSheet("border:1px solid #000000; background-color:#7FD5FF")
        self.actor2.GetProperty().SetColor(0.5,0.5,0.5)# (R,G,B)
        self.actor2.SetScale(1, 1, 1)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.ren.AddActor(self.actor2)
        self.ren.SetBackground(0.496,0.832,0.996)
        self.iren.Initialize()
        self.iren.Start()
        self.koordinat=QLabel("PITCH:           ROLL:           YAW:")
        self.mesafe=QLabel("MESAFE:")
        self.gpslo=QLabel("GPS LONGITUDE:")
        self.gpsal=QLabel("GPS LATITUDE:")
        self.koordinat.setFixedHeight(60)
        self.koordinat.setFixedWidth(335)
        self.koordinat.setStyleSheet("font:bold 15px; background-color: #e6e6e6; border:1px solid #000000")
        self.mesafe.setFixedHeight(60)
        self.mesafe.setFixedWidth(335)
        self.mesafe.setStyleSheet("font:bold 15px; background-color: #e6e6e6; border:1px solid #000000")
        self.gpslo.setFixedHeight(60)
        self.gpslo.setFixedWidth(335)
        self.gpslo.setStyleSheet("font:bold 15px; background-color: #e6e6e6; border:1px solid #000000")
        self.gpsal.setFixedHeight(60)
        self.gpsal.setFixedWidth(335)
        self.gpsal.setStyleSheet("font:bold 15px; background-color: #e6e6e6; border:1px solid #000000")
        self.stated=QLabel("Uydu Statüsü:")
        self.stated.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.koordinat.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.koordinat.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.mesafe.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.gpslo.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.gpsal.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.kaynak=QLabel("Görev Tamamlanma Yüzdesi:")
        self.kaynak.setFont(QFont("Comic Sans MS",9,QFont.Bold))
        self.kaynak.setFixedHeight(25)
        self.syc=0
        self.ilkveri=0
        self.onceki_gps_lon=0.000000
        self.onceki_gps_lat=0.000000
        self.threevb.addWidget(self.kaynak) 
        self.threevb.addWidget(self.prog)  
        self.threevb.addWidget(self.stated)
        self.threevb.addWidget(self.softws)
        self.threevb.addWidget(self.listem) 
        self.firstvb.addWidget(self.frames)
        self.firstvb.addWidget(self.koordinat)
        self.threevb.addWidget(self.view3)
        self.threevb.addWidget(self.gpsal)
        self.threevb.addWidget(self.gpslo)         
        self.threevb.addWidget(self.mesafe)
        self.genelhbox.addLayout(self.firstvb)
        self.genelhbox.addLayout(self.twovb)
        self.genelhbox.addLayout(self.threevb)
        self.setLayout(self.genelhbox)
        
        self.oran=0
        
        self.setWindowTitle("Grizu-263 Uzay Takımı| Yer İstasyonu")
        self.show()
    def yukseklikGonder(self):
        ser.write(self.yukseklik.text())
    def mesafe_hesapla(self,lat1,long1,lat2,long2):
        radius=6371*1000
        dlat=(lat2-lat1)*math.pi/180
        dlong=(long2-long1)*math.pi/180
        lat1=lat1*math.pi/180
        lat2=lat2*math.pi/180
        a=math.sin(dlat/2)*math.sin(dlat/2)+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlong/2)*math.sin(dlong/2)
        c=2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance=radius*c
        return distance
    def KalibrEt(self):
        ser.write(b'1')
        self.kalibredurumu=1
        self.prev=0
        for i in range(0,6):
            self.listem.item(i).setBackground(Qt.transparent)
        self.listem.item(0).setBackground(self.addg)
        self.listem.setCurrentRow(0)
        
    def Ayir(self):
        ser.write(b'2')
    def motorBasla(self):
        ser.write(b'3')
    def motorDur(self):
        ser.write(b'4')
    def Start(self):
        self.onceki1=0
        self.onceki2=0
        self.onceki3=0        
        if str(self.ports.currentText())== str('') and str(self.baudrate.currentText())== str(''):
            print("Port Seçmediniz veya Baudrate Seçmediniz!!") 
        else:
            self.start.setDisabled(True)
            h=['Takım Numarası', 'Paket Numarası', 'Gönderim Saati', 'Basınç', 'Yükseklik', 'İniş Hızı', 'Sıcaklık', 'Pil Gerilimi', 'GPS Latitude', 'GPS Longitude', 'GPS Altitude', 'Uydu Statüsü', 'Pitch', 'Roll', 'Yaw', 'Dönüş Sayısı', 'Video Aktarım Bilgisi']
            with open('telemetri_verileri.csv', 'w', newline='') as f:
                thewriter=csv.writer(f)
                thewriter.writerow(h)
            ser.port=str(self.ports.currentText())
            ser.baudrate=int(self.baudrate.currentText())
            ser.timeout=0.5
            ser.open()
            self.runnable = Runnable(self)
            QtCore.QThreadPool.globalInstance().start(self.runnable)
            self.listem.setCurrentRow(self.z)   
            self.listem.item(self.z).setBackground(self.addg)
            self.stated.setText("Uydu Statüsü:"+str("Görev Başladı"))
            QtCore.QMetaObject.invokeMethod(self.prog, "setValue", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(int, 1))
    def Start2(self):   
        self.mySerial=serialThreadClass()
        self.mySerial.start()
        if str(self.ports2.currentText())== str('') and str(self.baudrate2.currentText())== str(''):
            print("Port Seçmediniz veya Baudrate Seçmediniz!!") 
        else:
            
            self.start2.setDisabled(True)
            
            print('girdim')
            
            
    def cizdir(self):
        if len(self.gpslongitude)==2:
            pointItem = self.view3.scene().addCircle(self.gpslongitude[1], self.gpslatitude[1], 5.0)
            pointItem.setBrush(Qt.green)
            pointItem.setPen(QPen(Qt.NoPen))
            pointItem.setToolTip('%f, %f' % (self.gpslongitude[1],self.gpslatitude[1]))
            pointItem.setFlag(QGraphicsItem.ItemIsSelectable, True)
            pointItem2 = self.view5.scene().addCircle(self.gpslongitude[1], self.gpslatitude[1], 5.0)
            pointItem2.setBrush(Qt.green)
            pointItem2.setPen(QPen(Qt.NoPen))
            pointItem2.setToolTip('%f, %f' % (self.gpslongitude[1],self.gpslatitude[1]))
            pointItem2.setFlag(QGraphicsItem.ItemIsSelectable, True)
        else:
            pointItem = self.view3.scene().addCircle(self.gpslong, self.gpslat, 5.0)
            pointItem.setBrush(Qt.blue)
            pointItem.setPen(QPen(Qt.NoPen))
            pointItem.setToolTip('%f, %f' % (self.gpslong,self.gpslat))
            pointItem.setFlag(QGraphicsItem.ItemIsSelectable, True)
            pointItem2 = self.view5.scene().addCircle(self.gpslong, self.gpslat, 5.0)
            pointItem2.setBrush(Qt.blue)
            pointItem2.setToolTip('%f, %f' % (self.gpslong,self.gpslat))
            pointItem2.setFlag(QGraphicsItem.ItemIsSelectable, True)          
        self.view3.scene().update()
        self.view3.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        self.view3.setRenderHint(QPainter.Antialiasing, True)
        self.view3.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.view5.scene().update()
        self.view5.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        self.view5.setRenderHint(QPainter.Antialiasing, True)
        self.view5.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.view3.scene().setItemIndexMethod(QGraphicsScene.NoIndex)
        self.view3.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.view3.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.view5.scene().setItemIndexMethod(QGraphicsScene.NoIndex)
        self.view5.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.view5.setResizeAnchor(QGraphicsView.AnchorViewCenter)
    def get_frame(self):
        _, frame = self.capture.read()
        out.write(frame)
        image = QImage(frame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        image2 = QImage(frame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        pixmap2 = QPixmap.fromImage(image2)
        self.pixmapItem.setPixmap(pixmap) 
        self.pixmapItem2.setPixmap(pixmap2)   
    def Gonder(self):
        print('dosya buradaaa: '+self.dosya_yol)
        os.system(f'ffmpeg -i %s -c:v libx264 -preset ultrafast -crf 50 -c:a copy video5.mp4' % self.dosya_yol)
        cap = cv2.VideoCapture('video5.mp4')
        while(cap.isOpened()):
            ret, rame=cap.read()
            if not ret:
                print('Görüntü Alınamadı')
                gonderilecek_foto_say=int(self.syc/10)
                for i in range(0, 10):
                    son=i*gonderilecek_foto_say
                    image=open("outimage%s.jpg" % son, 'rb')
                    image_read= image.read()
                    image_64_encode= base64.encodestring(image_read)
                    with open("asdfg%s.txt" % i, "w") as imageFile:
                        strx=imageFile.write(image_64_encode.decode('utf-8'))
                break
            im=Image.fromarray(rame)
            im.save("outimage%s.jpg" % self.syc)
            self.syc+=1
        myfile = open('portyap.txt','w')
        myfile.writelines(str(self.baudrate2.currentText())+","+str(self.ports2.currentText())+","+str(self.syc)+"\n")
        myfile.writelines(str(self.baudrate.currentText())+","+str(self.ports.currentText()))
        myfile.close()
        cmd="python untitled10.py"
        proc = QProcess()
        proc.start(cmd)
        proc.startDetached(cmd)
    def ayarlarAc(self):
        self.tabwidget.addTab(self.splitter10, "AYARLAR")
    def ayarlarKapat(self):
        self.tabwidget.addTab(self.view8, "GERİ ALINAN KAMERA KAYDI")
    def geriAl(self):
        self.dimensions4 = self.capture4.read()[1].shape[1::-1]
        scene3 = QGraphicsScene(self)
        pixmap4 = QPixmap(*self.dimensions4)
        self.pixmapItem7 = scene3.addPixmap(pixmap4)
        self.view8 = QGraphicsView(self)
        timer4 = QTimer(self)
        timer4.setInterval(int(1000/fps))
        timer4.timeout.connect(self.get_frame2)
        timer4.start()
        self.tabwidget.addTab(self.view8, "GERİ ALINAN KAMERA KAYDI")
        self.view8.setScene(scene3)
        self.tabwidget.addTab(self.tableWidget3, "GERİ ALINAN TELEMETRİ VERİLERİ")
        self.tableWidget3.horizontalHeader().setStyleSheet("font: bold 9px;")
        with open('telemetri_verileri.csv', "r") as fileInput:
            for row in csv.reader(fileInput):    
                self.tableWidget3.insertRow(self.tableWidget3.rowCount())
                for i in range(17):
                    self.tableWidget3.setItem(self.tableWidget3.rowCount()-1,i,QTableWidgetItem(str(row[i])))
    def Stop(self):
        out.release()
        self.capture.release()
        self.stop.setDisabled(True)
        self.stopflag = True
        self.capture4 = cv2.VideoCapture('kamera_kaydi.avi')
        self.listem.setCurrentRow(6)
        self.listem.item(6).setBackground(self.addg)
        self.stated.setText("Uydu Statüsü:"+str("Görev Tamamlandı"))
        QtCore.QMetaObject.invokeMethod(self.prog, "setValue",QtCore.Qt.QueuedConnection,QtCore.Q_ARG(int, 100))
    def Stop2(self):
        self.stop2.setDisabled(True)
        self.stopflag2 = True

    def get_frame2(self):
        _, frame = self.capture4.read()
        image = QImage(frame, *self.dimensions4, QImage.Format_RGB888).rgbSwapped()
        pixmap4 = QPixmap.fromImage(image)
        self.pixmapItem7.setPixmap(pixmap4)
        if self.capture4.isOpened()==False:
            self.capture4.release()
            timer4.stop()
            timer4.release()
    def portlar(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    def Dosyasec(self):
        root=Tk()
        root.withdraw() 
        root.filename = askopenfilename()
        print(root.filename)
        if root.filename:
            self.iletimdurumu.setText('Video İletim Durumu:Dosya Seçildi')
            self.gonder.setDisabled(False)
            st = os.stat(root.filename)
            #dosya_yol=st.st_size
            self.dosya_yol=str(root.filename)
            
        else:
            self.iletimdurumu.setText('Video İletim Durumu:Dosya Seçilmedi')
class Runnable(QtCore.QRunnable,Pencere,QtCore.QThread):
    def __init__(self, w, *args, **kwargs):
        QtCore.QRunnable.__init__(self, *args, **kwargs)
       # QtCore.QCoreApplication.processEvents()
        self.w = w
    def run(self):
        while True:  
            if (self.w.stopflag): 
                self.w.stopflag = False
                break
            else:
                reading = ser.readline()
                if len(str(reading))>3:
                    try:
                        z=reading.decode('utf-8')
                    except UnicodeDecodeError:
                        continue                   
                    t=z.split(',')
                    if len(t)!=17:
                        continue
                    if int(self.w.kalibredurumu) == 1:
                        self.w.transform.RotateX(self.w.onceki1-int(t[12]))
                        self.w.transform.RotateY(self.w.onceki2-int(t[13]))
                        self.w.transform.RotateZ(0)
                        self.w.onceki1=int(t[12])
                        self.w.onceki2=int(t[13])
                        self.w.onceki3=int(t[14]) 
                        self.w.vtkWidget.update()
                        self.w.ren.ResetCamera()
                    with open('telemetri_verileri.csv', 'a', newline='') as f:
                        thewriter=csv.writer(f)
                        thewriter.writerow(t)
                    k=t[2].split('-')
                    misst.append(str(k[1]))
                                    
                    self.w.timer.append(str(k[0]))
                    self.w.altitude.append(float(t[4]))
                    self.w.temp.append(float(t[6])) 
                    self.w.pressure.append(float(t[3])) 
                    self.w.voltage.append(float(t[7])) 
                    self.w.gpsaltitude.append(float(t[10])) 
                    self.w.inishiz.append(float(t[5]))
                    self.w.packetcount2.setText(t[1])
                    self.w.missiontime2.setText(t[2])
                   
                    if (self.w.onceki_gps_lat != float(t[8]) and self.w.onceki_gps_lon !=float(t[9])) and (float(t[8]) !=0.000000 and float(t[9]) !=0.000000):
                        self.w.gpslatitude.append(float(t[8])) 
                        self.w.gpslong=float(t[9])
                        self.w.gpslat=float(t[8])
                        self.w.gpslongitude.append(float(t[9]))                 
                        self.w.mesafe.setText("MESAFE:"+str(self.w.mesafe_hesapla(self.w.gpslatitude[1],self.w.gpslongitude[1],float(t[8]),float(t[9]))))
                        self.w.onceki_gps_lat=float(t[8])
                        self.w.onceki_gps_lon=float(t[9])
                        self.w.cizdir()    
                    
                    self.w.koordinat.setText("PITCH:"+str(t[12])+"       ROLL:"+str(t[13])+"      YAW:"+str(t[14]))
                    self.w.gpsal.setText("GPS LATITUDE:"+str(t[8]))
                    self.w.gpslo.setText("GPS LONGITUDE:"+str(t[9]))
                    if len(misst)<6:
                        self.w.dates2.append(self.w.y)
                        self.w.y+=1
                        self.w.data_line.setData(x=self.w.dates2, y=self.w.altitude,clear = True)
                        self.w.data_line2.setData(x=self.w.dates2, y=self.w.temp,clear = True)
                        self.w.data_line3.setData(x=self.w.dates2, y=self.w.pressure,clear = True)
                        self.w.data_line4.setData(x=self.w.dates2, y=self.w.voltage,clear = True)
                        self.w.data_line5.setData(x=self.w.dates2, y=self.w.inishiz,clear = True)
                        self.w.data_line6.setData(x=self.w.dates2, y=self.w.gpsaltitude,clear = True)   
                    else:
                        del misst[0]
                        self.w.temp = self.w.temp[1:]
                        self.w.timer= self.w.timer[1:]  
                        self.w.altitude = self.w.altitude[1:]
                        self.w.pressure = self.w.pressure[1:]
                        self.w.voltage = self.w.voltage[1:]
                        self.w.gpsaltitude = self.w.gpsaltitude[1:]
                        self.w.inishiz = self.w.inishiz[1:]
                        self.w.data_line.setData(x=self.w.dates2, y=self.w.altitude,clear = True)
                        self.w.data_line2.setData(x=self.w.dates2, y=self.w.temp,clear = True)
                        self.w.data_line3.setData(x=self.w.dates2, y=self.w.pressure,clear = True)
                        self.w.data_line4.setData(x=self.w.dates2, y=self.w.voltage,clear = True)
                        self.w.data_line5.setData(x=self.w.dates2, y=self.w.inishiz,clear = True)
                        self.w.data_line6.setData(x=self.w.dates2, y=self.w.gpsaltitude,clear = True)   
                        self.w.pw.plotItem.updateLogMode()
                        self.w.pw2.plotItem.updateLogMode()
                        self.w.pw3.plotItem.updateLogMode()
                        self.w.pw4.plotItem.updateLogMode()
                        self.w.pw5.plotItem.updateLogMode()
                        self.w.pw6.plotItem.updateLogMode()                        
                    try:
                        for sayi3 in range(0,17):
                            self.w.tableWidget2.item(0,sayi3).setData(Qt.BackgroundRole,Qt.blue)
                            self.w.tableWidget.item(0,sayi3).setData(Qt.BackgroundRole,Qt.blue)
                    except AttributeError:
                        print('START')
                    self.w.tableWidget2.insertRow(0)
                    self.w.tableWidget.insertRow(0)
                    for i in range(17):
                        self.w.tableWidget2.setItem(0,i,QTableWidgetItem(str(t[i])))
                        self.w.tableWidget.setItem(0,i,QTableWidgetItem(str(t[i])))
                    for sayi in range(0,17):
                        self.w.tableWidget2.item(0,sayi).setData(Qt.BackgroundRole, QColor (2, 232, 253))   
                        self.w.tableWidget.item(0,sayi).setData(Qt.BackgroundRole, QColor (2, 232, 253))                       
                    if self.w.prev != int(t[11]):
                        self.w.listem.setCurrentRow(int(t[11]))
                        self.w.listem.item(int(t[11])).setBackground(self.w.addg)
                        self.w.prev=int(t[11])
                        self.w.stated.setText("Uydu Statüsü:"+str(self.w.uydu_statu[int(t[11])]))
                        QtCore.QMetaObject.invokeMethod(self.w.prog, "setValue", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(int, int(t[11])*19+4))    
                        
        ser.close()   
class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacingü):
        strns = []
        if len(misst)==0:
            return strns
        for x in values:
            strns.append(misst[int(x)])
        return strns
if __name__=="__main__":
    app=QApplication(sys.argv)
    pencere=Pencere()
    sys.exit(app.exec())