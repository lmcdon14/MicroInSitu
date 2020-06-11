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
		
		#self.tapedrive = td.Tapedrive()
		self.Field = ag.MagneticField()
		self.psus = self.Field.psus

		#self.absCoords.setValue(self.tapedrive.motor.get_('position')%360)
		# Set default stepsize
		#self.tapedrive.motor.set_('stepsize', 
			#self.tapedrive.motor.deg_to_hex(self.verticalSlider.value()))
		
		self.btnForward.clicked.connect(self.forward)
		#self.btnForward.clicked.connect(self.absolute)
		self.btnBackward.clicked.connect(self.backward)
		self.btnHome.clicked.connect(self.home)

		self.verticalSlider.valueChanged.connect(self.on_slider_drag)
		self.verticalSlider.sliderReleased.connect(self.on_slider_release)
		self.spinBox.valueChanged.connect(self.on_spin_box)
		self.ps1spinBox.valueChanged.connect(self.on_ps1_box)
		self.ps2spinBox.valueChanged.connect(self.on_ps2_box)
		self.homeEnable.toggled.connect(self.home_button_toggle)
		self.ps1Out.toggled.connect(self.ps1enable)
		self.ps2Out.toggled.connect(self.ps2enable)
		self.oventog.toggled.connect(self.oventoggle)
		self.cellspinBox.valueChanged.connect(self.cellsetpoint)
		self.ovenspinBox.valueChanged.connect(self.ovensetpoint)

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

	def on_ps1_box(self):
		psu = self.Field.psus[0].psu
		val = self.ps1spinBox.value()
		psu.outputs[0].configure_current_limit('regulate', val)

	def on_ps2_box(self):
		psu = self.Field.psus[1].psu
		val = self.ps2spinBox.value()
		psu.outputs[0].configure_current_limit('regulate', val)

	def ps1enable(self):
		psu = self.Field.psus[0].psu
		# if button is checked 
		if self.ps1Out.isChecked(): 
			# setting background color to light-blue 
			self.ps1Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
			psu.outputs[0].enabled = True
			if psu.outputs[0].enabled == True:
				print("Main field enabled.")
			else:
				print("Main field failed to turn on.")

		# if it is unchecked 
		else:
			# set background color back to light-grey 
			self.ps1Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;") 
			psu.outputs[0].enabled = False
			if psu.outputs[0].enabled == False:
				print("Main field disabled.")
			else:
				print("Main field failed to turn off.")

	def ps2enable(self):
		psu = self.Field.psus[1].psu
		# if button is checked 
		if self.ps2Out.isChecked(): 
			# setting background color to light-blue 
			self.ps2Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
			psu.outputs[0].enabled = True
			if psu.outputs[0].enabled == True:
				print("Compensation field enabled.")
			else:
				print("Compensation field failed to turn on.")

		# if it is unchecked 
		else:
			# set background color back to light-grey 
			self.ps2Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;") 
			psu.outputs[0].enabled = False
			if psu.outputs[0].enabled == False:
				print("Compensation field disabled.")
			else:
				print("Compensation field failed to turn off.")

	def oventoggle(self):
		if self.oventog.isChecked(): 
			self.oventog.setText("Oven Wall") 
			self.cellspinBox.setStyleSheet("color: lightgrey;")
			self.ovenspinBox.setStyleSheet("color: red;")
			self.cellreadout.setStyleSheet("color: lightgrey;")
			self.ovenreadout.setStyleSheet("color: red;")
			# Toggle thermocouple relay back to oven wall
			# Set heater setpoint to the value at self.ovenspinBox

		else:
			self.oventog.setText("Cell Wall") 
			self.ovenspinBox.setStyleSheet("color: lightgrey;")
			self.cellspinBox.setStyleSheet("color: red;")
			self.ovenreadout.setStyleSheet("color: lightgrey;")
			self.cellreadout.setStyleSheet("color: red;")
			# Toggle thermocouple relay back to cell wall
			# Set heater setpoint to the value at self.cellspinBox

	def ovensetpoint(self):
		if self.oventog.isChecked():
			# Change heater setpoint to new value at self.ovenspinBox
			setpoint = self.ovenspinBox.value()

	def cellsetpoint(self):
		if not self.oventog.isChecked():
			# Change heater setpoint to new value at self.cellspinBox
			setpoint = self.cellspinBox.value()

	def on_slider_release(self):
		val = self.verticalSlider.value()
		cmd_val = self.tapedrive.motor.deg_to_hex(val)
		#print(cmd_val)
		self.tapedrive.motor.set_('stepsize', cmd_val)
		self.tapedrive.motor.get_('stepsize')

	def home_button_toggle(self):
		self.btnHome.setEnabled(self.homeEnable.isChecked())

	def closeEvent(self, event):
		# here you can terminate your threads and do other stuff
		# turn off all power supplies
		for psu in self.psus:
			for output in psu.psu.outputs:
				output.enabled = True
			psu.psu.close()
		# and afterwards call the closeEvent of the super-class
		super(QtWidgets.QMainWindow, self).closeEvent(event)
		


if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	tdgui = mainProgram()
	tdgui.show()
	sys.exit(app.exec_())



