# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'td_gui.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TapeDriveWindow(object):
    def setupUi(self, TapeDriveWindow):
        # Setup window
        TapeDriveWindow.setObjectName("TapeDriveWindow")
        TapeDriveWindow.resize(640, 300)
        TapeDriveWindow.setMinimumSize(QtCore.QSize(640, 300))
        TapeDriveWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        TapeDriveWindow.setStyleSheet("TapeDriveWindow {qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))}")
        self.centralwidget = QtWidgets.QWidget(TapeDriveWindow)
        self.centralwidget.setObjectName("centralwidget")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resources/bw3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Resources/fw3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # Move forward
        self.btnForward = QtWidgets.QPushButton(self.centralwidget)
        self.btnForward.setGeometry(QtCore.QRect(350, 75, 151, 91))
        self.btnForward.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); border-radius: 5px;}")
        self.btnForward.setText("")
        self.btnForward.setIcon(icon1)
        self.btnForward.setIconSize(QtCore.QSize(100, 100))
        self.btnForward.setObjectName("btnForward")

        # Move backward
        self.btnBackward = QtWidgets.QPushButton(self.centralwidget)
        self.btnBackward.setGeometry(QtCore.QRect(140, 75, 151, 91))
        self.btnBackward.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); border-radius:4px;}")
        self.btnBackward.setText("")
        self.btnBackward.setIcon(icon)
        self.btnBackward.setIconSize(QtCore.QSize(100, 100))
        self.btnBackward.setObjectName("btnBackward")

        # Home group
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 75, 81, 101))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.btnHome = QtWidgets.QPushButton(self.groupBox)
        self.btnHome.setEnabled(False)
        self.btnHome.setGeometry(QtCore.QRect(10, 30, 61, 61))
        self.btnHome.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Resources/home2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnHome.setIcon(icon2)
        self.btnHome.setIconSize(QtCore.QSize(75, 75))
        self.btnHome.setObjectName("btnHome")
        self.homeEnable = QtWidgets.QCheckBox(self.groupBox)
        self.homeEnable.setGeometry(QtCore.QRect(10, 10, 71, 21))
        self.homeEnable.setObjectName("homeEnable")

        # Step group
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(520, 50, 101, 201))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalSlider = QtWidgets.QSlider(self.groupBox_2)
        self.verticalSlider.setGeometry(QtCore.QRect(10, 30, 21, 160))
        self.verticalSlider.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.verticalSlider.setMinimum(1)
        self.verticalSlider.setMaximum(359)
        self.verticalSlider.setSingleStep(1)
        self.verticalSlider.setPageStep(45)
        self.verticalSlider.setSliderPosition(45)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.verticalSlider.setTickInterval(5)
        self.verticalSlider.setObjectName("verticalSlider")
        # SpinBox
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox.setGeometry(QtCore.QRect(39, 30, 61, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox.setFont(font)
        self.spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(359)
        self.spinBox.setProperty("value", 45)
        self.spinBox.setObjectName("spinBox")

        # Absolute Coordinates
        self.absCoords = QtWidgets.QSpinBox(self.centralwidget)
        self.absCoords.setGeometry(QtCore.QRect(290, 200, 60, 40))
        self.absCoords.setFont(font)
        self.absCoords.setReadOnly(True)
        self.absCoords.setAlignment(QtCore.Qt.AlignHCenter)
        self.absCoords.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.absCoords.setMinimum(0)
        self.absCoords.setMaximum(359)
        self.absCoords.setProperty("value", 45)
        self.absCoords.setObjectName("absCoords")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 5, 621, 41))
        self.label_4.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")

        TapeDriveWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(TapeDriveWindow)
        self.statusbar.setObjectName("statusbar")
        TapeDriveWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(TapeDriveWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menuBar.setObjectName("menuBar")
        TapeDriveWindow.setMenuBar(self.menuBar)
        self.actionQuit = QtWidgets.QAction(TapeDriveWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionNothingHere = QtWidgets.QAction(TapeDriveWindow)
        self.actionNothingHere.setObjectName("actionNothingHere")

        self.retranslateUi(TapeDriveWindow)
        QtCore.QMetaObject.connectSlotsByName(TapeDriveWindow)

    def retranslateUi(self, TapeDriveWindow):
        _translate = QtCore.QCoreApplication.translate
        TapeDriveWindow.setWindowTitle(_translate("TapeDriveWindow", "Half Wave Plate Rotation"))
        self.homeEnable.setText(_translate("TapeDriveWindow", "Enable"))
        self.groupBox_2.setTitle(_translate("TapeDriveWindow", "Step Size (deg)"))
        self.verticalSlider.setToolTip(_translate("TapeDriveWindow", "<html><head/><body><p>Drag to change step size. Step will be set when slider is released.</p></body></html>"))
        self.label_4.setText(_translate("TapeDriveWindow", "Half Wave Plate Rotation"))
        self.actionQuit.setText(_translate("TapeDriveWindow", "Exit"))
        self.actionQuit.setShortcut(_translate("TapeDriveWindow", "Meta+Q"))
        self.actionNothingHere.setText(_translate("TapeDriveWindow", "NothingHere"))

import resources_rc
