import os
import pygame
from pygame.locals import *
import ConfigParser
import thread, threading
import serialThread
from tourde import tourde
from menu import menu

import serial

import sys
import signal

main_dir = os.path.split(os.path.abspath(__file__))[0]
config_file_name = 'torde.cfg'

def build_configuration(cfg):
	print "Building Initial Configuration File..."
	cfg.add_section('Display')
	cfg.set('Display', 'height', '480')
	cfg.set('Display', 'width', '640')
	with open(config_file_name, 'wb') as configfile:
		cfg.write(configfile)

def validate_configuration(cfg):
	#TODO -- Validate Config
	print "Not Implemented."

def load_configuration():
	config = ConfigParser.RawConfigParser()
	
	try:
		with open(config_file_name) as f: pass
	except IOError as e:
		build_configuration(config)

	config.read(config_file_name)
	return config

def main():
	lock = threading.Lock()
	sThread = serialThread.SerialThread(lock)
	sThread.start()
	
	def signal_handler(signal, frame):
		print 'Control C... Exiting'
		sThread.stop()
		sys.exit(0)

	signal.signal(signal.SIGINT, signal_handler)

	pygame.init ()
	config = load_configuration()
	screen = pygame.display.set_mode(
		(
			config.getint('Display', 'width'),
			config.getint('Display', 'height')
		), 0, 32)
	
	pygame.display.flip()
	pygame.key.set_repeat(500, 30)

	tourdePtr = tourde()
	menuPtr   = menu()

	going = True
	main_menu = False
	while going:
		if menuPtr.show:
			menuPtr.Update(screen)
		else:
			tourdePtr.Update(screen, menuPtr.GetCurrentRoutePath(), sThread)
		
		if menuPtr.quit or tourdePtr.quit:
			going = False
			
		pygame.display.flip()   # Call this only once per loop
		pygame.time.Clock().tick(30)     # forces the program to run at 30 fps.
		
	pygame.quit()

if __name__ == '__main__': 
	main()
