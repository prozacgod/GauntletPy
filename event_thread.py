#!/usr/bin/env python
from __future__ import print_function, with_statement, absolute_import, division, unicode_literals

import os, sys, time
from select import select

import threading
from threading import Thread

mainThread = threading.currentThread()
		
class MonitorThread (Thread):
	def __init__(self):
		Thread.__init__(self)
		self._debug = False
		self.files = []
		
		self.eventListeners = {}
		
	def monitorInput(self, fInput):
		if getattr(fInput, 'fileno'):
			self.files += [fInput]
		return fInput
		
	def run(self):
		while mainThread.isAlive():
			fds = select(self.files, [], [], .250)
			for fInput in fds[0]:
				event = fInput.read()
				if None in self.eventListeners:
					[callback(fInput, event) for callback in self.eventListeners[None][None]]
					
				if (event.type in self.eventListeners):
					if None in self.eventListeners[event.type]:
						[callback(fInput, event) for callback in self.eventListeners[event.type][None]]
					if (event.code in self.eventListeners[event.type]):
						[callback(fInput, event) for callback in self.eventListeners[event.type][event.code]]						
				
				if self._debug:
					print(fInput.name, event)
				
	def debug(self):
		self._debug = True
	
	def on(self, event_map, callback):
		for event_type in event_map:
			if not event_type in self.eventListeners:
				self.eventListeners[event_type] = {}
			
			for event_code in event_map[event_type]:
				if not event_code in self.eventListeners[event_type]:
					self.eventListeners[event_type][event_code] = []
			
				self.eventListeners[event_type][event_code] += [callback]
		
if __name__ == "__main__":
	import math
	from glob import glob
	from linux_input import EventDevice
	
	devices = glob("/dev/input/event*")
	mt = MonitorThread()
	mt.start()
	#mt.debug()
	
	for device in devices:
		try:
			eventInput = mt.monitorInput(EventDevice(device))
			print("Added %s (%s) " % (device, eventInput.name))
		except:
			print("Ignored " + device)


	event_codes = set()
	events = {}

	def ABS(fInput, event):
		print(fInput.name)

		if fInput.name.startswith('Sony'):
			event_codes.update([event.code])
			events[event.code] = event.value
		
	mt.on({None: [None]}, ABS)
		
		
	table_col = 5
	
	while True: ## the event thread works in the background,
		time.sleep(.1)
	
		






