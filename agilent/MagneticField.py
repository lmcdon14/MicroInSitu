import threading
import os
import sys
from agilent import PowerSupply, find_ports

class MagneticField():
	def __init__(self, psus=[None]*2, simulate=False):
		if (psus[0] is None):
			self.psus = psus
			try:
				self.mod_num = "E3633A"
				self.connect_supplies(sim=simulate)
			except IOError as e:
				print(e)
				sys.exit()
		else:
			for psu in psus:
				assert isinstance(psu, PowerSupply)
			self.psus = psus

	def connect_supplies(self, sim=False):
		if sim==False:
			ports = find_ports()
			ix=0
			for port in ports:
				# check if port is a known power supply
				if (port.serial_number == self.mod_num):
					self.psus[ix] = PowerSupply(port.device)
					ix=ix+1
		else:
			for i in range(2):
				self.psus[i] = PowerSupply('test', sim=True)