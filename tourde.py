import pygame
import os
from pygame.locals import *

import hud
import plot

from bike import bike
import time, datetime

import ConfigParser

class tourde:

	def load_configuration(self, cfg_file):
		config = ConfigParser.RawConfigParser()
		
		try:
			with open(cfg_file) as f: pass
		except IOError as e:
			build_configuration(config)

		config.read(cfg_file)
		return config
	
	def Start(self):
		self.start_time = time.time()-self.elapsed_time
		self.running = True

	def Stop(self):
		self.stop_time = time.time()
		self.elapsed_time = 0
		self.running = False
		#Total Time = stop_time - start_time
		self.bike.dist+=.1

	def Pause(self):
		self.stop_time = time.time()
		self.running = False
		self.elapsed_time = time.time()-self.start_time

	def Update(self, screen, route):
		self.route = route
		main_dir = os.path.split(os.path.abspath(__file__))[0]

		self.update = False
		
		if not self.init:
			self.init = True
			self.Start()
			self.update = False
			self.config = self.load_configuration((route+"/route.dat"))
			print self.config.getint('Route', 'image_count')
			if self.config.getint('Route', 'image_count') >= (self.position+1):
				self.image = pygame.image.load (os.path.join (main_dir, route+"/ROUTE-"+str(self.position)+".jpg")).convert()
				self.next_image = pygame.image.load (os.path.join (main_dir, route+"/ROUTE-"+str(self.position+1)+".jpg")).convert()
				

			
		for event in pygame.event.get():
			if event.type == QUIT:
				self.quit = True
			elif event.type == KEYDOWN and event.key == K_q:
				if self.running:
					self.position +=1
					if self.position+1 > len(self.route_points):
						self.position = 0 #TODO Route Done!
					if self.config.getint('Route', 'iamge_count') >= (self.position+1):
						self.image = pygame.image.load (os.path.join (main_dir, route+"/ROUTE-"+str(self.position)+".jpg")).convert()
						self.next_image = pygame.image.load (os.path.join (main_dir, route+"/ROUTE-"+str(self.position+1)+".jpg")).convert()
					self.bike.dist+=.1
					self.bike.rpm=300
					self.update = True

			elif event.type == KEYDOWN and event.key == K_b:	
				if not self.running:
					self.Start()
			elif event.type == KEYDOWN and event.key == K_n:	
				if self.running:
					self.Pause()
			elif event.type == KEYDOWN and event.key == K_m:	
				self.Stop()
		
		#Update Bike
		if self.running:
			seconds = time.time() - self.start_time
			self.bike.time = str(datetime.timedelta(seconds=int(seconds)))
			if not self.last_time == self.bike.time:
				self.last_time = self.bike.time
				self.update = True

		if self.update:
			#Blit World Data
			screen.blit (self.image, (0,0))

			#Blit HUD
			screen.blit(hud.get_hud(self.bike), (0,0))
		
			#NAV BOX
			screen.blit(plot.get_chart(self.route_points,self.position), (10, 380))

		return True

	def __init__(self):
		self.route_points = [300,320,405,233,323,325,343,343,400]
		self.update = True
		self.last_time = ""
		self.elapsed_time = 0
		self.start_time = 0
		self.end_time = 0
		self.running = False
		self.bike = bike()
		self.quit = False
		self.position = 1
		self.route = ""
		self.init = False

