from __future__ import print_function, with_statement, absolute_import, division, unicode_literals

import uinput

class Mouse():
	_refCount = 0
	def __init__(self, name = ""):
		self.name = "Gauntlet mouse %d" % (Mouse._refCount)
		Mouse._refCount += 1
		
		self.capabilities = {
			uinput.EV_REL: [uinput.REL_X, uinput.REL_Y, uinput.REL_WHEEL, uinput.REL_HWHEEL],
			uinput.EV_KEY: [uinput.BTN_LEFT, uinput.BTN_RIGHT],
		}

		self.device = uinput.Device(name=self.name, capabilities=self.capabilities)

	def __setitem__(self, index, value):
		if (index[:4] == "REL_") and hasattr(uinput, index):
			self.device.emit(uinput.EV_REL, getattr(uinput, index), value)
		elif (index[:4] in ["BTN_", "KEY_"]) and hasattr(uinput, index):
			self.device.emit(uinput.EV_KEY, getattr(uinput, index), value)
			
		elif index == 'REL_POS':
			self.device.emit(uinput.EV_REL, uinput.REL_X, value[0])
			self.device.emit(uinput.EV_REL, uinput.REL_Y, value[1])
		
		else:
			print ("invalid property");

class Keyboard():
	_refCount = 0
	def __init__(self, name = ""):
		self.name = "Gauntlet keyboard %s" % (Keyboard._refCount)
		Keyboard._refCount += 1
		#support all keyboard keys
		keys = [uinput.CAPABILITIES[key] for key in uinput.CAPABILITIES.keys() if key.startswith('KEY_')]
		
		self.capabilities = {
			uinput.EV_KEY: keys,
        }
		self.device = uinput.Device(name=self.name, capabilities=self.capabilities)

	def __setitem__(self, index, value):
		if index.startswith("KEY_") and hasattr(uinput, index):
			self.device.emit(uinput.EV_KEY, getattr(uinput, index), value)

	def press(self, key):
		self.device.emit(uinput.EV_KEY, key, 1) # Press.
		self.device.emit(uinput.EV_KEY, key, 0) # Release.

		
if __name__ == "__main__":
	import time, sys
	m = Mouse()
	for i in range(20):
		m['REL_POS'] = (5,5)
		time.sleep(.01)
		
	
