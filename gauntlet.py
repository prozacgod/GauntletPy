#!/usr/bin/env python

# python 2.6 - 3.x compatibility
from __future__ import print_function, with_statement, absolute_import, division, unicode_literals

import sys, os, time, socket, json
import uinput

dev_hostnames = ['prozacgod', 'portablepill']

SETTINGS = {}

class Gauntlet():
	def __init__(self):
		pass
	
def findModule(name):
	if name.endswith('.py'):
		name = name[:-3]
	
	#if os.path.exists(parm):
	
	
	return name
		
		
def main(modules = None):
	if (modules == None):
		for parm in sys.argv[1:]:
			module = findModule(parm)
			if module:
				print("found")
			print(module)

	#main()

def loadSettings(conf_file):
	if conf_file:
		try:
			data = eval(open(conf,'r').read())
		except:
			print("Could not load config file '%s'" % (conf_file))
			sys.exit(1)

		SETTINGS.update(data)

if __name__ == "__main__":
	SETTINGS['dev'] = socket.gethostname() in dev_hostnames
	
	conf = os.path.join(os.environ['HOME'], '.gauntlet.pyon.conf')
	conf = conf if os.path.exists(conf) else None
	
	if SETTINGS['dev']:
		conf = 'gauntlet.pyon.conf'
		conf = conf if os.path.exists(conf) else None
	
	loadSettings(conf)
	print(SETTINGS)
	
#	if (os.path.exists()
#	main()

