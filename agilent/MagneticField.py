import threading
import os
import sys
from agilent import PowerSupply, find_ports

class MagneticField():
	def __init__(self, psus=[None]):
		if (psus[0] is None):
			try:
				self.mod_num = "E3633A"
				self.connect_supplies()
			except IOError as e:
				print(e)
				sys.exit()
		else:
			for psu in psus:
				assert isinstance(psu, PowerSupply)
			self.psus = psus

	def connect_supplies(self):
		ports = find_ports()
		ix=0
		for port in ports:
			if (port.serial_number == self.mod_num):
				self.psus[ix] = PowerSupply(port.device)
				ix=ix+1