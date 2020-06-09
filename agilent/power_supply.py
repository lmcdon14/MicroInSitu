import ivi
import serial
import sys
from pprint import pprint

class PowerSupply(serial.Serial):
	def __init__(self, port, baudrate=9600, bytesize=8, parity='N', timeout=2, startbits=1, stopbits=2, dsrdtr=True):
		try:
			super().__init__(port, baudrate=9600, bytesize=8, parity='N', timeout=2, startbits=1, stopbits=2, dsrdtr=True)
		except serial.SerialException:
			print('Could not open power supply port %s' % port)
			sys.exit()

		if self.is_open:
			print('Power supply connection established!')
			self.psu = ivi.agilent.agilentE3633A(port, simulate=True)

        # psu.outputs[0].configure_range('voltage', 12)
        # psu.outputs[0].voltage_level = 10
        # psu.outputs[0].current_limit = 1.0
        # psu.outputs[0].ovp_limit = 14.0
        # psu.outputs[0].ovp_enabled = True
        # psu.outputs[0].enabled = True
        # pprint(dir(psu.outputs[0]), indent=2)
        # psu.close()

