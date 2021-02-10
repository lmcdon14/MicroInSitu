import threading
import os
import sys
from configparser import ConfigParser
from elliptec import Motor, find_ports

class Tapedrive():
	def __init__(self, motor=None):
		if (motor is None):
			try:
				self.sn_mots = ["DT03BPRIA", "DT03ANGAA", "DT03BQ5GA"]
				self.connect_motors()
			except IOError as e:
				print(e)
				sys.exit()
		else:
			assert isinstance(motor, Motor)
			self.motor = motor

	def connect_motors(self):
		self.motors = [None] * 2
		ports = find_ports()
		i=0
		for port in ports:
			if (port.serial_number in self.sn_mots):
				self.motors[i] = Motor(port.device)
				i = i+1