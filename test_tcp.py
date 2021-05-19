from pyModbusTCP.client import ModbusClient

c = ModbusClient(host="192.168.127.247", port = 502, auto_open = True, auto_close = True)
regs = c.read_input_registers(12,4)
if regs:
	print("Temps:\n1: " + str(regs[0]/10) + "\n2: " + str(regs[1]/10) + "\n3: " + str(regs[2]/10) + "\n4: " + str(regs[3]/10))
else:
	print("read error")