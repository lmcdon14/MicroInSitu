# Code adapted from Chris Baird's repository on github:
# cdbaird/TL-rotation-control


from PyQt5 import QtCore, QtGui, QtWidgets
from td_gui import Ui_TapeDriveWindow

import elliptec.tapedrive as td
import elliptec
import agilent as ag

class mainProgram(QtWidgets.QMainWindow, Ui_TapeDriveWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		
		self.tapedrive = td.Tapedrive()
		self.psus = ag.MagneticField()
		self.absCoords.setValue(self.tapedrive.motor.get_('position')%360)
		# Set default stepsize
		self.tapedrive.motor.set_('stepsize', 
			self.tapedrive.motor.deg_to_hex(self.verticalSlider.value()))
		
		self.btnForward.clicked.connect(self.forward)
		#self.btnForward.clicked.connect(self.absolute)
		self.btnBackward.clicked.connect(self.backward)
		self.btnHome.clicked.connect(self.home)

		self.verticalSlider.valueChanged.connect(self.on_slider_drag)
		self.verticalSlider.sliderReleased.connect(self.on_slider_release)
		self.spinBox.valueChanged.connect(self.on_spin_box)
		self.homeEnable.toggled.connect(self.home_button_toggle)

	def forward(self):
		pos = self.tapedrive.motor.do_('forward')
		if pos != 420:
			self.absCoords.setValue(pos)

	def backward(self):
		pos = self.tapedrive.motor.do_('backward')
		if pos != 420:
			self.absCoords.setValue(pos)

	def absolute(self):
		pos = self.tapedrive.motor.do_('absolute', data=self.tapedrive.motor.deg_to_hex(self.spinBox.value()))
		if pos != 420:
			self.absCoords.setValue(pos)

	def home(self):
		pos = self.tapedrive.motor.do_('home')
		if pos != 420:
			self.absCoords.setValue(pos)

	def on_slider_drag(self):
		val = self.verticalSlider.value()
		self.spinBox.setValue(val)

	def on_spin_box(self):
		val = self.spinBox.value()
		self.verticalSlider.setValue(val)
		cmd_val = self.tapedrive.motor.deg_to_hex(val)
		#print(cmd_val)
		self.tapedrive.motor.set_('stepsize', cmd_val)
		self.tapedrive.motor.get_('stepsize')

	def on_slider_release(self):
		val = self.verticalSlider.value()
		cmd_val = self.tapedrive.motor.deg_to_hex(val)
		#print(cmd_val)
		self.tapedrive.motor.set_('stepsize', cmd_val)
		self.tapedrive.motor.get_('stepsize')

	def home_button_toggle(self):
		self.btnHome.setEnabled(self.homeEnable.isChecked())
		


if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	tdgui = mainProgram()
	tdgui.show()
	sys.exit(app.exec_())



