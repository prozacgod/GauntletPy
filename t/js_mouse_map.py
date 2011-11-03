import os, sys, time
from glob import glob

cmd_folder = os.path.dirname(os.path.abspath(__file__ + "/../"))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

from event_thread import MonitorThread
from linux_input import EventDevice
from devices import Mouse, Keyboard


mt = MonitorThread()
devices = glob("/dev/input/event*")
for device in devices:
	try:
		eventInput = mt.monitorInput(EventDevice(device))
		print("Added %s (%s) " % (device, eventInput.name))
	except:
		print("Ignored " + device)
mt.start()


mouse = Mouse()
keyboard = Keyboard()

joystick = {'ABS_X':0, 'ABS_Y':0, 'ABS_THROTTLE':0, 'ABS_Z':0}

def AXIS(fInput, event):
	joystick[event.code] = event.value // 16

	if (joystick['ABS_Y'] > 2):
		keyboard['KEY_S'] = 1
	if (joystick['ABS_Y'] < 2):
		keyboard['KEY_S'] = 0

	if (joystick['ABS_Y'] < -2):
		keyboard['KEY_W'] = 1
	if (joystick['ABS_Y'] > -2):
		keyboard['KEY_W'] = 0

	if (joystick['ABS_X'] > 2):
		keyboard['KEY_D'] = 1
	if (joystick['ABS_X'] < 2):
		keyboard['KEY_D'] = 0

	if (joystick['ABS_X'] < -2):
		keyboard['KEY_A'] = 1
	if (joystick['ABS_X'] > -2):
		keyboard['KEY_A'] = 0

	
def BUTTON(fInput, event):
	print event.code
	
	if (event.code == 'BTN_TL') and (event.value > 0):
		mouse['REL_WHEEL'] = -1

	if (event.code == 'BTN_Y') and (event.value > 0):
		mouse['REL_WHEEL'] = 1
		
	if (event.code == 'BTN_C'):
		keyboard['KEY_SPACE'] = int(event.value)
		
	if (event.code == 'BTN_X'):
		mouse['BTN_LEFT'] = int(event.value)

	if (event.code == 'BTN_B'):
		mouse['BTN_RIGHT'] = int(event.value)

	
def Debug(fInput, event):
	print(event)

mt.on({"EV_ABS": [None]}, AXIS)
mt.on({"EV_KEY": [None]}, BUTTON)

	
while True:
	if (abs(joystick['ABS_Z']) > 1):
		mouse['REL_X'] = joystick['ABS_Z'];

	if (abs(joystick['ABS_THROTTLE']) > 1):
		mouse['REL_Y'] = joystick['ABS_THROTTLE'];

	
	time.sleep(.01) # 100 times a second..
