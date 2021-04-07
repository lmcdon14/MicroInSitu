import threading
import os
import sys
from agilent import PowerSupply

class MagneticField():
	def __init__(self, psus=[None]*3, simulate=False, ports=['COM13', 'COM14']):
		if (psus[0] is None):
			self.psus = psus
			try:
				self.sns = ['MY51270007', 'MY51290001']
				self.connect_supplies(sim=simulate, ports=ports)
			except IOError as e:
				print(e)
				sys.exit()
		else:
			for psu in psus:
				assert isinstance(psu, PowerSupply)
			self.psus = psus

	def connect_supplies(self, sim=False, ports=['COM13', 'COM14']):
		if sim==False:
			ix=0
			for port in ports:
				if port != None:		
					self.psus[ix] = PowerSupply(port)
					ix=ix+1
		else:
			for i in range(3):
				self.psus[i] = PowerSupply('test', sim=True)