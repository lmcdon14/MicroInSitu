import threading
import os
import sys
from configparser import ConfigParser
from elliptec import Motor, find_ports

class Tapedrive():
	def __init__(self, motor=None):
		if (motor is None):
			try:
				self.sn_mot = "DT03BPRIA"
				self.connect_motors()
			except IOError as e:
				print(e)
				sys.exit()
		else:
			assert isinstance(motor, Motor)
			self.motor = motor

	def connect_motors(self):
		ports = find_ports()
		for port in ports:
			if (port.serial_number == self.sn_mot):
				self.motor = Motor(port.device)