import serial as s
import serial.tools.list_ports as lp
import sys

# Some helper functions for agilent module

def find_ports():
	avail_ports = []
	for port in lp.comports():
		print(port)
		try:
			p = s.Serial(port.device)
			p.close()
			avail_ports.append(port)
		except (OSError, s.SerialException):
			print('%s unavailable.\n' % port.device)

	return avail_ports