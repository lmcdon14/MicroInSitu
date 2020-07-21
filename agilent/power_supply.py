import ivi
import sys
from pprint import pprint

class PowerSupply():
	def __init__(self, port, sim=False, baudrate=9600, bytesize=8, parity='N', timeout=2, stopbits=2, dsrdtr=True):
		if sim==False:
			print('Power supply connection established!')
			port_str = 'ASRL::' + port + ',9600,8n2::INSTR'

			if port == 'COM1':
				self.psu = ivi.agilent.agilentE3633A(port_str)
				self.psu.outputs[0].configure_range('voltage', 20)
				self.psu.outputs[0].voltage_level = 20
				self.psu.outputs[0].current_limit = 0
			else:
				self.psu = ivi.agilent.agilentE3634A(port_str)
				self.psu.outputs[0].configure_range('voltage', 50)
				self.psu.outputs[0].voltage_level = 50
				self.psu.outputs[0].current_limit = 0
		else:
			self.psu = ivi.agilent.agilentE3633A(port, simulate=sim)

		# Other functions
		# psu.outputs[0].configure_range('voltage', 12)
		# psu.outputs[0].voltage_level = 10
		# psu.outputs[0].current_limit = 1.0
		# psu.outputs[0].ovp_limit = 14.0
		# psu.outputs[0].ovp_enabled = True
		# psu.outputs[0].enabled = True
		# pprint(dir(self.psu.outputs[0]), indent=2)
		# psu.close()

