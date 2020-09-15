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
    def __init__(self, widget, font2, dims, text):
        super().__init__(widget)
        font3 = font2
        font3.setPointSize(10)
        self.setGeometry(dims)
        self.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:5px;}")
        self.setFont(font3)
        self.setText(text)
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
        TapeDriveWindow.resize(640, 1000)
        TapeDriveWindow.setMinimumSize(QtCore.QSize(640, 1000))
        TapeDriveWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        TapeDriveWindow.setStyleSheet("TapeDriveWindow {qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))}")
        self.centralwidget = QtWidgets.QWidget(TapeDriveWindow)
        self.centralwidget.setObjectName("centralwidget")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resources/bw3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Resources/fw3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        """
        # Move forward
        self.btnForward = QtWidgets.QPushButton(self.centralwidget)
        self.btnForward.setGeometry(QtCore.QRect(175, 75, 101, 61))
        self.btnForward.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); border-radius: 5px;}")
        self.btnForward.setText("")
        self.btnForward.setIcon(icon1)
        self.btnForward.setIconSize(QtCore.QSize(100, 100))
        self.btnForward.setObjectName("btnForward")

        # Move backward
        self.btnBackward = QtWidgets.QPushButton(self.centralwidget)
        self.btnBackward.setGeometry(QtCore.QRect(45, 75, 101, 61))
        self.btnBackward.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); border-radius:5px;}")
        self.btnBackward.setText("")
        self.btnBackward.setIcon(icon)
        self.btnBackward.setIconSize(QtCore.QSize(100, 100))
        self.btnBackward.setObjectName("btnBackward")

        # Home group
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 75, 61, 76))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.btnHome = QtWidgets.QPushButton(self.groupBox)
        self.btnHome.setEnabled(False)
        self.btnHome.setGeometry(QtCore.QRect(10, 30, 46, 46))
        self.btnHome.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Resources/home2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnHome.setIcon(icon2)
        self.btnHome.setIconSize(QtCore.QSize(46, 46))
        self.btnHome.setObjectName("btnHome")
        self.homeEnable = QtWidgets.QCheckBox(self.groupBox)
        self.homeEnable.setGeometry(QtCore.QRect(10, 10, 46, 16))
        self.homeEnable.setObjectName("homeEnable")

        # Step group
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(200, 50, 101, 151))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalSlider = QtWidgets.QSlider(self.groupBox_2)
        self.verticalSlider.setGeometry(QtCore.QRect(10, 30, 21, 110))
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
        """

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        self.absCoords = [None] * 2
        self.absCoordset = [None] * 2

        # HWP Absolute Coordinates
        self.absCoords[0] = QtWidgets.QSpinBox(self.centralwidget)
        self.absCoords[0].setGeometry(QtCore.QRect(110, 150, 100, 40))
        self.absCoords[0].setFont(font)
        self.absCoords[0].setReadOnly(True)
        self.absCoords[0].setAlignment(QtCore.Qt.AlignHCenter)
        self.absCoords[0].setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.absCoords[0].setMinimum(0)
        self.absCoords[0].setMaximum(359)
        self.absCoords[0].setProperty("value", 0)
        self.absCoords[0].setObjectName("absCoords1")

        # HWP Absolute Coordinates Setpoint
        self.absCoordset[0] = QtWidgets.QSpinBox(self.centralwidget)
        self.absCoordset[0].setGeometry(QtCore.QRect(110, 100, 100, 40))
        self.absCoordset[0].setFont(font)
        self.absCoordset[0].setAlignment(QtCore.Qt.AlignHCenter)
        self.absCoordset[0].setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.absCoordset[0].setKeyboardTracking(False)
        self.absCoordset[0].setMinimum(0)
        self.absCoordset[0].setMaximum(359)
        self.absCoordset[0].setProperty("value", 0)
        self.absCoordset[0].setObjectName("absCoordset1")

        # QWP Absolute Coordinates
        self.absCoords[1] = QtWidgets.QSpinBox(self.centralwidget)
        self.absCoords[1].setGeometry(QtCore.QRect(320+110, 150, 100, 40))
        self.absCoords[1].setFont(font)
        self.absCoords[1].setReadOnly(True)
        self.absCoords[1].setAlignment(QtCore.Qt.AlignHCenter)
        self.absCoords[1].setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.absCoords[1].setMinimum(-359)
        self.absCoords[1].setMaximum(359)
        self.absCoords[1].setProperty("value", 0)
        self.absCoords[1].setObjectName("absCoords2")

        # QWP Absolute Coordinates Setpoint
        self.absCoordset[1] = QtWidgets.QSpinBox(self.centralwidget)
        self.absCoordset[1].setGeometry(QtCore.QRect(320+110, 100, 100, 40))
        self.absCoordset[1].setFont(font)
        self.absCoordset[1].setAlignment(QtCore.Qt.AlignHCenter)
        self.absCoordset[1].setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.absCoordset[1].setKeyboardTracking(False)
        self.absCoordset[1].setMinimum(-359)
        self.absCoordset[1].setMaximum(359)
        self.absCoordset[1].setProperty("value", 0)
        self.absCoordset[1].setObjectName("absCoordset2")

        # QWP Right Hand Circular Position
        self.QWP_right_pos = QtWidgets.QSpinBox(self.centralwidget)
        self.QWP_right_pos.setGeometry(QtCore.QRect(320+3*320/4+5, 50, 60, 40))
        self.QWP_right_pos.setFont(font)
        self.QWP_right_pos.setAlignment(QtCore.Qt.AlignHCenter)
        self.QWP_right_pos.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.QWP_right_pos.setKeyboardTracking(False)
        self.QWP_right_pos.setProperty("value", 130)
        self.QWP_right_pos.setObjectName("QWP_right_pos")

        # QWP Left Hand Circular Position
        self.QWP_left_pos = QtWidgets.QSpinBox(self.centralwidget)
        self.QWP_left_pos.setGeometry(QtCore.QRect(320+1*320/4+5, 50, 60, 40))
        self.QWP_left_pos.setFont(font)
        self.QWP_left_pos.setAlignment(QtCore.Qt.AlignHCenter)
        self.QWP_left_pos.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.QWP_left_pos.setKeyboardTracking(False)
        self.QWP_left_pos.setProperty("value", -130)
        self.QWP_left_pos.setObjectName("QWP_left_pos")

        # Rotation Label
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 5, 301, 41))
        self.label_4.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        # QWP Label
        self.label_qwp = QtWidgets.QLabel(self.centralwidget)
        self.label_qwp.setGeometry(QtCore.QRect(330, 5, 301, 41))
        self.label_qwp.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_qwp.setAlignment(QtCore.Qt.AlignCenter)
        self.label_qwp.setObjectName("label_qwp")
        # PS Label
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 220, 621, 41))
        self.label_5.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        # Main Field Label
        self.label_m = QtWidgets.QLabel(self.centralwidget)
        self.label_m.setGeometry(QtCore.QRect(70, 275, 181, 31))
        self.label_m.setStyleSheet("QLabel {font-size: 18px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_m.setAlignment(QtCore.Qt.AlignCenter)
        self.label_m.setObjectName("label_m")
        # Comp Field Label
        self.label_c = QtWidgets.QLabel(self.centralwidget)
        self.label_c.setGeometry(QtCore.QRect(390, 275, 181, 31))
        self.label_c.setStyleSheet("QLabel {font-size: 18px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_c.setAlignment(QtCore.Qt.AlignCenter)
        self.label_c.setObjectName("label_c")
        # Oven Label
        self.label_o = QtWidgets.QLabel(self.centralwidget)
        self.label_o.setGeometry(QtCore.QRect(10, 450, 621, 41))
        self.label_o.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_o.setAlignment(QtCore.Qt.AlignCenter)
        self.label_o.setObjectName("label_o")
        # AFP
        self.label_afp = QtWidgets.QLabel(self.centralwidget)
        self.label_afp.setGeometry(QtCore.QRect(10, 800, 400, 41))
        self.label_afp.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_afp.setAlignment(QtCore.Qt.AlignCenter)
        self.label_afp.setObjectName("label_afp")
        # Main Field Setpoint Label
        self.label_ms = QtWidgets.QLabel(self.centralwidget)
        self.label_ms.setGeometry(QtCore.QRect(5, 320, 100, 41))
        self.label_ms.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_ms.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ms.setObjectName("label_ms")
        # Main Field Readout Label
        # self.label_msr = QtWidgets.QLabel(self.centralwidget)
        # self.label_msr.setGeometry(QtCore.QRect(170, 300, 141, 41))
        # self.label_msr.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        # self.label_msr.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_msr.setObjectName("label_msr")
        # Comp Field Setpoint Label
        self.label_cos = QtWidgets.QLabel(self.centralwidget)
        self.label_cos.setGeometry(QtCore.QRect(325, 320, 100, 41))
        self.label_cos.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_cos.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cos.setObjectName("label_cos")
        # Comp Field Readout Label
        # self.label_cosr = QtWidgets.QLabel(self.centralwidget)
        # self.label_cosr.setGeometry(QtCore.QRect(490, 300, 141, 41))
        # self.label_cosr.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        # self.label_cosr.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_cosr.setObjectName("label_cosr")
        # Cell Wall Setpoint Label
        self.label_cs = QtWidgets.QLabel(self.centralwidget)
        self.label_cs.setGeometry(QtCore.QRect(5, 500, 100, 41))
        self.label_cs.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_cs.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cs.setObjectName("label_cs")
        # Oven Wall Setpoint Label
        self.label_os = QtWidgets.QLabel(self.centralwidget)
        self.label_os.setGeometry(QtCore.QRect(525, 500, 120, 41))
        self.label_os.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_os.setAlignment(QtCore.Qt.AlignCenter)
        self.label_os.setObjectName("label_os")
        # Cell Wall Readout Label
        self.label_cr = QtWidgets.QLabel(self.centralwidget)
        self.label_cr.setGeometry(QtCore.QRect(5, 550, 100, 41))
        self.label_cr.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_cr.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cr.setObjectName("label_cr")
        # Oven Wall Readout Label
        self.label_or = QtWidgets.QLabel(self.centralwidget)
        self.label_or.setGeometry(QtCore.QRect(525, 550, 120, 41))
        self.label_or.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_or.setAlignment(QtCore.Qt.AlignCenter)
        self.label_or.setObjectName("label_or")
        # Halfwave plate readout label
        self.label_hr = QtWidgets.QLabel(self.centralwidget)
        self.label_hr.setGeometry(QtCore.QRect(100, 180, 120, 41))
        self.label_hr.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_hr.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hr.setObjectName("label_hr")
        # Quarterwave plate readout label
        self.label_qr = QtWidgets.QLabel(self.centralwidget)
        self.label_qr.setGeometry(QtCore.QRect(420, 180, 120, 41))
        self.label_qr.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_qr.setAlignment(QtCore.Qt.AlignCenter)
        self.label_qr.setObjectName("label_qr")
        # Laser PS Label
        self.label_lps = QtWidgets.QLabel(self.centralwidget)
        self.label_lps.setGeometry(QtCore.QRect(10, 620, 301, 41))
        self.label_lps.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_lps.setAlignment(QtCore.Qt.AlignCenter)
        self.label_lps.setObjectName("label_lps")
        # Laser Setpoint Label
        self.label_lassp = QtWidgets.QLabel(self.centralwidget)
        self.label_lassp.setGeometry(QtCore.QRect(5, 675, 100, 41))
        self.label_lassp.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_lassp.setAlignment(QtCore.Qt.AlignCenter)
        self.label_lassp.setObjectName("label_lassp")
        # Laser Ramp Rate Label
        self.label_rampsp = QtWidgets.QLabel(self.centralwidget)
        self.label_rampsp.setGeometry(QtCore.QRect(5, 725, 100, 41))
        self.label_rampsp.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_rampsp.setAlignment(QtCore.Qt.AlignCenter)
        self.label_rampsp.setObjectName("label_rampsp")
        # Photodiodes Label
        self.label_pds = QtWidgets.QLabel(self.centralwidget)
        self.label_pds.setGeometry(QtCore.QRect(330, 620, 301, 41))
        self.label_pds.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_pds.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pds.setObjectName("label_pds")
        # PD1 Label
        self.label_pd1 = QtWidgets.QLabel(self.centralwidget)
        self.label_pd1.setGeometry(QtCore.QRect(325, 675, 100, 41))
        self.label_pd1.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_pd1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pd1.setObjectName("label_pd1")
        # PD2 Label
        self.label_pd2 = QtWidgets.QLabel(self.centralwidget)
        self.label_pd2.setGeometry(QtCore.QRect(325, 725, 100, 41))
        self.label_pd2.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_pd2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pd2.setObjectName("label_pd2")
        # AFP Center Frequency Label
        self.label_afp1 = QtWidgets.QLabel(self.centralwidget)
        self.label_afp1.setGeometry(QtCore.QRect(5, 855, 100, 41))
        self.label_afp1.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_afp1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_afp1.setObjectName("label_afp1")
        # AFP FWHM Label
        self.label_afp2 = QtWidgets.QLabel(self.centralwidget)
        self.label_afp2.setGeometry(QtCore.QRect(5, 900, 100, 41))
        self.label_afp2.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_afp2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_afp2.setObjectName("label_afp2")
        # AFP Sweeprate Label
        self.label_afp3 = QtWidgets.QLabel(self.centralwidget)
        self.label_afp3.setGeometry(QtCore.QRect(215, 855, 100, 41))
        self.label_afp3.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_afp3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_afp3.setObjectName("label_afp3")
        # AFP RF Amplitude Label
        self.label_afp4 = QtWidgets.QLabel(self.centralwidget)
        self.label_afp4.setGeometry(QtCore.QRect(215, 900, 100, 41))
        self.label_afp4.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_afp4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_afp4.setObjectName("label_afp4")
        # AFP Timer Label
        self.label_afptime = QtWidgets.QLabel(self.centralwidget)
        self.label_afptime.setGeometry(QtCore.QRect(400, 800, 100, 41))
        self.label_afptime.setStyleSheet("QLabel {font-size: 14x; color: black; border-radius: 5px;}")
        self.label_afptime.setAlignment(QtCore.Qt.AlignCenter)
        self.label_afptime.setObjectName("label_afptime")
        # Plot Enable Label
        self.label_plot = QtWidgets.QLabel(self.centralwidget)
        self.label_plot.setGeometry(QtCore.QRect(567, 850, 81, 41))
        self.label_plot.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_plot.setAlignment(QtCore.Qt.AlignCenter)
        self.label_plot.setObjectName("label_plot")
        # Left Hand QWP Setpoint Label
        self.label_left = QtWidgets.QLabel(self.centralwidget)
        self.label_left.setGeometry(QtCore.QRect(320+5, 50, 81, 41))
        self.label_left.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_left.setAlignment(QtCore.Qt.AlignCenter)
        self.label_left.setObjectName("label_left")
        # Right Hand QWP Setpoint Label
        self.label_right = QtWidgets.QLabel(self.centralwidget)
        self.label_right.setGeometry(QtCore.QRect(320+2*320/4+5, 50, 81, 41))
        self.label_right.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_right.setAlignment(QtCore.Qt.AlignCenter)
        self.label_right.setObjectName("label_right")

        # Power Supply Control 1
        self.ps1spinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ps1spinBox.setGeometry(QtCore.QRect(110, 320, 100, 40))
        self.ps1spinBox.setFont(font)
        self.ps1spinBox.setDecimals(3)
        self.ps1spinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ps1spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.ps1spinBox.setKeyboardTracking(False)
        self.ps1spinBox.setMinimum(0.0)
        self.ps1spinBox.setMaximum(20.0)
        self.ps1spinBox.setProperty("value", 0.0)
        self.ps1spinBox.setObjectName("ps1spinBox")
        # Power Supply Readout 1
        self.ps1readspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ps1readspinBox.setGeometry(QtCore.QRect(210, 320, 100, 40))
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
        self.ps2spinBox.setGeometry(QtCore.QRect(430, 320, 100, 40))
        self.ps2spinBox.setFont(font)
        self.ps2spinBox.setDecimals(3)
        self.ps2spinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ps2spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.ps2spinBox.setKeyboardTracking(False)
        self.ps2spinBox.setMinimum(0.0)
        self.ps2spinBox.setMaximum(20.0)
        self.ps2spinBox.setProperty("value", 0.0)
        self.ps2spinBox.setObjectName("ps2spinBox")
        # Power Supply Readout 2
        self.ps2readspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ps2readspinBox.setGeometry(QtCore.QRect(530, 320, 100, 40))
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
        self.cellspinBox.setGeometry(QtCore.QRect(110, 500, 100, 40))
        self.cellspinBox.setFont(font)
        self.cellspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.cellspinBox.setStyleSheet("color: red;")
        self.cellspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.cellspinBox.setKeyboardTracking(False)
        self.cellspinBox.setMinimum(0.0)
        self.cellspinBox.setMaximum(250.0)
        self.cellspinBox.setProperty("value", 20.0)
        self.cellspinBox.setObjectName("cellspinBox")

        # Oven Wall Control
        self.ovenspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ovenspinBox.setGeometry(QtCore.QRect(430, 500, 100, 40))
        self.ovenspinBox.setFont(font)
        self.ovenspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ovenspinBox.setStyleSheet("color: lightgrey;")
        self.ovenspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.ovenspinBox.setKeyboardTracking(False)
        self.ovenspinBox.setMinimum(0.0)
        self.ovenspinBox.setMaximum(250.0)
        self.ovenspinBox.setProperty("value", 20.0)
        self.ovenspinBox.setObjectName("ovenspinBox")

        # Laser Output Control
        self.lasspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.lasspinBox.setGeometry(QtCore.QRect(110, 675, 100, 40))
        self.lasspinBox.setFont(font)
        self.lasspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.lasspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.lasspinBox.setMinimum(0.0)
        self.lasspinBox.setMaximum(45.0)
        self.lasspinBox.setProperty("value", 0.0)
        self.lasspinBox.setObjectName("lasspinBox")

        # Laser Ramp Rate Control
        self.rampspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.rampspinBox.setGeometry(QtCore.QRect(110, 725, 100, 40))
        self.rampspinBox.setFont(font)
        self.rampspinBox.setSingleStep(0.1)
        self.rampspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.rampspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.rampspinBox.setMinimum(0.0)
        self.rampspinBox.setMaximum(1.0)
        self.rampspinBox.setProperty("value", 0.1)
        self.rampspinBox.setObjectName("rampspinBox")

        # AFP repeating timer spinbox
        self.afptime = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.afptime.setGeometry(QtCore.QRect(480, 800, 100, 41))
        self.afptime.setFont(font)
        self.afptime.setSingleStep(1)
        self.afptime.setDecimals(0)
        self.afptime.setAlignment(QtCore.Qt.AlignHCenter)
        self.afptime.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.afptime.setMinimum(10)
        self.afptime.setMaximum(1800)
        self.afptime.setProperty("value", 60)
        self.afptime.setObjectName("afptime")

        # AFP Center Frequency
        self.FcentspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.FcentspinBox.setGeometry(QtCore.QRect(110, 855, 100, 40))
        self.FcentspinBox.setFont(font)
        self.FcentspinBox.setSingleStep(1.0)
        self.FcentspinBox.setDecimals(0)
        self.FcentspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.FcentspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.FcentspinBox.setMinimum(0.0)
        self.FcentspinBox.setMaximum(50000)
        self.FcentspinBox.setProperty("value", 37500)
        self.FcentspinBox.setObjectName("FcentspinBox")

        # AFP FWHM
        self.FWHMspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.FWHMspinBox.setGeometry(QtCore.QRect(110, 900, 100, 40))
        self.FWHMspinBox.setFont(font)
        self.FWHMspinBox.setSingleStep(1.0)
        self.FWHMspinBox.setDecimals(0)
        self.FWHMspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.FWHMspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.FWHMspinBox.setMinimum(0.0)
        self.FWHMspinBox.setMaximum(20000)
        self.FWHMspinBox.setProperty("value", 6000)
        self.FWHMspinBox.setObjectName("FWHMspinBox")

        # AFP Sweeprate
        self.SweepspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.SweepspinBox.setGeometry(QtCore.QRect(320, 855, 100, 40))
        self.SweepspinBox.setFont(font)
        self.SweepspinBox.setSingleStep(1.0)
        self.SweepspinBox.setDecimals(0)
        self.SweepspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.SweepspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.SweepspinBox.setMinimum(0.0)
        self.SweepspinBox.setMaximum(1000)
        self.SweepspinBox.setProperty("value", 100)
        self.SweepspinBox.setObjectName("SweepspinBox")

        # AFP RF Amplitude
        self.RFampspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.RFampspinBox.setGeometry(QtCore.QRect(320, 900, 100, 40))
        self.RFampspinBox.setFont(font)
        self.RFampspinBox.setSingleStep(0.1)
        self.RFampspinBox.setDecimals(1)
        self.RFampspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.RFampspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.RFampspinBox.setMinimum(0.0)
        self.RFampspinBox.setMaximum(10.0)
        self.RFampspinBox.setProperty("value", 2.0)
        self.RFampspinBox.setObjectName("RFampspinBox")

        # Plot enable
        self.plotEnable = QtWidgets.QCheckBox(self.centralwidget)
        self.plotEnable.setGeometry(QtCore.QRect(600, 890, 41, 16))
        self.plotEnable.setObjectName("plotEnable")

        # Cell Wall Readout
        self.cellreadout = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.cellreadout.setGeometry(QtCore.QRect(110, 550, 100, 40))
        self.cellreadout.setFont(font)
        self.cellreadout.setReadOnly(True)
        self.cellreadout.setMinimum(0.0)
        self.cellreadout.setMaximum(300.0)
        self.cellreadout.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.cellreadout.setAlignment(QtCore.Qt.AlignHCenter)
        self.cellreadout.setStyleSheet("color: red;")
        self.cellreadout.setObjectName("cellreadout")

        # Oven Wall Readout
        self.ovenreadout = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ovenreadout.setGeometry(QtCore.QRect(430, 550, 100, 40))
        self.ovenreadout.setFont(font)
        self.ovenreadout.setReadOnly(True)
        self.ovenreadout.setMinimum(0.0)
        self.ovenreadout.setMaximum(300.0)
        self.ovenreadout.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ovenreadout.setAlignment(QtCore.Qt.AlignHCenter)
        self.ovenreadout.setStyleSheet("color: lightgrey;")
        self.ovenreadout.setObjectName("ovenreadout")

        # Photodiode 1 Readout
        self.pdreadout = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.pdreadout.setGeometry(QtCore.QRect(430, 675, 100, 40))
        self.pdreadout.setFont(font)
        self.pdreadout.setReadOnly(True)
        self.pdreadout.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.pdreadout.setAlignment(QtCore.Qt.AlignHCenter)
        self.pdreadout.setStyleSheet("color: black;")
        self.pdreadout.setObjectName("pdreadout")

        # Photodiode 2 Readout
        self.pd2readout = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.pd2readout.setGeometry(QtCore.QRect(430, 725, 100, 40))
        self.pd2readout.setFont(font)
        self.pd2readout.setReadOnly(True)
        self.pd2readout.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.pd2readout.setAlignment(QtCore.Qt.AlignHCenter)
        self.pd2readout.setStyleSheet("color: lightgrey;")
        self.pd2readout.setObjectName("pd2readout")

        # Laser Current Readout
        self.lasreadout = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.lasreadout.setGeometry(QtCore.QRect(210, 675, 100, 40))
        self.lasreadout.setFont(font)
        self.lasreadout.setReadOnly(True)
        self.lasreadout.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.lasreadout.setAlignment(QtCore.Qt.AlignHCenter)
        self.lasreadout.setStyleSheet("color: black;")
        self.lasreadout.setObjectName("lasreadout")

        # PS1 Output Enable
        self.ps1Out = QtWidgets.QPushButton(self.centralwidget)
        self.ps1Out.setGeometry(QtCore.QRect(90, 375, 140, 40))
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
        self.ps2Out.setGeometry(QtCore.QRect(410, 375, 140, 40))
        self.ps2Out.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;}")
        self.ps2Out.setFont(font2)
        self.ps2Out.setCheckable(True)
        self.ps2Out.setText("Output Enable")
        self.ps2Out.setObjectName("ps2Out")

        # Oven Toggle 
        self.oventog = QtWidgets.QPushButton(self.centralwidget)
        self.oventog.setGeometry(QtCore.QRect(270, 525, 100, 40))
        self.oventog.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:5px;}")
        self.oventog.setFont(font2)
        self.oventog.setCheckable(True)
        self.oventog.setText("Cell Wall")
        self.oventog.setObjectName("oventog")

        # Laser Ramp Control
        self.lasOut = MyButton(self.centralwidget, font2, QtCore.QRect(210, 725, 100, 40), "Ramp\nCurrent")
        self.anim = QtCore.QPropertyAnimation(self.lasOut, b"zcolor")
        self.anim.setDuration(750)
        self.anim.setLoopCount(1)
        self.anim.setStartValue(QtGui.QColor(0,0,0,0.5))
        self.anim.setKeyValueAt(0.1, QtGui.QColor("lightblue"))
        self.anim.setKeyValueAt(0.9, QtGui.QColor("lightblue"))
        self.anim.setEndValue(QtGui.QColor(0,0,0,0.5))

        # AFP Button
        self.AFPOut = MyButton(self.centralwidget, font2, QtCore.QRect(480, 900, 100, 40),"AFP")
        self.AFPOut.setEnabled(False)
        self.animAFP = QtCore.QPropertyAnimation(self.AFPOut, b"zcolor")
        self.animAFP.setDuration(750)
        self.animAFP.setLoopCount(1)
        self.animAFP.setStartValue(QtGui.QColor(0,0,0,0.5))
        self.animAFP.setKeyValueAt(0.1, QtGui.QColor("lightblue"))
        self.animAFP.setKeyValueAt(0.9, QtGui.QColor("lightblue"))
        self.animAFP.setEndValue(QtGui.QColor(0,0,0,0.5))

        # AFP Timer Button
        self.AFPTimerOut = QtWidgets.QPushButton(self.centralwidget)
        self.AFPTimerOut.setGeometry(QtCore.QRect(590, 803, 40, 35))
        self.AFPTimerOut.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:5px;}")
        self.AFPTimerOut.setFont(font2)
        self.AFPTimerOut.setCheckable(True)
        self.AFPTimerOut.setText("Run")
        self.AFPTimerOut.setObjectName("AFPTimerOut")

        # AFP Send Waveform
        self.AFPwave = QtWidgets.QPushButton(self.centralwidget)
        self.AFPwave.setGeometry(QtCore.QRect(480, 855, 100, 40))
        self.AFPwave.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:5px;}")
        self.AFPwave.setFont(font2)
        self.AFPwave.setCheckable(True)
        self.AFPwave.setText("Send New\nWaveform")
        self.AFPwave.setObjectName("AFPwave")

        # AFP Sequencing Dropdown Menu
        self.AFPDrop = QtWidgets.QComboBox(self.centralwidget)
        self.AFPDrop.setGeometry(QtCore.QRect(300, 803, 100, 35))
        self.AFPDrop.setStyleSheet("QPushButton {background-color: white; color: black; border-radius:5px;}")
        self.AFPDrop.setFont(font2)
        self.AFPDrop.addItem("10101010")
        self.AFPDrop.addItem("10010110")

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
        #self.homeEnable.setText(_translate("TapeDriveWindow", "Enable"))
        #self.groupBox_2.setTitle(_translate("TapeDriveWindow", "Step Size (deg)"))
        #self.verticalSlider.setToolTip(_translate("TapeDriveWindow", "<html><head/><body><p>Drag to change step size. Step will be set when slider is released.</p></body></html>"))
        self.label_4.setText(_translate("TapeDriveWindow", "HWP"))
        self.label_qwp.setText(_translate("TapeDriveWindow", "QWP"))
        self.label_5.setText(_translate("TapeDriveWindow", "Power Supply Control"))
        self.label_m.setText(_translate("TapeDriveWindow", "Main Field"))
        self.label_c.setText(_translate("TapeDriveWindow", "Compensation Field"))
        self.label_o.setText(_translate("TapeDriveWindow", "Oven Control"))
        self.label_afp.setText(_translate("TapeDriveWindow", "AFP Settings"))
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
        self.label_qr.setText(_translate("TapeDriveWindow", "Angle Readout"))
        self.label_cos.setText(_translate("TapeDriveWindow", "Current\nSetpoint (A)"))
        self.label_afptime.setText(_translate("TapeDriveWindow", "AFP\nTimer (s)"))
        # self.label_cosr.setText(_translate("TapeDriveWindow", "Current Readout (A)"))
        self.label_ms.setText(_translate("TapeDriveWindow", "Current\nSetpoint (A)"))
        # self.label_msr.setText(_translate("TapeDriveWindow", "Current Readout (A)"))
        self.label_afp1.setText(_translate("TapeDriveWindow", "Center Frequency\n(Hz)"))
        self.label_afp2.setText(_translate("TapeDriveWindow", "FWHM Frequency\n(Hz)"))
        self.label_afp3.setText(_translate("TapeDriveWindow", "Sweeprate\n(KHz/s)"))
        self.label_afp4.setText(_translate("TapeDriveWindow", "RF Amplitude\n(V)"))
        self.label_plot.setText(_translate("TapeDriveWindow", "Plot\nEnable"))
        self.label_left.setText(_translate("TapeDriveWindow", "Spin Down\nSetpoint"))
        self.label_right.setText(_translate("TapeDriveWindow", "Spin Up\nSetpoint"))
        self.actionQuit.setText(_translate("TapeDriveWindow", "Exit"))
        self.actionQuit.setShortcut(_translate("TapeDriveWindow", "Meta+Q"))
        self.actionNothingHere.setText(_translate("TapeDriveWindow", "NothingHere"))

import resources_rc