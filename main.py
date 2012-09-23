import os
import pygame
from pygame.locals import *
import ConfigParser

from tourde import tourde
from menu import menu

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
			tourdePtr.Update(screen, menuPtr.GetCurrentRoutePath())
		
		if menuPtr.quit or tourdePtr.quit:
			going = False
		pygame.display.flip()
	pygame.quit()

if __name__ == '__main__': 
	main()
