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

	def MoveBike(self,route):
		main_dir = os.path.split(os.path.abspath(__file__))[0]
		self.alpha -= self.dist_step
		if(self.alpha < 0):
			self.position += 1
			self.alpha = 255 
			if self.position+1 > self.config.getint('Route', 'image_count'):
				self.position = 1 #TODO Route Done!
			if self.config.getint('Route', 'image_count') >= (self.position+1):
				self.image = pygame.image.load (os.path.join (main_dir, route+"/ROUTE-"+str(self.position)+".jpg")).convert()
				self.next_image = pygame.image.load (os.path.join (main_dir, route+"/ROUTE-"+str(self.position+1)+".jpg")).convert()
		self.bike.dist += .1
		self.bike.rpm = 300
		self.update = True
		
	def Update(self, screen, route):
		self.route = route
		main_dir = os.path.split(os.path.abspath(__file__))[0]

		self.update = False
		
		if not self.init:
			self.init = True
			self.Start()
			self.alpha = 0
			self.update = True
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
					self.MoveBike(route)
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
			#Blit HUD
			screen.blit(hud.get_hud(self.bike, screen.get_width(), screen.get_height()), (0,0))

		if self.update:
			if self.alpha >140:
				self.image.set_alpha(255)
				screen.blit (self.image, (0,50))
			else:
				self.image.set_alpha(self.alpha)
				screen.blit (self.image, (0,50))
				self.next_image.set_alpha(255-self.alpha)
				#Blit World Data
				screen.blit (self.next_image, (0,50))

			#Blit HUD
			screen.blit(hud.get_hud(self.bike, screen.get_width(), screen.get_height()), (0,0))
		
			#NAV BOX
			screen.blit(plot.get_chart(self.route_points,0), (10, screen.get_height()-100))

			if self.cleanup_mode:
				self.image.set_alpha(255)
				screen.blit(pygame.transform.scale(self.image, (200,100)), (20, 300))

		return True

	def __init__(self):
		self.cleanup_mode = True
		self.dist_step = 90
		self.alpha = 255
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

