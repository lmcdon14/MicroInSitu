# Code adapted from Chris Baird's repository on github:
# cdbaird/TL-rotation-control


from PyQt5 import QtCore, QtGui, QtWidgets
from td_gui import Ui_TapeDriveWindow
import elliptec.tapedrive as td
import elliptec
#import agilent as ag
import serial
from PyExpLabSys.drivers.omega_cni import ISeries as cni
from genesys.genesys_project import serialPorts, mySerial, DataContainer, ComSerial
import instruments as ik
from instruments.abstract_instruments import FunctionGenerator
import quantities as pq
import math
import matplotlib.pyplot as plt
import array
import numpy as np
import nidaqmx
from nidaqmx.stream_writers import AnalogSingleChannelWriter
system = nidaqmx.system.system.System.local()
import pySMC100.smc100
import datetime
from os import path
import re
from pprint import pprint 
from pyModbusTCP.client import ModbusClient as mc

class mainProgram(QtWidgets.QMainWindow, Ui_TapeDriveWindow):
	def __init__(self, simulate=False):
		super().__init__()
		self.sim = simulate
		self.loaded = 0
		self.hardcode = True
		self.port_i = 0

		#function to go through all ports and print all properties
		if self.hardcode == False:
			self.printPortInfo()
		#once properties identified write if statements to determine which port is which
		if self.hardcode:
			self.smcport = None
			#self.smcport = 'COM19'
			#self.laser_port = 'COM10'
			self.laser_port = None
			#self.pdlock_port = 'COM11'
			self.pdlock_port = None
			#self.oven_port = 'COM9'
			self.oven_port = None
			#self.relay_port = 'COM13'
			self.relay_port = None
			#self.ps_ports = ['COM2', 'COM12', None]
			self.ps_ports = [None] * 3
			self.tc_addr = "192.168.127.247"
			#self.tc_addr = None
			self.daq = False
			#self.daq = True
		else:
			self.smcport = None
			self.oven_port = None
			self.pdlock_port = None
			self.relay_port = None
			self.laser_port = None
			self.ps_ports = [None]*3
			self.discoverPorts()

		self.tc = None

		#Connect Power Supplies
		#self.Field = ag.MagneticField(simulate=True)
		#self.Field = ag.MagneticField(simulate=simulate, ports=self.ps_ports)
		#self.psus = self.Field.psus
		self.psus = [None] *3
		#If there are 3 supplies power compensation coils separately
		if self.psus[2] == None:
			self.comps = 1
			if self.psus[1] == None:
				self.comps = 0
		else:
			self.comps = 2

		#Initialize GUI
		self.setupUi(self, comps = self.comps)
		if self.psus[0] != None:
			self.mainlabel.setPixmap(self.pixmap_green)
		if self.comps>0:
			self.complabel.setPixmap(self.pixmap_green)
		if self.comps==2:
			self.complabel2.setPixmap(self.pixmap_green)

		#Load parameters from previous run if config file exists
		if path.exists("Resources/Config.txt"):
			print("Loading parameters from last run\n")
			a_file = open("Resources/Config.txt", "r")
			list_of_lines = a_file.readlines()
			numbers = np.ones(len(list_of_lines))
			for ind, line in enumerate(list_of_lines):
				numbers[ind] = re.findall(r"[-+]?\d*\.\d+|\d+", line)[0]
			#print(numbers)
			a_file.close()

			# Set all loaded parameters
			if numbers[0] == 1:
				self.afp_bool = True
				self.afp_old = True
			else:
				self.afp_bool = False
				self.afp_old = False
			if self.afp_bool:
				self.spinlabel.setPixmap(self.pixmap_down)
			else:
				self.spinlabel.setPixmap(self.pixmap_up)
				
			self.QWP_right_pos.setProperty("value", int(numbers[1]))
			self.QWP_left_pos.setProperty("value", int(numbers[2]))
			self.HWP_opt_pos.setProperty("value", int(numbers[3]))
			self.FcentspinBox.setProperty("value", int(numbers[6]))
			self.FWHMspinBox.setProperty("value", int(numbers[7]))
			self.SweepspinBox.setProperty("value", int(numbers[8]))
			self.RFampspinBox.setProperty("value", float(numbers[9]))
			#Set loaded flag
			self.loaded = 1

		#Initialize other variables
		self.i=0
		self.las = '770'
		self.task = None
		self.trig_task = None
		self.trig_task2 = None
		self.digi_task = None
		if self.loaded == 0:
			self.afp_bool = False
			self.afp_old = False
		self.afp_ind = 0
		self._translate = QtCore.QCoreApplication.translate
		self.afpcount_int = 0
		self.afprun_int = 0
		self.afprun_int_count = 0
		self.lasprev = 0
		self.newport_motor = 0
		self.switch_state = 0

		#Define destructor function and other GUI parameters
		exitAction = QtWidgets.QAction(QtGui.QIcon('pics/exit.png'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit/Terminate application')
		exitAction.triggered.connect(self.close)
		menubar = self.menuBar
		menubar.setNativeMenuBar(False)
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAction)

		laser_baud = '9600'
		laser_add = '6'

		"""
		# Function Generator Code
		func_gen_port = 'COM8'
		self.srs = ik.srs.SRS345.open_serial(port=func_gen_port)
		self.srs.sendcmd('BCNT 1')
		self.srs.sendcmd('OFFS 0')
		self.srs.sendcmd('MENA 0')
		self.srs.sendcmd('MTYP 5')
		#self.srs.sendcmd('MDWF 5')
		self.srs.sendcmd('DPTH -100')
		"""

		if simulate==False:			
			#Connect rotation mount(s)
			self.tapedrive = td.Tapedrive()
			i=0
			for motor in self.tapedrive.motors:
				if motor != None:
					#Add logic to detect if position has changed between runs
					val = motor.get_('position')%360
					self.absCoords[i].setValue(val)
					self.absCoordset[i].setValue(val)
					if i==0:
						self.hwplabel.setPixmap(self.pixmap_green)
					else:
						self.qwplabel.setPixmap(self.pixmap_green)
					#motor.set_('stepsize', motor.deg_to_hex(self.verticalSlider.value()))
				i += 1

			#If there is only one Thorlabs rotation mount use Newport QWP mount (if one exists)
			if self.tapedrive.motors[1] == None:
				if self.smcport != None:
					self.qwplabel.setPixmap(self.pixmap_green)
					self.smc100 = pySMC100.smc100.SMC100(1, self.smcport, silent=True)
					self.smc100.home()
					val = self.smc100.get_position_mm()
					self.absCoords[1].setValue(val)
					self.absCoordset[1].setValue(val)

			#Connect TC Controller
			if self.tc_addr != None:
				self.tc = mc(host=self.tc_addr, port = 502, auto_open = True, auto_close = True)
				regs = self.tc.read_input_registers(12,4)
				if regs:
					print("Temps:\n1: " + str(regs[0]/10) + "\n2: " + str(regs[1]/10) + "\n3: " + str(regs[2]/10) + "\n4: " + str(regs[3]/10))
				else:
					print("read error")

			#Connect DAQ board
			if self.daq == True:
				if len(system.devices)>0:
					print(system.tasks.task_names)
					self.afplabel.setPixmap(self.pixmap_green)
					for device in system.devices:
						print(device)
					self.daq = system.devices[0]
					#Send waveform and set state pin if config file loaded
					#print("loading:" + str(self.loaded))
					if self.loaded == 1:
						self.AFPwave.clicked.connect(self.AFPSendWvfm)
						self.AFPwave.click()
						print("Setting spin state pin")
						if self.digi_writer.write_one_sample_one_line(self.afp_bool) == 1:
							if (self.afp_bool):
								print("Flipped spin")
							else:
								print("Original spin")
						else:
							print("Status bit unsuccessful")
					self.AFPOut.clicked.connect(self.AFP)
			
			#Connect Laser
			if self.laser_port != None:
				self.laslabel.setPixmap(self.pixmap_green)
				if self.las == '770':
					self.lasSer = ComSerial(sim=simulate)
					#self.lasSer.QuerySetupGUI()   
					#self.lasSer.QueryRefreshGUI()
					self.lasSer.SetComPort(self.laser_port)
					self.lasSer.SetComSpeed(laser_baud)
					self.lasSer.SetComAddress(laser_add)
					self.lasSer.ConnectPort()
					self.lasSer.ConnectDevice()
					self.lasSer.QuerySTT()
					self.lasprev = self.lasSer.GenData.MC
					self.lasreadout.setValue(self.lasSer.GenData.MC)
					self.lasspinBox.setValue(self.lasSer.GenData.MC)
				else:
					# 795nm QPC laser control (don't have the serial enabled power supply)
					self.lasSer = mySerial(port=self.laser_port, baudrate=9600, timeout=1, parity=serial.PARITY_NONE,
						stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
					self.lasSer.write(('I\r').encode())
					test=self.lasSer.readline()
					lasval=float(test.decode("utf-8"))
					self.lasreadout.setValue(lasval)
					self.lasprev = lasval
				self.lasOut.clicked.connect(self.lasRamp)

			# Connect Omega controllers
			if self.oven_port != None:
				self.ovenlabel.setPixmap(self.pixmap_green)
				self.oven = cni(self.oven_port, baudrate=9600)
				self.ovenspinBox.setValue(int(self.oven.command('R01').replace('2', '0', 1),16)/10)
				self.ovenspinBox.valueChanged.connect(self.ovensetpoint)

			if self.pdlock_port != None:
				self.pdlabel.setPixmap(self.pixmap_green)
				self.pdlock = cni(self.pdlock_port, baudrate=9600)
									
			#Connect oven relay and switch relay to cell wall
			if self.relay_port != None:
				self.ovenRelayPort = serial.Serial(self.relay_port, baudrate=9600, bytesize=8, stopbits=1, timeout=0.5)
				mybytes = bytearray()
				mybytes.append(254)
				mybytes.append(0)
				self.ovenRelayPort.write(mybytes)
				mybytes = bytearray()
				mybytes.append(254)
				mybytes.append(2)
				self.ovenRelayPort.write(mybytes)
				self.oventog.toggled.connect(self.oventoggle)
				self.cellspinBox.setValue(int(self.oven.command('R01').replace('2', '0', 1),16)/10)
				self.cellspinBox.valueChanged.connect(self.cellsetpoint)

		# Set parameters for power supplies
		if self.sim == False:
			if self.psus[0] != None:
				cur1 = self.psus[0].psu.outputs[0].measure('current')
				self.ps1readspinBox.setValue(cur1)
				self.ps1spinBox.setValue(cur1)
				if self.psus[0].psu.outputs[0].enabled:
					self.ps1Out.setChecked(True)
					self.ps1Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
				self.ps1spinBox.valueChanged.connect(self.on_ps1_box)
				self.ps1Out.toggled.connect(self.ps1enable)
			if self.comps > 0:
				cur2 = self.psus[1].psu.outputs[0].measure('current')
				self.ps2readspinBox.setValue(cur2)
				self.ps2spinBox.setValue(cur2)
				if self.psus[1].psu.outputs[0].enabled:
					self.ps2Out.setChecked(True)
					self.ps2Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
				self.ps2spinBox.valueChanged.connect(self.on_ps2_box)
				self.ps2Out.toggled.connect(self.ps2enable)
			if self.comps == 2:
				cur3 = self.psus[2].psu.outputs[0].measure('current')
				self.ps3readspinBox.setValue(cur3)
				self.ps3spinBox.setValue(cur3)
				if self.psus[2].psu.outputs[0].enabled:
					self.ps3Out.setChecked(True)
					self.ps3Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
				self.ps3spinBox.valueChanged.connect(self.on_ps3_box)
				self.ps3Out.toggled.connect(self.ps3enable)
				self.psswitch.clicked.connect(self.switch_ps)
		
		#self.btnForward.clicked.connect(self.forward)
		#self.btnForward.clicked.connect(self.absolute)
		#self.btnBackward.clicked.connect(self.backward)
		#self.btnHome.clicked.connect(self.home)
		#self.verticalSlider.valueChanged.connect(self.on_slider_drag)
		#self.verticalSlider.sliderReleased.connect(self.on_slider_release)
		#self.spinBox.valueChanged.connect(self.on_spin_box)
		#self.homeEnable.toggled.connect(self.home_button_toggle)

		if self.sim == False:
			self.absCoordset[0].valueChanged.connect(self.absolute1)
			if self.tapedrive.motors[1] != None:
				self.absCoordset[1].valueChanged.connect(self.absolute2)
				self.absCoordset[1].setMinimum(0)
				self.absCoordset[1].setMaximum(359)
				self.QWP_right_pos.setMinimum(0)
				self.QWP_right_pos.setMaximum(359)
				if self.loaded == 0:
					self.QWP_right_pos.setProperty("value", 46)
				self.QWP_left_pos.setMinimum(0)
				self.QWP_left_pos.setMaximum(359)
				if self.loaded == 0:
					self.QWP_left_pos.setProperty("value", 163)
			else:
				self.newport_motor = 1
				self.absCoordset[1].valueChanged.connect(self.newport)
				self.absCoordset[1].setMinimum(-165)
				self.absCoordset[1].setMaximum(165)
				self.QWP_right_pos.setMinimum(-165)
				self.QWP_right_pos.setMaximum(165)
				if self.loaded == 0:
					self.QWP_right_pos.setProperty("value", 130)
				self.QWP_left_pos.setMinimum(-165)
				self.QWP_left_pos.setMaximum(165)
				if self.loaded == 0:
					self.QWP_left_pos.setProperty("value", -130)
		else:
			self.absCoordset[0].valueChanged.connect(self.absolute1)
			self.absCoordset[1].valueChanged.connect(self.absolute2)
			self.absCoordset[1].setMinimum(0)
			self.absCoordset[1].setMaximum(359)
			self.QWP_right_pos.setMinimum(0)
			self.QWP_right_pos.setMaximum(359)
			if self.loaded == 0:
				self.QWP_right_pos.setProperty("value", 46)
			self.QWP_left_pos.setMinimum(0)
			self.QWP_left_pos.setMaximum(359)
			if self.loaded == 0:
				self.QWP_left_pos.setProperty("value", 163)
		#self.rotHome.clicked.connect(self.rotation_homing)
		self.rotHome2.clicked.connect(self.home)
		
		self.timer = QtCore.QTimer()
		self.timer.setInterval(5000)
		self.timer.timeout.connect(self.recurring_timer)
		self.timer.start()

		self.lasint = 1000
		self.ramptimer = QtCore.QTimer()
		self.ramptimer.setInterval(self.lasint)
		self.ramptimer.timeout.connect(self.ramptimeout)
		self.lasdelta = 0.01 # Allowable threshold for laser power supply to be off from setpoint to avoid infinite looping
		self.failflag = 0

		self.afptime.valueChanged.connect(self.timechange)
		self.afptimer = QtCore.QTimer()
		self.afptimer.setInterval(self.afptime.value())
		self.afptimer.timeout.connect(self.afptimeout)
		self.AFPTimerOut.clicked.connect(self.afptimerun)

	# Go through all ports and determine which devices are connected to each
	def discoverPorts(self):
		for port in self.ports:
			if "Laser" in port.description:
				self.laser_port = port
			elif "Newport" in port.description:
				self.smcport = port
			elif "Oven" in port.description:
				self.oven_port = port
			elif "PDlock" in port.description:
				self.pdlock_port = port
			elif "Relay" in port.description:
				self.relay_port = port
			elif "ps_port" in port.description:
				self.ps_ports[self.port_i] = port
				self.port_i += 1
				
	# Print all port info
	def printPortInfo(self):
		if self.sim==False:
			self.ports = ag.find_ports()
			#print(len(self.ports))
			for port in self.ports:
				print(port)
				pprint(vars(port), indent=2)
				#if port.serial_number in self.sns:
			
	"""
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
	"""

	def switch_ps(self):
		print("Switching compensation coils")
		if self.switch_state == 0:
			# Switch US to DS and v/v
			self.uslabel.setText(self._translate("TapeDriveWindow", "DS"))
			self.dslabel.setText(self._translate("TapeDriveWindow", "US"))
			self.switch_state = 1
		else:
			# Switch US and DS back to original locations
			self.dslabel.setText(self._translate("TapeDriveWindow", "DS"))
			self.uslabel.setText(self._translate("TapeDriveWindow", "US"))
			self.switch_state = 0

	def rotation_homing(self):
		self.animRot.start()
		if self.sim == False:
			if self.newport_motor == 0:
				loop = 2
			else:
				loop = 1

			for ind in range(loop):
				if self.tapedrive.motors[ind] != None:
					self.absCoordset[ind].setProperty("value", 336)
		else:
			self.absCoordset[0].setProperty("value",336)
			self.absCoordset[1].setProperty("value",336)

	def absolute1(self):
		ind = 0
		if self.sim == False:
			if self.tapedrive.motors[ind] != None:
				pos = self.tapedrive.motors[ind].do_('absolute', data=self.tapedrive.motors[ind].deg_to_hex(self.absCoordset[ind].value()))
				if pos != 420:
					self.absCoords[ind].setValue(pos)
		else:
			self.absCoords[ind].setValue(self.absCoordset[ind].value())
			
	def absolute2(self):
		ind = 1
		if self.sim == False:
			if self.tapedrive.motors[ind] != None:
				pos = self.tapedrive.motors[ind].do_('absolute', data=self.tapedrive.motors[ind].deg_to_hex(self.absCoordset[ind].value()))
				if pos != 420:
					self.absCoords[ind].setValue(pos)
		else:
			self.absCoords[ind].setValue(self.absCoordset[ind].value())

	def newport(self):
		if self.sim == False:
			self.smc100.move_absolute_mm(self.absCoordset[1].value())
			loc = self.smc100.get_position_mm()
			#print(loc)
			self.absCoords[1].setValue(loc)
		else:
			self.absCoords[1].setValue(self.absCoordset[1].value())
	
	def home(self):
		self.animRot2.start()
		if self.sim == False:
			if self.tapedrive.motors[0] != None:
				pos1 = self.tapedrive.motors[0].do_('home')
			else:
				pos1 = 420
			if self.tapedrive.motors[1] != None:
				pos2 = self.tapedrive.motors[1].do_('home')
			else:
				pos2 = 420

			if pos1 != 420:
				self.absCoords[0].setValue(pos1)
			if pos2 != 420:
				self.absCoords[1].setValue(pos2)
		else:
			self.absCoords[0].setValue(0)
			self.absCoords[1].setValue(0)
			self.absCoordset[0].setValue(0)
			self.absCoordset[1].setValue(0)

	"""
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
	"""

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
		if self.comps == 1:
			print("Compensation field set to {:3.2f}A with constant current.".format(val))
		else:
			if self.switch_state == 0:
				stream = "US"
			else:
				stream = "DS"
			print("{:s} compensation field set to {:3.2f}A with constant current.".format(stream, val))
		#else:
			#print("Compensation field set to {:3.2f}A with constant voltage.".format(val))

	def on_ps3_box(self):
		psu = self.Field.psus[2].psu
		val = self.ps3spinBox.value()
		psu.outputs[0].configure_current_limit('regulate', val)
		psu.outputs[0].current_limit = val

		#if psu.outputs[0].query_output_state(state='constant_current'):\
		if self.switch_state == 0:
			stream = "DS"
		else:
			stream = "US"
		print("{:s} compensation field set to {:3.2f}A with constant current.".format(stream, val))
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
		if self.comps == 1:
			stream = "C"
		else:
			if self.switch_state == 0:
				stream = "US c"
			else:
				stream = "DS c"
		# if button is checked 
		if self.ps2Out.isChecked(): 
			# setting background color to light-blue 
			self.ps2Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
			psu.outputs[0].enabled = True
			if psu.outputs[0].enabled == True:
				print(stream + "ompensation field enabled.")
			else:
				print(stream + "ompensation field failed to turn on.")

		# if it is unchecked 
		else:
			# set background color back to light-grey 
			self.ps2Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;") 
			psu.outputs[0].enabled = False
			if psu.outputs[0].enabled == False:
				print(stream + "ompensation field disabled.")
			else:
				print(stream + "ompensation field failed to turn off.")

	def ps3enable(self):
		psu = self.Field.psus[2].psu
		if self.switch_state == 1:
			stream = "US c"
		else:
			stream = "DS c"
		# if button is checked 
		if self.ps3Out.isChecked(): 
			# setting background color to light-blue 
			self.ps3Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
			psu.outputs[0].enabled = True
			if psu.outputs[0].enabled == True:
				print(stream + "ompensation field enabled.")
			else:
				print(stream + "ompensation field failed to turn on.")

		# if it is unchecked 
		else:
			# set background color back to light-grey 
			self.ps3Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;") 
			psu.outputs[0].enabled = False
			if psu.outputs[0].enabled == False:
				print(stream + "ompensation field disabled.")
			else:
				print(stream + "ompensation field failed to turn off.")

	def oventoggle(self):
		if self.oventog.isChecked(): 
			self.oventog.setText("Oven Wall") 
			self.cellspinBox.setStyleSheet("color: lightgrey;")
			self.ovenspinBox.setStyleSheet("color: red;")
			self.cellreadout.setStyleSheet("color: lightgrey;")
			self.ovenreadout.setStyleSheet("color: red;")
			print("Oven wall setpoint being used.")
			
			if self.sim == False:
				# Toggle thermocouple relay back to cell wall
				mybytes = bytearray()
				mybytes.append(254)
				mybytes.append(1)
				self.ovenRelayPort.write(mybytes)
				mybytes = bytearray()
				mybytes.append(254)
				mybytes.append(3)
				self.ovenRelayPort.write(mybytes)

				# Set heater setpoint to the value at self.ovenspinBox
				setpoint = self.ovenspinBox.value()
				setpoint_str = (int(setpoint*10).to_bytes(3, byteorder='big')).hex().upper()
				setpoint_str = setpoint_str.replace('0', '2', 1)
				#print(setpoint_str)
				self.oven.command('W01' + setpoint_str)
				#print(self.oven.command('R01'))

		else:
			self.oventog.setText("Cell Wall") 
			self.ovenspinBox.setStyleSheet("color: lightgrey;")
			self.cellspinBox.setStyleSheet("color: red;")
			self.ovenreadout.setStyleSheet("color: lightgrey;")
			self.cellreadout.setStyleSheet("color: red;")
			print("Cell wall setpoint being used.")
			
			if self.sim == False:
				# Toggle thermocouple relay back to cell wall
				mybytes = bytearray()
				mybytes.append(254)
				mybytes.append(0)
				self.ovenRelayPort.write(mybytes)
				mybytes = bytearray()
				mybytes.append(254)
				mybytes.append(2)
				self.ovenRelayPort.write(mybytes)

				# Set heater setpoint to the value at self.cellspinBox
				setpoint = self.cellspinBox.value()
				setpoint_str = (int(setpoint*10).to_bytes(3, byteorder='big')).hex().upper()
				setpoint_str = setpoint_str.replace('0', '2', 1)
				#print(setpoint_str)
				self.oven.command('W01' + setpoint_str)
				#print(self.oven.command('R01'))

	def ovensetpoint(self):
		if self.oventog.isChecked():
			# Change heater setpoint to new value at self.ovenspinBox
			if self.sim == False:
				setpoint = self.ovenspinBox.value()
				setpoint_str = (int(setpoint*10).to_bytes(3, byteorder='big')).hex().upper()
				setpoint_str = setpoint_str.replace('0', '2', 1)
				#print(setpoint_str)
				self.oven.command('W01' + setpoint_str)
				#print(self.oven.command('R01'))

	def cellsetpoint(self):
		if not self.oventog.isChecked():
			# Change heater setpoint to new value at self.cellspinBox
			if self.sim == False:
				setpoint = self.cellspinBox.value()
				setpoint_str = (int(setpoint*10).to_bytes(3, byteorder='big')).hex().upper()
				setpoint_str = setpoint_str.replace('0', '2', 1)
				#print(setpoint_str)
				self.oven.command('W01' + setpoint_str)
				#print(self.oven.command('R01'))

	def AFP(self):
		#Set new spin state value based on sequencing method used
		if self.AFPTimerOut.isChecked():
			#If spin is already flipped start the octet at the 5th index or the normal sequence at the 2nd index
			if self.afp_ind == 0 and self.afp_bool == True:
				if self.AFPDrop.currentIndex() == 1:
					self.afp_ind = 4
				else:
					self.afp_ind = 1
			#print(self.afp_ind)
			#print(self.AFPDrop.currentText()[self.afp_ind])
			if self.AFPDrop.currentText()[self.afp_ind] == "0":
				self.afp_bool = False
			else:
				self.afp_bool = True
			#print(self.afp_old)
			#print(self.afp_bool)
			#Increment index value
			self.afp_ind += 1
			if self.afp_ind == 8:
				self.afp_ind = 0 
		#If not using timed sequencing just flip spin to opposite value
		else:
			if self.afp_bool == False:
				self.afp_bool = True
			else:
				self.afp_bool = False

		self.afprun_int_count += 1
		self.afpcount3.setText(self._translate("TapeDriveWindow", str(self.afprun_int_count)))

		if self.afp_bool != self.afp_old:
			self.animAFP.start()
			if self.sim==False:
				# Analog workaround
				# if self.afp_bool:
				# 	val = 3
				# else:
				# 	val = 0

				print('Output triggered')
				if self.digi_writer.write_one_sample_one_line(self.afp_bool) == 1:
				#if self.digi_writer.write_one_sample(val):
					if (self.afp_bool):
						print("Flipped spin")
					else:
						print("Original spin")
				else:
					print("Status bit unsuccessful.")
				self.task.start()
				self.task.wait_until_done()
				self.task.stop()

				#Flip rotation of QWP
				if self.afp_bool == False:
					self.absCoordset[1].setProperty("value", self.QWP_right_pos.value())
				else:
					self.absCoordset[1].setProperty("value", self.QWP_left_pos.value())

				#Function generator code
				#self.srs.trigger()
			else:
				#print("Spin flipped")
				if (self.afp_bool):
					print("Flipped spin")
				else:
					print("Original spin")

				#Flip rotation of QWP
				if self.afp_bool == False:
					self.absCoordset[1].setProperty("value", self.QWP_right_pos.value())
				else:
					self.absCoordset[1].setProperty("value", self.QWP_left_pos.value())
		
			self.afpcount_int += 1
			self.afpcount2.setText(self._translate("TapeDriveWindow", str(self.afpcount_int)))

			if self.AFPTimerOut.isChecked():
				self.afprun_int += 1
				self.afpcount1.setText(self._translate("TapeDriveWindow", str(self.afprun_int)))
			
		#Set boolean value of current spin state
		self.afp_old = self.afp_bool

		if self.afp_bool:
			self.spinlabel.setPixmap(self.pixmap_down)
		else:
			self.spinlabel.setPixmap(self.pixmap_up)
	
	def test(self, *args):
		print("Triggering test successful")
		self.AFPOut.click()
		return 0

	def AFPSendWvfm(self):
		self.AFPwave.setStyleSheet("QPushButton {background-color: lightblue; color: white; border-radius:5px;}") 
		RFamp = self.RFampspinBox.value()
		FsweepRate = self.SweepspinBox.value()/1000.0
		Ffwhm = self.FWHMspinBox.value()
		Fcent = self.FcentspinBox.value()
		sample_rate = 1.0e6
		Fmin = 0.55*Fcent
		Fmax = 1.5*Fcent
		totaltime = (Fmax-Fmin)/(FsweepRate*1.0e6)
		npnts = int(totaltime*sample_rate+1)
		
		FsweepRate = FsweepRate/sample_rate*1.0e6
		#data = np.zeros(npnts, dtype='<i2')
		data = np.zeros(npnts)
		for x in range (npnts):
			# Freq = Fmin+FsweepRate*x
			# given code showed "=" instead of "+" below...
			# Amplitude = math.exp( (x-Fcent)^2/Ffwhm^2 ) = math.exp( -1* ((Fmin + FsweepRate*x)-Fcent)^2/Ffwhm^2 )
			# Note factor of 2 in rate to keep peak in correct place
			#val = int((32676*RFamp/10*math.exp(-1*(math.pow(((Fmin + FsweepRate*x)-Fcent),2)/(math.pow(Ffwhm,2))))*math.sin(2*math.pi*(Fmin +0.5*FsweepRate*x)*x))+0.5)
			if (self.amEnable.isChecked()):
				val = RFamp*math.exp(-1*(math.pow((Fmin + FsweepRate*x)-Fcent,2))/(math.pow(Ffwhm,2)))*math.sin(2*3.141592653589793238*(Fmin +0.5*FsweepRate*x)*(x/sample_rate))
				# Test function
				# val = RFamp*math.exp(-1*(math.pow((Fmin + FsweepRate*x)-Fcent,2))/(math.pow(Ffwhm,2)))*math.sin(1/2*3.141592653589793238)
			else:
				val = RFamp*math.sin(2*math.pi*(Fmin +0.5*FsweepRate*x)*x)
			#val = -RFamp+RFamp*2*x/npnts
			data[x] = val
			
		self.data = data

		if (self.plotEnable.isChecked()):
			plt.clf()
			plt.close()
			plt.plot(range(npnts), data, '-o')
			plt.title('AFP Function')
			plt.xlabel('Time (us)')
			plt.ylabel('Voltage (V)')
			plt.show()
			#print(np.amin(data), np.amax(data))
			
		if self.sim==False:
			if self.task != None:
				self.task.close()
				if self.trig_task != None:
					self.trig_task.close()
				if self.trig_task2 != None:
					self.trig_task2.close()
			else:
				self.AFPOut.setEnabled(True)
				self.digi_task = nidaqmx.task.Task()
				#self.digi_task.ao_channels.add_ao_voltage_chan("Dev1/ao1", min_val=0, max_val=5)
				self.digi_task.do_channels.add_do_chan("Dev1/port0/line7", line_grouping=nidaqmx.constants.LineGrouping.CHAN_PER_LINE)
				self.digi_writer = nidaqmx.stream_writers.DigitalSingleChannelWriter(self.digi_task.out_stream, auto_start=True)
				#self.digi_writer = nidaqmx.stream_writers.AnalogSingleChannelWriter(self.digi_task.out_stream, auto_start=True)

			self.task = nidaqmx.Task()
			self.task.ao_channels.add_ao_voltage_chan("Dev1/ao1", min_val=-RFamp, max_val=RFamp)
			self.task.timing.cfg_samp_clk_timing(sample_rate, sample_mode = nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=npnts)
			self.writer = AnalogSingleChannelWriter(self.task.out_stream)
			print("Successfully loaded " + str(self.writer.write_many_sample(data)) + " points")
			#self.task.register_done_event(self.test)
			#self.task.write(data, auto_start=False)
			#self.task.save(save_as='AFPTest', overwrite_existing_task=True, allow_interactive_editing=False)

			if self.trigEnable.isChecked():
			#if False:
				self.trig_task = nidaqmx.Task()
				self.trig_task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=nidaqmx.constants.TerminalConfiguration.DIFFERENTIAL)
				self.trig_task.timing.cfg_samp_clk_timing(1e6, active_edge=nidaqmx.constants.Edge.RISING, sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=2)
				print(self.trig_task.read())
				"""
				print("Enabling triggering with 0-5V")
				trig_dat = np.array([0, 1], dtype='uint32')
				self.trig_task = nidaqmx.Task()
				#self.trig_task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
				self.trig_task.do_channels.add_do_chan("Dev1/port0/line20", line_grouping=nidaqmx.constants.LineGrouping.CHAN_PER_LINE)
				#self.trig_task.ao_channels.add_ao_voltage_chan("Dev1/ao1", min_val=0, max_val=1)
				self.trig_task.timing.cfg_samp_clk_timing(1e6, active_edge=nidaqmx.constants.Edge.RISING, sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=2)
				#self.trig_writer = AnalogSingleChannelWriter(self.trig_task.out_stream)
				#self.trig_writer.write_many_sample(trig_dat)
				self.trig_writer = nidaqmx.stream_writers.DigitalSingleChannelWriter(self.trig_task.out_stream, auto_start=False)
				self.trig_task.triggers.start_trigger.cfg_dig_edge_start_trig("/Dev1/PFI0", trigger_edge=nidaqmx.constants.Edge.RISING)
				self.trig_task.triggers.start_trigger.retriggerable = True
				self.trig_task.register_done_event(self.test)
				print(self.trig_writer.write_many_sample_port_uint32(trig_dat))
				self.trig_task.start()
				self.trig_task.wait_until_done()
				self.trig_task.stop()
				print("Trig 1 enabled - rising edge")
				"""

				"""
				self.trig_task2 = nidaqmx.Task()
				self.trig_task2.do_channels.add_do_chan("Dev1/port0/line21", line_grouping=nidaqmx.constants.LineGrouping.CHAN_PER_LINE)
				self.trig_task2.timing.cfg_samp_clk_timing(1e6, active_edge=nidaqmx.constants.Edge.RISING, sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=2)
				self.trig_writer2 = nidaqmx.stream_writers.DigitalSingleChannelWriter(self.trig_task2.out_stream, auto_start=False)
				self.trig_task2.triggers.start_trigger.cfg_dig_edge_start_trig("/Dev1/PFI0", trigger_edge=nidaqmx.constants.Edge.FALLING)
				self.trig_task2.triggers.start_trigger.retriggerable = True
				self.trig_task2.register_done_event(self.test)
				print(self.trig_writer2.write_many_sample_port_uint32(trig_dat))
				self.trig_task2.start()
				self.trig_task2.wait_until_done()
				self.trig_task2.stop()
				print("Trig 2 enabled - falling edge")
				"""
		else:
			print("Waveform sent")
			self.AFPOut.setEnabled(True)
			self.task = 0 # arbitrary value for simulating output
		self.AFPwave.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:5px;}")

	def AFPSendWvfm_funcgen(self):
		if self.sim == False:
			self.AFPwave.setStyleSheet("QPushButton {background-color: lightblue; color: white; border-radius:5px;}") 
			RFamp = 2*self.RFampspinBox.value()
			self.srs._set_amplitude_(RFamp,FunctionGenerator.VoltageMode.peak_to_peak)
			FsweepRate = 1000*self.SweepspinBox.value()
			Ffwhm = self.FWHMspinBox.value()
			Fcent = self.FcentspinBox.value()
			Fmin = 0.55*Fcent
			Fmax = 1.5*Fcent
			totaltime = (Fmax-Fmin)/FsweepRate
			npnts = 16001
			og = npnts
			checksum = 32768
			while(abs(checksum) > 32767 or npnts < og-100 or npnts < 2):
				npnts = npnts-1
				tpnt = totaltime/npnts
				act_freq = 1/tpnt
				print(tpnt, act_freq, int(act_freq+0.5))
				FsweepR = FsweepRate*tpnt # sweeprate per point (not per second)
				# print('sweeprate = {:f}'.format(FsweepRate))
				#div = int(tpnt/(0.3*math.pow(10,(-6))))

				checksum = 0
				data = [0] * (npnts + 1)
				for x in range (npnts):
					# Freq = Fmin+FsweepRate*x
					# given code showed "=" instead of "+" below...
					# Amplitude = math.exp( (x-Fcent)^2/Ffwhm^2 ) + math.exp( -1* ((Fmin + FsweepRate*x)-Fcent)^2/Ffwhm^2 )
					# Note factor of 2 in rate to keep peak in correct place
					val = 2047*math.exp( -1* (math.pow(((Fmin + FsweepR*x)-Fcent),2)/(math.pow(Ffwhm,2)) ) ) * math.sin(2*math.pi*(Fmin +0.5*FsweepR*x)*x)+0.5
					#val = 2047*math.sin(2/100*math.pi*x)+0.5
					data[x] = int(val)
					checksum = checksum + int(val)
				data[npnts] = checksum
				print('{:d}, {:d}'.format(npnts,checksum))

			self.srs.sendcmd('FSMP {:d}'.format(int(act_freq+0.5)))
			#self.srs.sendcmd('AMRT {:d}'.format(div))

			self.srs.sendcmd('LDWF? 0,{:d}'.format(npnts))
			i=0
			while(self.srs.read(1) != '1' or i>=5):
				True
				i=i+1
				if i==1:
					print('Read failed {:d} time'.format(i))
				else:
					print('Read failed {:d} times'.format(i))

			plt.plot(range(npnts), data[0:npnts], '-o')
			plt.title('AFP Function')
			plt.xlabel('nth point')
			plt.ylabel('magnitude (-32676,32676)')
			plt.show()

			#print(data[npnts])
			
			if (i<5):
				for pt in range(npnts+1):
					if (abs(data[pt]) > 32767):
						print('Load range error!')
					self.srs.write((data[pt]).to_bytes(2, 'little', signed=True), bin=True)

				self.srs.sendcmd('MENA 1')
				self.AFPOut.setEnabled(True)
			else:
				print('Function loading failed.')
			self.AFPwave.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:5px;}") 
		else:
			print("Waveform sent")
			self.AFPOut.setEnabled(True)
			self.task = 0 # arbitrary value for simulating output

	def lasRamp(self):
		# if another setpoint is still being ramped toward stop that timer and ramp toward new setpoint
		if self.ramptimer.isActive():
			self.ramptimer.stop()
		if self.sim==False:
			if not self.lasSer.QueryOUT():
				if not self.lasSer.SetOutputON():
					print("Laser failed to turn on. Try again.")
					self.ramptimer.stop()
		# Begin ramping laser
		self.failflag = 0
		self.rampit = 0
		self.ramptimer.start()
		print('Laser ramping to {:4.2f}A at {:4.2f}A/s.'.format(self.lasspinBox.value(), self.rampspinBox.value()))
		self.anim.start()

	def ramptimeout(self):
		if self.sim==False:
			if self.las == '770':
				self.lasSer.QuerySTT()
				lasval = self.lasSer.GenData.MC
				self.lasreadout.setValue(lasval)
				if self.rampit == 0:
					self.lasprev = lasval
					self.rampit = 1
			else:
				self.lasSer.write(('I\r').encode())
				test=self.lasSer.readline()
				lasval=float(test.decode("utf-8"))
				self.lasreadout.setValue(lasval)
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
			#print(lasval, self.lasprev)
			#if abs(lasval - self.lasprev) < self.lasdelta or abs(lasval - self.lasspinBox.value()) < self.lasdelta:
			# check if current laser readout is within tolerance of overall setpoint
			if abs(lasval - self.lasspinBox.value()) > self.lasdelta:
				# if not check if the difference in current value and setpoint is less than allowable change for 
				# given maximum ramp rate
				dif = self.lasspinBox.value()-lasval
				if abs(dif) < self.rampspinBox.value()/(1000/self.lasint):
					# if ramp rate not exceeded, set power supply current to desired setpoint
					if self.sim==False:
						if self.lasSer.SetCurrent(self.lasspinBox.value()):
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
							if not self.lasSer.SetCurrent(self.lasprev-self.rampspinBox.value()/(1000/self.lasint)):
								if not self.failflag > 1:
									print("Failed to continue ramping.")
								self.failflag += 1
							else:
								self.lasprev = self.lasprev-self.rampspinBox.value()/(1000/self.lasint)
						else:
							self.lasprev = self.lasprev-self.rampspinBox.value()/(1000/self.lasint)
					else:
						if self.sim==False:
							if not self.lasSer.SetCurrent(self.lasprev+self.rampspinBox.value()/(1000/self.lasint)):
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
				#print(lasval)
				if lasval < self.lasdelta:
					if self.sim==False:
						if self.lasSer.SetOutputOFF():
							print("Laser turned off.")
						else:
							print("Laser failed to turn off.")
					else:
						print("Laser turned off.")
				else:
					print("Desired laser current reached.")
			# else wait for current to stabilize to previous laser setting before updating current setpoint

	def timechange(self):
		if self.AFPTimerOut.isChecked():
			print("Time interval change\nAFP running every {:.0f} seconds\nFinishing current interval".format(self.afptime.value()))
		else:
			self.afpcount.setText(self._translate("TapeDriveWindow", str(datetime.timedelta(seconds=self.afptime.value()))[2:]))

	def afptimerun(self):
		if self.AFPTimerOut.isChecked():
			self.AFPTimerOut.setStyleSheet("QPushButton {background-color: lightblue; color: white; border-radius:5px;}")
			self.afptimer.setInterval(1000)
			self.time_left_int = 0
			print("AFP running every {:.0f} seconds".format(self.afptime.value()))
			self.afptimeout()
			self.afptimer.start()
		else:
			self.AFPTimerOut.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:5px;}")
			print("AFP stopped")
			self.afptimer.stop()
			self.afpcount.setText(self._translate("TapeDriveWindow", str(datetime.timedelta(seconds=self.afptime.value()))[2:]))
			self.afp_ind = 0
			self.afprun_int = 0
			self.afprun_int_count = 0
			self.afpcount1.setText(self._translate("TapeDriveWindow", "0"))
			self.afpcount3.setText(self._translate("TapeDriveWindow", "0"))

	def afptimeout(self):
		time_str = str(datetime.timedelta(seconds=self.time_left_int))[2:]
		self.afpcount.setText(self._translate("TapeDriveWindow", time_str))

		if self.time_left_int == 0:
			self.time_left_int = self.afptime.value() - 1

			if self.task != None:
				self.AFPOut.click()
			else:
				print("No waveform loaded. Loading now...")
				print("First flip will occur in {:.0f} seconds".format(self.afptime.value()))
				self.AFPwave.click()
		else:
			self.time_left_int -= 1

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
		if self.sim==False:
			# Triggering workaround
			if self.trig_task != None:
				val = self.trig_task.read()
				# print(val)
				if val >= 2.5:
					self.check_bool = 1
				else:
					self.check_bool = 0
				if self.check_bool != self.afp_bool:
					self.AFPOut.click()

			# Update power supply readouts
			if self.psus[0] != None:
				self.ps1readspinBox.setValue(self.psus[0].psu.outputs[0].measure('current'))
			if self.comps > 0:
				self.ps2readspinBox.setValue(self.psus[1].psu.outputs[0].measure('current'))
			if self.comps == 2:
				self.ps3readspinBox.setValue(self.psus[2].psu.outputs[0].measure('current'))

			# Update photodiode readout
			if self.pdlock_port != None:
				pdread = self.pdlock.read_temperature()
				if pdread != None:
					self.pdreadout.setValue(pdread)
				#self.pd2readout.setValue(self.pds[1].value())

			# Update TC readout
			if self.tc != None:
				regs = self.tc.read_input_registers(12,4)
				if regs:
					print("Temps:\n1: " + str(regs[0]/10) + "\n2: " + str(regs[1]/10) + "\n3: " + str(regs[2]/10) + "\n4: " + str(regs[3]/10))
				else:
					print("read error")

			# Update oven readout (cell/wall)
			if self.oven_port != None:
				if self.relay_port != None:
					if self.oventog.isChecked(): 
						self.ovenreadout.setValue(self.oven.read_temperature())
						
					else:
						self.cellreadout.setValue(self.oven.read_temperature())
				else:
					self.ovenreadout.setValue(self.oven.read_temperature())
			
	def closeEvent(self, event):
		# Kill all timers
		if self.ramptimer.isActive():
			self.ramptimer.stop()
		if self.afptimer.isActive():
			self.afptimer.stop()
		if self.timer.isActive():
			self.timer.stop()

		# Disconnect all power supplies
		for psu in self.psus:
			#for output in psu.psu.outputs:
				#output.enabled = False
			if psu != None:
				psu.psu.close()
			
		# Close connection to omega controllers and oven relay
		if self.sim == False:
			if self.oven_port != None:
				self.oven.close()
			if self.pdlock_port != None:
				self.pdlock.close()
			if self.relay_port != None:
				self.ovenRelayPort.close()

		# Close AFP tasks
		if self.digi_task != None:
			self.task.close()
			self.digi_task.close()
		if self.trig_task != None:
			self.trig_task.close()
			if self.trig_task2 != None:
				self.trig_task2.close()

		# Close connection with Newport rotation stage
		if self.sim == False:
			if self.tapedrive.motors[1] == None:
				if self.smcport != None:
					self.smc100.close()
					del self.smc100

		# Save setpoints in text file
		f = open("Resources/Config.txt","w+")
		f.write("AFP_bool: {:d}\n".format(1 if self.afp_bool else 0))
		f.write("Spin up: {:d}\n".format(self.QWP_right_pos.value()))
		f.write("Spin down: {:d}\n".format(self.QWP_left_pos.value()))
		f.write("Optimum HWP:  {:d}\n".format(self.HWP_opt_pos.value()))
		f.write("HWP location: {:d}\n".format(self.absCoords[0].value()))
		f.write("QWP location: {:d}\n".format(self.absCoords[1].value()))
		f.write("AFP settings: \t{:d}Hz\n\t\t{:d}Hz\n\t\t{:d}kHz/s\n\t\t{:3.1f}V\n".format(int(self.FcentspinBox.value()), int(self.FWHMspinBox.value()), int(self.SweepspinBox.value()), self.RFampspinBox.value()))
		f.close()

		# and afterwards call the closeEvent of the super-class
		super(QtWidgets.QMainWindow, self).closeEvent(event)
		

if __name__ == '__main__':
	import sys
	#QtWidgets.QApplication.setAttribute(QtCore.Qt.
	#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
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