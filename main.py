# Code adapted from Chris Baird's repository on github:
# cdbaird/TL-rotation-control


from PyQt5 import QtCore, QtGui, QtWidgets
from td_gui import Ui_TapeDriveWindow
import elliptec.tapedrive as td
import elliptec
import agilent as ag
from PyExpLabSys.drivers.omega_cni import CNi3244_C24 as cni
from genesys.genesys_project import serialPorts, mySerial, DataContainer, ComSerial

class mainProgram(QtWidgets.QMainWindow, Ui_TapeDriveWindow):
	def __init__(self, simulate=False):
		super().__init__()
		self.setupUi(self)
		self.sim = simulate
		self.i=0
		self.mySerial = ComSerial(sim=simulate)
		self.mySerial.QuerySetupGUI()   
		self.mySerial.QueryRefreshGUI()

		exitAction = QtWidgets.QAction(QtGui.QIcon('pics/exit.png'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit/Terminate application')
		exitAction.triggered.connect(self.close)
		menubar = self.menuBar
		menubar.setNativeMenuBar(False)
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAction)

		oven_port = '/dev/ttyUSB0'
		laser_port = 'COM7'
		laser_baud = '9600'
		laser_add = '6'

		if simulate==False:
			#self.tapedrive = td.Tapedrive()
			#self.absCoords.setValue(self.tapedrive.motor.get_('position')%360)
			# Set default stepsize
			#self.tapedrive.motor.set_('stepsize', 
				#self.tapedrive.motor.deg_to_hex(self.verticalSlider.value()))
			#self.oven = cni(oven_port)
			print("Start connection to laser port.")
			self.mySerial.SetComPort(laser_port)
			self.mySerial.SetComSpeed(laser_baud)
			self.mySerial.SetComAddress(laser_add)
			print("Connecting to port.")
			self.mySerial.ConnectPort()
			print("Connecting to device.")
			self.mySerial.ConnectDevice()
			print("Start connection to laser device.")
		
		#self.Field = ag.MagneticField(simulate=True)
		self.Field = ag.MagneticField(simulate=simulate)
		self.psus = self.Field.psus
		
		self.btnForward.clicked.connect(self.forward)
		# self.btnForward.clicked.connect(self.absolute)
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
		self.lasOut.clicked.connect(self.lasRamp)
		
		self.timer = QtCore.QTimer()
		self.timer.setInterval(1000)
		self.timer.timeout.connect(self.recurring_timer)
		self.timer.start()

		self.lasint = 1000
		self.ramptimer = QtCore.QTimer()
		self.ramptimer.setInterval(self.lasint)
		self.ramptimer.timeout.connect(self.ramptimeout)
		self.lasprev = 0
		self.lasdelta = 0.01 # Allowable threshold for laser power supply to be off from setpoint to avoid infinite looping
		self.failflag = 0

	def forward(self):
		if self.sim == False:
			pos = self.tapedrive.motor.do_('forward')
			if pos != 420:
				self.absCoords.setValue(pos)
		else:
			oldVal = self.absCoords.value()
			step = self.spinBox.value()
			self.absCoords.setValue((oldVal + step)%360)

	def backward(self):
		if self.sim == False:
			pos = self.tapedrive.motor.do_('backward')
			if pos != 420:
				self.absCoords.setValue(pos)
		else:
			oldVal = self.absCoords.value()
			step = self.spinBox.value()
			self.absCoords.setValue((oldVal - step)%360)

	def absolute(self):
		if self.sim == False:
			pos = self.tapedrive.motor.do_('absolute', data=self.tapedrive.motor.deg_to_hex(self.spinBox.value()))
			if pos != 420:
				self.absCoords.setValue(pos)
		else:
			self.absCoords.setValue(self.spinBox.value())

	def home(self):
		if self.sim == False:
			pos = self.tapedrive.motor.do_('home')
			if pos != 420:
				self.absCoords.setValue(pos)
		else:
			self.absCoords.setValue(0)

	def on_slider_drag(self):
		val = self.verticalSlider.value()
		self.spinBox.setValue(val)

	def on_spin_box(self):
		val = self.spinBox.value()
		self.verticalSlider.setValue(val)
		if self.sim == False:
			cmd_val = self.tapedrive.motor.deg_to_hex(val)
			#print(cmd_val)
			self.tapedrive.motor.set_('stepsize', cmd_val)
			self.tapedrive.motor.get_('stepsize')

	def on_ps1_box(self):
		psu = self.Field.psus[0].psu
		val = self.ps1spinBox.value()
		psu.outputs[0].configure_current_limit('regulate', val)
		psu.outputs[0].current_limit = val
		
		#if psu.outputs[0].query_output_state(state='constant_current'):
		print("Main field set to {:3.2f}A with constant current.".format(val))
		#else:
			#print("Main field set to {:3.2f}A with constant voltage.".format(val))

	def on_ps2_box(self):
		psu = self.Field.psus[1].psu
		val = self.ps2spinBox.value()
		psu.outputs[0].configure_current_limit('regulate', val)
		psu.outputs[0].current_limit = val

		#if psu.outputs[0].query_output_state(state='constant_current'):
		print("Compensation field set to {:3.2f}A with constant current.".format(val))
		#else:
			#print("Compensation field set to {:3.2f}A with constant voltage.".format(val))

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
			print("Oven wall setpoint being used.")
			# Toggle thermocouple relay back to oven wall
			# Set heater setpoint to the value at self.ovenspinBox

		else:
			self.oventog.setText("Cell Wall") 
			self.ovenspinBox.setStyleSheet("color: lightgrey;")
			self.cellspinBox.setStyleSheet("color: red;")
			self.ovenreadout.setStyleSheet("color: lightgrey;")
			self.cellreadout.setStyleSheet("color: red;")
			print("Cell wall setpoint being used.")
			# Toggle thermocouple relay back to cell wall
			# Set heater setpoint to the value at self.cellspinBox

	def ovensetpoint(self):
		if self.oventog.isChecked():
			# Change heater setpoint to new value at self.ovenspinBox
			if self.sim == False:
				setpoint = self.ovenspinBox.value()
				self.oven.command('rw' + str(int(setpoint)))

	def cellsetpoint(self):
		if not self.oventog.isChecked():
			# Change heater setpoint to new value at self.cellspinBox
			if self.sim == False:
				setpoint = self.cellspinBox.value()
				self.oven.command('rw' + str(int(setpoint)))

	def lasRamp(self):
		# if another setpoint is still being ramped toward stop that timer and ramp toward new setpoint
		if self.ramptimer.isActive():
			self.ramptimer.stop()
		if self.sim==False:
			if not self.mySerial.QueryOUT():
				self.mySerial.SetOutputON()
		# Begin ramping laser
		self.failflag = 0
		self.ramptimer.start()
		print('Laser ramping to {:4.2f}A at {:4.2f}A/s.'.format(self.lasspinBox.value(), self.rampspinBox.value()))
		self.anim.start()

	def ramptimeout(self):
		if self.sim==False:
			self.mySerial.QuerySTT()
			self.lasreadout.setValue(self.mySerial.GenData.MC)
			lasval = self.mySerial.GenData.MC
		else:
			self.lasreadout.setValue(self.lasprev)
			lasval = self.lasprev
		# Once 10 failures to ramp have occurred, stop timer and report failure.
		if self.failflag >= 10:
			print("Ramp request timeout.")
			self.ramptimer.stop()
		# Otherwise continue to attempt to ramp
		else:
			# if current laser readout is within allowable tolerance of previous command...
			if abs(lasval - self.lasprev) < self.lasdelta:
				# check if current laser readout is within tolerance of overall setpoint
				if abs(lasval - self.lasspinBox.value()) > self.lasdelta:
					# if not check if the difference in current value and setpoint is less than allowable change for 
					# given maximum ramp rate
					dif = self.lasspinBox.value()-lasval
					if abs(dif) < self.rampspinBox.value()/(1000/self.lasint):
						# if ramp rate not exceeded, set power supply current to desired setpoint
						if self.sim==False:
							if self.mySerial.SetCurrent(self.lasspinBox.value()):
								if not self.failflag > 1:
									print("Final ramp setting applied.")
								self.lasprev = self.lasspinBox.value()
							else:
								if not self.failflag > 1:
									print("Failed to continue ramping.")
								self.failflag += 1
						else:
							self.lasprev = self.lasspinBox.value()
					else:
						# if ramp rate would have been exceeded, change the current value by the maximum allowable 
						# amount for the given ramp rate
						if lasval > self.lasspinBox.value():
							if self.sim==False:
								if not self.mySerial.SetCurrent(self.lasprev-self.rampspinBox.value()/(1000/self.lasint)):
									if not self.failflag > 1:
										print("Failed to continue ramping.")
									self.failflag += 1
								else:
									self.lasprev = self.lasprev-self.rampspinBox.value()/(1000/self.lasint)
							else:
								self.lasprev = self.lasprev-self.rampspinBox.value()/(1000/self.lasint)
						else:
							if self.sim==False:
								if not self.mySerial.SetCurrent(self.lasprev+self.rampspinBox.value()/(1000/self.lasint)):
									if not self.failflag > 1:
										print("Failed to continue ramping.")
									self.failflag += 1
								else:
									self.lasprev = self.lasprev+self.rampspinBox.value()/(1000/self.lasint)
							else:
								self.lasprev = self.lasprev+self.rampspinBox.value()/(1000/self.lasint)
				else:
					# desired current setting reached
					self.lasprev = lasval
					self.ramptimer.stop()
					if lasval < self.lasdelta:
						if self.sim==False:
							if self.mySerial.SetOutputOFF():
								print("Laser turned off.")
							else:
								print("Laser failed to turn off.")
						else:
							print("Laser turned off.")
					else:
						print("Desired laser current reached.")
			# else wait for current to stabilize to previous laser setting before updating current setpoint

	def on_slider_release(self):
		val = self.verticalSlider.value()
		if self.sim==False:
			cmd_val = self.tapedrive.motor.deg_to_hex(val)
			#print(cmd_val)
			self.tapedrive.motor.set_('stepsize', cmd_val)
			self.tapedrive.motor.get_('stepsize')

	def home_button_toggle(self):
		self.btnHome.setEnabled(self.homeEnable.isChecked())

	def recurring_timer(self):
		# Update laser current readout
		# self.lasReadout.setValue(self.las.value())

		#Update power supply readouts
		if self.sim==False:
			self.ps1readspinBox = psus[0].psu.output[0].measure('current')
			self.ps2readspinBox = psus[1].psu.output[0].measure('current')

		# Update photodiode readouts
		# self.pdreadout.setValue(self.pds[0].value())
		# self.pd2readout.setValue(self.pds[1].value())

		# Update oven readout (cell/wall)
		if self.oventog.isChecked(): 
			# self.ovenreadout.setValue(self.oven.read_temperature())
			self.ovenreadout.setValue(self.i)

		else:
			# self.cellreadout.setValue(self.oven.read_temperature())
			self.cellreadout.setValue(self.i)
		
		self.i += 1


	def closeEvent(self, event):
		# here you can terminate your threads and do other stuff
		# turn off all power supplies
		for psu in self.psus:
			for output in psu.psu.outputs:
				output.enabled = False
			psu.psu.close()
			
		# close connection to omega controller
		if self.sim == False:
			self.oven.close()

		# and afterwards call the closeEvent of the super-class
		super(QtWidgets.QMainWindow, self).closeEvent(event)
		

if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	
	if len(sys.argv)>1:
		if sys.argv[1] == 'sim':
			tdgui = mainProgram(simulate=True)
		else:
			tdgui = mainProgram()
	else:
		tdgui = mainProgram()
	tdgui.show()
	sys.exit(app.exec_())