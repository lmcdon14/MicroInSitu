from PyQt5 import QtCore, QtGui, QtWidgets
from td_gui import Ui_TapeDriveWindow

import elliptec.tapedrive as td
import elliptec

class mainProgram(QtWidgets.QMainWindow, Ui_TapeDriveWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.tapedrive = td.Tapedrive()
		# Set default stepsize
		self.tapedrive.motor.set_('stepsize', 
			self.tapedrive.motor.deg_to_hex(self.verticalSlider.value()))

		self.btnForward.clicked.connect(self.forward)
		self.btnBackward.clicked.connect(self.backward)
		self.btnHome.clicked.connect(self.home)
		self.btnIsolate.clicked.connect(self.isolate)

		self.verticalSlider.valueChanged.connect(self.on_slider_drag)
		self.verticalSlider.sliderReleased.connect(self.on_slider_release)
		self.homeEnable.toggled.connect(self.home_button_toggle)
		self.IsolateEnable.toggled.connect(self.isolate_button_toggle)

	def forward(self):
		self.tapedrive.motor.do_('forward')

	def backward(self):
		self.tapedrive.motor.do_('backward')

	def home(self):
		self.tapedrive.motor.do_('home')

	def isolate(self):
		self.tapedrive.motor.set_('isolate', '01')

	def on_slider_drag(self):
		val = self.verticalSlider.value()
		self.spinBox.setValue(val)

	def on_slider_release(self):
		val = self.verticalSlider.value()
		cmd_val = self.tapedrive.motor.deg_to_hex(val)
		#print(cmd_val)
		self.tapedrive.motor.set_('stepsize', self.tapedrive.motor.deg_to_hex(val))
		self.tapedrive.motor.get_('stepsize')

	def home_button_toggle(self):
		self.btnHome.setEnabled(self.homeEnable.isChecked())

	def isolate_button_toggle(self):
		self.btnIsolate.setEnabled(self.IsolateEnable.isChecked())
		


if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	tdgui = mainProgram()
	tdgui.show()
	sys.exit(app.exec_())



