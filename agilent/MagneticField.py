import threading
import os
import sys
from agilent import PowerSupply, find_ports
from pprint import pprint

class MagneticField():
	def __init__(self, psus=[None]*3, simulate=False):
		if (psus[0] is None):
			self.psus = psus
			try:
				self.sns = ['MY51270007', 'MY51290001']
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
			print("Testing mag field")
			print(ports)
			print(len(ports))
			for port in ports:
				print(port)
				# check if port is a known power supply
				print(port.serial_number)
				#pprint(vars(port), indent=2)
				#if port.serial_number in self.sns:
				#if port.device != 'COM13' or port.device == 'COM14':
			ports = ['COM13', 'COM14']
			for port in ports:		
				self.psus[ix] = PowerSupply(port)
				ix=ix+1
		else:
			for i in range(3):
				self.psus[i] = PowerSupply('test', sim=True)