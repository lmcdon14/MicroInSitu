# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'td_gui.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import re
        
class MyButton(QtWidgets.QPushButton):
    def __init__(self, widget, font2):
        super().__init__(widget)
        self.setGeometry(QtCore.QRect(80, 875, 160, 50))
        self.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:5px;}")
        self.setFont(font2)
        self.setText("Ramp Current")
        self.setObjectName("lasOut")
        self.co_get = 0
        self.co_set = 0

    def _set_color(self, col):
        palette = self.palette()
        palette.setColor(self.foregroundRole(), col)
        self.setPalette(palette)

    def parseStyleSheet(self):
        ss = self.styleSheet()
        sts = [s.strip() for s in ss.split(';') if len(s.strip())]
        return sts

    def getBackColor(self):
        self.co_get += 1
        # print(fuin(), self.co_get)
        return self.palette().color(self.pal_ele)

    def setBackColor(self, color):
        self.co_set += 1
        sss = self.parseStyleSheet()
        if color.alpha() == 0:
            alph = 0.5
        else:
            alph = color.alpha()
        bg_new = 'background-color: rgba(%2.1f,%2.1f,%2.1f,%2.1f)' % (color.red(), color.green(), color.blue(), alph)

        for k, sty in enumerate(sss):
            if re.search('background-color:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        self.setStyleSheet('QPushButton {' + '; '.join(sss))
        #print('QPushButton {' + '; '.join(sss))

    pal_ele = QtGui.QPalette.Window
    zcolor = QtCore.pyqtProperty(QtGui.QColor, getBackColor, setBackColor)

    color = QtCore.pyqtProperty(QtGui.QColor, fset=_set_color)


class Ui_TapeDriveWindow(object):
    def setupUi(self, TapeDriveWindow):
        # Setup window
        TapeDriveWindow.setObjectName("TapeDriveWindow")
        TapeDriveWindow.resize(640, 975)
        TapeDriveWindow.setMinimumSize(QtCore.QSize(640, 950))
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

        # Rotation Label
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 5, 621, 41))
        self.label_4.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        # PS Label
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 290, 621, 41))
        self.label_5.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        # Main Field Label
        self.label_m = QtWidgets.QLabel(self.centralwidget)
        self.label_m.setGeometry(QtCore.QRect(70, 345, 181, 31))
        self.label_m.setStyleSheet("QLabel {font-size: 18px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_m.setAlignment(QtCore.Qt.AlignCenter)
        self.label_m.setObjectName("label_m")
        # Comp Field Label
        self.label_c = QtWidgets.QLabel(self.centralwidget)
        self.label_c.setGeometry(QtCore.QRect(390, 345, 181, 31))
        self.label_c.setStyleSheet("QLabel {font-size: 18px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_c.setAlignment(QtCore.Qt.AlignCenter)
        self.label_c.setObjectName("label_c")
        # Oven Label
        self.label_o = QtWidgets.QLabel(self.centralwidget)
        self.label_o.setGeometry(QtCore.QRect(10, 550, 621, 41))
        self.label_o.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_o.setAlignment(QtCore.Qt.AlignCenter)
        self.label_o.setObjectName("label_o")
        # Main Field Setpoint Label
        self.label_ms = QtWidgets.QLabel(self.centralwidget)
        self.label_ms.setGeometry(QtCore.QRect(10, 370, 141, 41))
        self.label_ms.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_ms.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ms.setObjectName("label_ms")
        # Main Field Readout Label
        self.label_msr = QtWidgets.QLabel(self.centralwidget)
        self.label_msr.setGeometry(QtCore.QRect(170, 370, 141, 41))
        self.label_msr.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_msr.setAlignment(QtCore.Qt.AlignCenter)
        self.label_msr.setObjectName("label_msr")
        # Comp Field Setpoint Label
        self.label_cos = QtWidgets.QLabel(self.centralwidget)
        self.label_cos.setGeometry(QtCore.QRect(330, 370, 141, 41))
        self.label_cos.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_cos.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cos.setObjectName("label_cos")
        # Comp Field Readout Label
        self.label_cosr = QtWidgets.QLabel(self.centralwidget)
        self.label_cosr.setGeometry(QtCore.QRect(490, 370, 141, 41))
        self.label_cosr.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_cosr.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cosr.setObjectName("label_cosr")
        # Cell Wall Setpoint Label
        self.label_cs = QtWidgets.QLabel(self.centralwidget)
        self.label_cs.setGeometry(QtCore.QRect(5, 600, 100, 41))
        self.label_cs.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_cs.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cs.setObjectName("label_cs")
        # Oven Wall Setpoint Label
        self.label_os = QtWidgets.QLabel(self.centralwidget)
        self.label_os.setGeometry(QtCore.QRect(525, 600, 120, 41))
        self.label_os.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_os.setAlignment(QtCore.Qt.AlignCenter)
        self.label_os.setObjectName("label_os")
        # Cell Wall Readout Label
        self.label_cr = QtWidgets.QLabel(self.centralwidget)
        self.label_cr.setGeometry(QtCore.QRect(5, 650, 100, 41))
        self.label_cr.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_cr.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cr.setObjectName("label_cr")
        # Oven Wall Readout Label
        self.label_or = QtWidgets.QLabel(self.centralwidget)
        self.label_or.setGeometry(QtCore.QRect(525, 650, 120, 41))
        self.label_or.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_or.setAlignment(QtCore.Qt.AlignCenter)
        self.label_or.setObjectName("label_or")
        # Halfwave plate readout label
        self.label_hr = QtWidgets.QLabel(self.centralwidget)
        self.label_hr.setGeometry(QtCore.QRect(260, 170, 120, 41))
        self.label_hr.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_hr.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hr.setObjectName("label_hr")
        # Laser PS Label
        self.label_lps = QtWidgets.QLabel(self.centralwidget)
        self.label_lps.setGeometry(QtCore.QRect(10, 720, 301, 41))
        self.label_lps.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_lps.setAlignment(QtCore.Qt.AlignCenter)
        self.label_lps.setObjectName("label_lps")
        # Laser Setpoint Label
        self.label_lassp = QtWidgets.QLabel(self.centralwidget)
        self.label_lassp.setGeometry(QtCore.QRect(5, 775, 100, 41))
        self.label_lassp.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_lassp.setAlignment(QtCore.Qt.AlignCenter)
        self.label_lassp.setObjectName("label_lassp")
        # Laser Ramp Rate Label
        self.label_rampsp = QtWidgets.QLabel(self.centralwidget)
        self.label_rampsp.setGeometry(QtCore.QRect(5, 825, 100, 41))
        self.label_rampsp.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_rampsp.setAlignment(QtCore.Qt.AlignCenter)
        self.label_rampsp.setObjectName("label_rampsp")
        # Photodiodes Label
        self.label_pds = QtWidgets.QLabel(self.centralwidget)
        self.label_pds.setGeometry(QtCore.QRect(330, 720, 301, 41))
        self.label_pds.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_pds.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pds.setObjectName("label_pds")
        # PD1 Label
        self.label_pd1 = QtWidgets.QLabel(self.centralwidget)
        self.label_pd1.setGeometry(QtCore.QRect(325, 775, 100, 41))
        self.label_pd1.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_pd1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pd1.setObjectName("label_pd1")
        # PD2 Label
        self.label_pd2 = QtWidgets.QLabel(self.centralwidget)
        self.label_pd2.setGeometry(QtCore.QRect(325, 825, 100, 41))
        self.label_pd2.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_pd2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pd2.setObjectName("label_pd2")

        # Power Supply Control 1
        self.ps1spinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ps1spinBox.setGeometry(QtCore.QRect(30, 400, 100, 40))
        self.ps1spinBox.setFont(font)
        self.ps1spinBox.setDecimals(3)
        self.ps1spinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ps1spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.ps1spinBox.setMinimum(0.0)
        self.ps1spinBox.setMaximum(20.0)
        self.ps1spinBox.setProperty("value", 0.0)
        self.ps1spinBox.setObjectName("ps1spinBox")
        # Power Supply Readout 1
        self.ps1readspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ps1readspinBox.setGeometry(QtCore.QRect(190, 400, 100, 40))
        self.ps1readspinBox.setFont(font)
        self.ps1readspinBox.setReadOnly(True)
        self.ps1readspinBox.setDecimals(3)
        self.ps1readspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ps1readspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ps1readspinBox.setMinimum(0.0)
        self.ps1readspinBox.setMaximum(20.0)
        self.ps1readspinBox.setProperty("value", 0.0)
        self.ps1readspinBox.setObjectName("ps1readspinBox")

        # Power Supply Control 2
        self.ps2spinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ps2spinBox.setGeometry(QtCore.QRect(350, 400, 100, 40))
        self.ps2spinBox.setFont(font)
        self.ps2spinBox.setDecimals(3)
        self.ps2spinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ps2spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.ps2spinBox.setMinimum(0.0)
        self.ps2spinBox.setMaximum(20.0)
        self.ps2spinBox.setProperty("value", 0.0)
        self.ps2spinBox.setObjectName("ps2spinBox")
        # Power Supply Readout 2
        self.ps2readspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ps2readspinBox.setGeometry(QtCore.QRect(510, 400, 100, 40))
        self.ps2readspinBox.setFont(font)
        self.ps2readspinBox.setReadOnly(True)
        self.ps2readspinBox.setDecimals(3)
        self.ps2readspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ps2readspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ps2readspinBox.setMinimum(0.0)
        self.ps2readspinBox.setMaximum(20.0)
        self.ps2readspinBox.setProperty("value", 0.0)
        self.ps2readspinBox.setObjectName("ps2readspinBox")

        # Cell Wall Control
        self.cellspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.cellspinBox.setGeometry(QtCore.QRect(110, 600, 100, 40))
        self.cellspinBox.setFont(font)
        self.cellspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.cellspinBox.setStyleSheet("color: red;")
        self.cellspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.cellspinBox.setMinimum(0.0)
        self.cellspinBox.setMaximum(220.0)
        self.cellspinBox.setProperty("value", 20.0)
        self.cellspinBox.setObjectName("cellspinBox")

        # Oven Wall Control
        self.ovenspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ovenspinBox.setGeometry(QtCore.QRect(430, 600, 100, 40))
        self.ovenspinBox.setFont(font)
        self.ovenspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ovenspinBox.setStyleSheet("color: lightgrey;")
        self.ovenspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.ovenspinBox.setMinimum(0.0)
        self.ovenspinBox.setMaximum(220.0)
        self.ovenspinBox.setProperty("value", 20.0)
        self.ovenspinBox.setObjectName("ovenspinBox")

        # Laser Output Control
        self.lasspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.lasspinBox.setGeometry(QtCore.QRect(110, 775, 100, 40))
        self.lasspinBox.setFont(font)
        self.lasspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.lasspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.lasspinBox.setMinimum(0.0)
        self.lasspinBox.setMaximum(45.0)
        self.lasspinBox.setProperty("value", 0.0)
        self.lasspinBox.setObjectName("lasspinBox")

        # Laser Ramp Rate Control
        self.rampspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.rampspinBox.setGeometry(QtCore.QRect(110, 825, 100, 40))
        self.rampspinBox.setFont(font)
        self.rampspinBox.setSingleStep(0.1)
        self.rampspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.rampspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.rampspinBox.setMinimum(0.0)
        self.rampspinBox.setMaximum(1.0)
        self.rampspinBox.setProperty("value", 1.0)
        self.rampspinBox.setObjectName("rampspinBox")

        # Cell Wall Readout
        self.cellreadout = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.cellreadout.setGeometry(QtCore.QRect(110, 650, 100, 40))
        self.cellreadout.setFont(font)
        self.cellreadout.setReadOnly(True)
        self.cellreadout.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.cellreadout.setAlignment(QtCore.Qt.AlignHCenter)
        self.cellreadout.setStyleSheet("color: red;")
        self.cellreadout.setObjectName("cellreadout")

        # Oven Wall Readout
        self.ovenreadout = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ovenreadout.setGeometry(QtCore.QRect(430, 650, 100, 40))
        self.ovenreadout.setFont(font)
        self.ovenreadout.setReadOnly(True)
        self.ovenreadout.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ovenreadout.setAlignment(QtCore.Qt.AlignHCenter)
        self.ovenreadout.setStyleSheet("color: lightgrey;")
        self.ovenreadout.setObjectName("ovenreadout")

        # Photodiode 1 Readout
        self.pdreadout = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.pdreadout.setGeometry(QtCore.QRect(430, 775, 100, 40))
        self.pdreadout.setFont(font)
        self.pdreadout.setReadOnly(True)
        self.pdreadout.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.pdreadout.setAlignment(QtCore.Qt.AlignHCenter)
        self.pdreadout.setStyleSheet("color: black;")
        self.pdreadout.setObjectName("pdreadout")

        # Photodiode 2 Readout
        self.pd2readout = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.pd2readout.setGeometry(QtCore.QRect(430, 825, 100, 40))
        self.pd2readout.setFont(font)
        self.pd2readout.setReadOnly(True)
        self.pd2readout.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.pd2readout.setAlignment(QtCore.Qt.AlignHCenter)
        self.pd2readout.setStyleSheet("color: black;")
        self.pd2readout.setObjectName("pd2readout")

        # Laser Current Readout
        self.lasreadout = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.lasreadout.setGeometry(QtCore.QRect(210, 775, 100, 40))
        self.lasreadout.setFont(font)
        self.lasreadout.setReadOnly(True)
        self.lasreadout.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.lasreadout.setAlignment(QtCore.Qt.AlignHCenter)
        self.lasreadout.setStyleSheet("color: black;")
        self.lasreadout.setObjectName("lasreadout")

        # PS1 Output Enable
        self.ps1Out = QtWidgets.QPushButton(self.centralwidget)
        self.ps1Out.setGeometry(QtCore.QRect(80, 460, 160, 50))
        self.ps1Out.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;}")
        font2 = font
        font2.setPointSize(11)
        font2.setBold(False)
        self.ps1Out.setFont(font2)
        self.ps1Out.setCheckable(True)
        self.ps1Out.setText("Output Enable")
        self.ps1Out.setObjectName("ps1Out")

        # PS2 Output Enable
        self.ps2Out = QtWidgets.QPushButton(self.centralwidget)
        self.ps2Out.setGeometry(QtCore.QRect(400, 460, 160, 50))
        self.ps2Out.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;}")
        self.ps2Out.setFont(font2)
        self.ps2Out.setCheckable(True)
        self.ps2Out.setText("Output Enable")
        self.ps2Out.setObjectName("ps2Out")

        # Oven Toggle 
        self.oventog = QtWidgets.QPushButton(self.centralwidget)
        self.oventog.setGeometry(QtCore.QRect(240, 625, 160, 50))
        self.oventog.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:5px;}")
        self.oventog.setFont(font2)
        self.oventog.setCheckable(True)
        self.oventog.setText("Cell Wall")
        self.oventog.setObjectName("oventog")

        # Laser Ramp Control
        self.lasOut = MyButton(self.centralwidget, font2)
        self.anim = QtCore.QPropertyAnimation(self.lasOut, b"zcolor")
        self.anim.setDuration(750)
        self.anim.setLoopCount(1)
        self.anim.setStartValue(QtGui.QColor(0,0,0,0.5))
        self.anim.setKeyValueAt(0.1, QtGui.QColor("lightblue"))
        self.anim.setKeyValueAt(0.9, QtGui.QColor("lightblue"))
        self.anim.setEndValue(QtGui.QColor(0,0,0,0.5))

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
        degree_sign = u"\N{DEGREE SIGN}"
        _translate = QtCore.QCoreApplication.translate
        TapeDriveWindow.setWindowTitle(_translate("TapeDriveWindow", "Micro In-Situ Control"))
        self.homeEnable.setText(_translate("TapeDriveWindow", "Enable"))
        self.groupBox_2.setTitle(_translate("TapeDriveWindow", "Step Size (deg)"))
        self.verticalSlider.setToolTip(_translate("TapeDriveWindow", "<html><head/><body><p>Drag to change step size. Step will be set when slider is released.</p></body></html>"))
        self.label_4.setText(_translate("TapeDriveWindow", "Half Wave Plate Rotation"))
        self.label_5.setText(_translate("TapeDriveWindow", "Power Supply Control"))
        self.label_m.setText(_translate("TapeDriveWindow", "Main Field"))
        self.label_c.setText(_translate("TapeDriveWindow", "Compensation Field"))
        self.label_o.setText(_translate("TapeDriveWindow", "Oven Control"))
        self.label_lps.setText(_translate("TapeDriveWindow", "Laser Power"))
        self.label_pds.setText(_translate("TapeDriveWindow", "Photodiodes"))
        self.label_cs.setText(_translate("TapeDriveWindow", "Cell Wall\nSetpoint (" + degree_sign + "C)"))
        self.label_os.setText(_translate("TapeDriveWindow", "Oven Wall\nSetpoint (" + degree_sign + "C)"))
        self.label_cr.setText(_translate("TapeDriveWindow", "Cell Wall\nReadout (" + degree_sign + "C)"))
        self.label_or.setText(_translate("TapeDriveWindow", "Oven Wall\nReadout (" + degree_sign + "C)"))
        self.label_lassp.setText(_translate("TapeDriveWindow", "Current\nSetpoint (A)"))
        self.label_rampsp.setText(_translate("TapeDriveWindow", "Ramp Rate\n(A/s)"))
        self.label_pd1.setText(_translate("TapeDriveWindow", "Transmission\nPhotodiode"))
        self.label_pd2.setText(_translate("TapeDriveWindow", "EPR\nPhotodiode"))
        self.label_hr.setText(_translate("TapeDriveWindow", "Angle Readout"))
        self.label_cos.setText(_translate("TapeDriveWindow", "Current Setpoint (A)"))
        self.label_cosr.setText(_translate("TapeDriveWindow", "Current Readout (A)"))
        self.label_ms.setText(_translate("TapeDriveWindow", "Current Setpoint (A)"))
        self.label_msr.setText(_translate("TapeDriveWindow", "Current Readout (A)"))
        self.actionQuit.setText(_translate("TapeDriveWindow", "Exit"))
        self.actionQuit.setShortcut(_translate("TapeDriveWindow", "Meta+Q"))
        self.actionNothingHere.setText(_translate("TapeDriveWindow", "NothingHere"))

import resources_rc