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
        TapeDriveWindow.resize(640, 400)
        TapeDriveWindow.setMinimumSize(QtCore.QSize(640, 400))
        TapeDriveWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        TapeDriveWindow.setStyleSheet("TapeDriveWindow {qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))}")
        self.centralwidget = QtWidgets.QWidget(TapeDriveWindow)
        self.centralwidget.setObjectName("centralwidget")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resources/bw3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Resources/fw3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        # PS Label
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 25, 621, 41))
        self.label_5.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        # Main Field Setpoint Label
        self.label_ms = QtWidgets.QLabel(self.centralwidget)
        self.label_ms.setGeometry(QtCore.QRect(5, 125, 100, 41))
        self.label_ms.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_ms.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ms.setObjectName("label_ms")
<<<<<<< HEAD
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
        # Amplitude Modulation Enable Label
        self.label_am = QtWidgets.QLabel(self.centralwidget)
        self.label_am.setGeometry(QtCore.QRect(415, 850, 71, 41))
        self.label_am.setStyleSheet("QLabel {font-size: 12x; color: black; border-radius: 5px;}")
        self.label_am.setAlignment(QtCore.Qt.AlignCenter)
        self.label_am.setObjectName("label_am")
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

=======
        
>>>>>>> 9bc73b2297c976af1f6984f6a20b3e003ffd5608
        # Power Supply Control 1
        self.ps1spinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ps1spinBox.setGeometry(QtCore.QRect(110, 130, 100, 40))
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
        self.ps1readspinBox.setGeometry(QtCore.QRect(210, 130, 100, 40))
        self.ps1readspinBox.setFont(font)
        self.ps1readspinBox.setReadOnly(True)
        self.ps1readspinBox.setDecimals(3)
        self.ps1readspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ps1readspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ps1readspinBox.setMinimum(0.0)
        self.ps1readspinBox.setMaximum(20.0)
        self.ps1readspinBox.setProperty("value", 0.0)
        self.ps1readspinBox.setObjectName("ps1readspinBox")

<<<<<<< HEAD
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
        self.lasspinBox.setMaximum(47.5)
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
        self.afptime.setMinimum(2)
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
        # Amplitude modulation enable
        self.amEnable = QtWidgets.QCheckBox(self.centralwidget)
        self.amEnable.setGeometry(QtCore.QRect(441, 890, 41, 16))
        self.amEnable.setObjectName("amenable")
        self.amEnable.setChecked(True)

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

=======
>>>>>>> 9bc73b2297c976af1f6984f6a20b3e003ffd5608
        # PS1 Output Enable
        self.ps1Out = QtWidgets.QPushButton(self.centralwidget)
        self.ps1Out.setGeometry(QtCore.QRect(320, 130, 140, 40))
        self.ps1Out.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;}")
        font2 = font
        font2.setPointSize(11)
        font2.setBold(False)
        self.ps1Out.setFont(font2)
        self.ps1Out.setCheckable(True)
        self.ps1Out.setText("Output Enable")
        self.ps1Out.setObjectName("ps1Out")

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
        TapeDriveWindow.setWindowTitle(_translate("TapeDriveWindow", "Lakeshore 625 Control"))
        self.label_5.setText(_translate("TapeDriveWindow", "Lakeshore 625"))
        self.label_ms.setText(_translate("TapeDriveWindow", "Current\nSetpoint (A)"))
<<<<<<< HEAD
        # self.label_msr.setText(_translate("TapeDriveWindow", "Current Readout (A)"))
        self.label_afp1.setText(_translate("TapeDriveWindow", "Center Frequency\n(Hz)"))
        self.label_afp2.setText(_translate("TapeDriveWindow", "FWHM Frequency\n(Hz)"))
        self.label_afp3.setText(_translate("TapeDriveWindow", "Sweeprate\n(KHz/s)"))
        self.label_afp4.setText(_translate("TapeDriveWindow", "RF Amplitude\n(V)"))
        self.label_plot.setText(_translate("TapeDriveWindow", "Plot\nEnable"))
        self.label_am.setText(_translate("TapeDriveWindow", "AM"))
        self.label_left.setText(_translate("TapeDriveWindow", "Spin Down\nSetpoint"))
        self.label_right.setText(_translate("TapeDriveWindow", "Spin Up\nSetpoint"))
=======
>>>>>>> 9bc73b2297c976af1f6984f6a20b3e003ffd5608
        self.actionQuit.setText(_translate("TapeDriveWindow", "Exit"))
        self.actionQuit.setShortcut(_translate("TapeDriveWindow", "Meta+Q"))
        self.actionNothingHere.setText(_translate("TapeDriveWindow", "NothingHere"))

import resources_rc