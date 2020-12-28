# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'heartGUI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from GUI.mplwidget import MplWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1089, 875)
        icon = QIcon()
        icon.addFile(u"data/heart_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.simulationButton = QPushButton(self.centralwidget)
        self.simulationButton.setObjectName(u"simulationButton")
        self.simulationButton.setGeometry(QRect(740, 20, 161, 51))
        self.simulationTimeLineEdit = QLineEdit(self.centralwidget)
        self.simulationTimeLineEdit.setObjectName(u"simulationTimeLineEdit")
        self.simulationTimeLineEdit.setGeometry(QRect(850, 80, 51, 31))
        self.fullSimulationCheckBox = QCheckBox(self.centralwidget)
        self.fullSimulationCheckBox.setObjectName(u"fullSimulationCheckBox")
        self.fullSimulationCheckBox.setGeometry(QRect(880, 120, 16, 20))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(740, 80, 111, 31))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(130, 10, 101, 21))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(490, 10, 101, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(750, 120, 121, 16))
        self.fullSimulationButton = QPushButton(self.centralwidget)
        self.fullSimulationButton.setObjectName(u"fullSimulationButton")
        self.fullSimulationButton.setGeometry(QRect(920, 20, 151, 121))
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(730, 200, 351, 361))
        self.leftBloodFlowWidget = MplWidget(self.centralwidget)
        self.leftBloodFlowWidget.setObjectName(u"leftBloodFlowWidget")
        self.leftBloodFlowWidget.setGeometry(QRect(10, 30, 351, 261))
        self.rightBloodFlowWidget = MplWidget(self.centralwidget)
        self.rightBloodFlowWidget.setObjectName(u"rightBloodFlowWidget")
        self.rightBloodFlowWidget.setGeometry(QRect(370, 30, 351, 261))
        self.leftPressuresWidget = MplWidget(self.centralwidget)
        self.leftPressuresWidget.setObjectName(u"leftPressuresWidget")
        self.leftPressuresWidget.setGeometry(QRect(10, 300, 351, 261))
        self.rightPressuresWidget = MplWidget(self.centralwidget)
        self.rightPressuresWidget.setObjectName(u"rightPressuresWidget")
        self.rightPressuresWidget.setGeometry(QRect(370, 300, 351, 261))
        self.leftVolumesWidget = MplWidget(self.centralwidget)
        self.leftVolumesWidget.setObjectName(u"leftVolumesWidget")
        self.leftVolumesWidget.setGeometry(QRect(10, 570, 351, 261))
        self.rightVolumesWidget = MplWidget(self.centralwidget)
        self.rightVolumesWidget.setObjectName(u"rightVolumesWidget")
        self.rightVolumesWidget.setGeometry(QRect(370, 570, 351, 261))
        self.pressuresVolumesWidget = MplWidget(self.centralwidget)
        self.pressuresVolumesWidget.setObjectName(u"pressuresVolumesWidget")
        self.pressuresVolumesWidget.setGeometry(QRect(730, 570, 351, 261))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(750, 140, 121, 20))
        self.saveFileCheckBox = QCheckBox(self.centralwidget)
        self.saveFileCheckBox.setObjectName(u"saveFileCheckBox")
        self.saveFileCheckBox.setGeometry(QRect(880, 140, 16, 17))
        self.pushButton_increase = QPushButton(self.centralwidget)
        self.pushButton_increase.setObjectName(u"pushButton_increase")
        self.pushButton_increase.setGeometry(QRect(1000, 150, 75, 41))
        self.lineEdit_th = QLineEdit(self.centralwidget)
        self.lineEdit_th.setObjectName(u"lineEdit_th")
        self.lineEdit_th.setGeometry(QRect(850, 170, 51, 21))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(740, 170, 91, 20))
        self.pushButton_return = QPushButton(self.centralwidget)
        self.pushButton_return.setObjectName(u"pushButton_return")
        self.pushButton_return.setGeometry(QRect(920, 150, 75, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1089, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Symulacja Modelu Serca", None))
        self.simulationButton.setText(QCoreApplication.translate("MainWindow", u"Przeprowad\u017a now\u0105 symulacj\u0119", None))
        self.fullSimulationCheckBox.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"D\u0142ugo\u015b\u0107 symulacji [s]:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Lewa po\u0142owa serca", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Prawa po\u0142owa serca", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Wyrysuj ca\u0142\u0105 symulacj\u0119", None))
        self.fullSimulationButton.setText(QCoreApplication.translate("MainWindow", u"Wykre\u015bl\n"
"charakterystyki\n"
"z pliku", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Zapisz symulacj\u0119 do pliku", None))
        self.saveFileCheckBox.setText("")
        self.pushButton_increase.setText(QCoreApplication.translate("MainWindow", u"Podw\u00f3j\n"
"op\u00f3r", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"D\u0142ugo\u015b\u0107 cyklu [s]:", None))
        self.pushButton_return.setText(QCoreApplication.translate("MainWindow", u"Pocz\u0105tkowy\n"
"op\u00f3r", None))
    # retranslateUi

