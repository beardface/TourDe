import pygame
import os
from pygame.locals import *

class menu:

	def RenderPreview(self, screen, image_path, x, y, w, h):
		image = pygame.image.load (os.path.join (image_path)).convert()
		image = pygame.transform.scale(image, (w,h))
		screen.blit (image, (x, y))

	def RenderMenu(self, screen):
		font_size = 36
		line_space = 4;
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((250, 250, 250))
		
		index = 0
		for key, value in self.CurrentMenuFocus.items() :
			font = pygame.font.Font(None, font_size)
			line_text = key
			if index == self.CurrentItemFocus and not self.level == 'route':
				line_text = "--> "+line_text
			elif self.level == 'route':
				line_text = key + ": "+value

			text = font.render(line_text, 1, (10, 10, 10))
			textpos = text.get_rect()
			textpos.centerx = background.get_rect().centerx
			textpos.centery = font_size+font_size*(index)+line_space*(index)
			background.blit(text, textpos)
			index+=1

			main_dir = os.path.split(os.path.abspath(__file__))[0]

			if self.level == 'route':
				self.RenderPreview(background, os.path.join(main_dir, 'circuits/'+self.CurrentCircuit+'/'+self.CurrentLegs+'/route.bmp'), background.get_rect().centerx-100,300, 200, 100)
				text = font.render("--> START", 1, (10, 10, 10))
				textpos = text.get_rect()
				textpos.centerx = background.get_rect().centerx
				textpos.centery = (len(self.CurrentMenuFocus)+2)*font_size+line_space*(len(self.CurrentMenuFocus)+2)
				background.blit(text, textpos)
			elif self.level == 'legs':
				self.RenderPreview(background, os.path.join(main_dir, 'circuits/'+self.CurrentCircuit+'/'+self.CurrentLegs+'/route.bmp'), background.get_rect().centerx-100,300, 200, 100)
			elif self.level == 'circuits':
				if not self.CurrentCircuit == "none":
					self.RenderPreview(background, os.path.join(main_dir, 'circuits/'+self.CurrentCircuit+'/circuit.bmp'), background.get_rect().centerx-100,300, 200, 100)

		screen.blit(background, (0, 0))
		
	def GetKeyFromIndex(self, d, i):
		t = 0
		for key, value in self.CurrentMenuFocus.iteritems() :
			if(t == i):
				return key
			else:
				t+=1
		return ""

	def MenuDown(self):
		if(self.CurrentItemFocus < (len(self.CurrentMenuFocus) - 1)):
			self.CurrentItemFocus += 1

		if self.level == 'legs':
			self.CurrentLegs = self.GetKeyFromIndex(self.CurrentMenuFocus, self.CurrentItemFocus)
		elif self.level == 'circuits':
			self.CurrentCircuit = self.GetKeyFromIndex(self.CurrentMenuFocus, self.CurrentItemFocus)

	def MenuUp(self):
		if(self.CurrentItemFocus > 0):
			self.CurrentItemFocus -= 1
			
		if self.level == 'legs':
			self.CurrentLegs = self.GetKeyFromIndex(self.CurrentMenuFocus, self.CurrentItemFocus)
		elif self.level == 'circuits':
			self.CurrentCircuit = self.GetKeyFromIndex(self.CurrentMenuFocus, self.CurrentItemFocus)
			
	def MenuSelect(self):
		if self.level == 'main':
			if self.GetKeyFromIndex(self.CurrentMenuFocus, self.CurrentItemFocus) == 'Circuits':
				self.level = 'circuits'
				self.CurrentMenuFocus = self.CurrentMenuFocus[self.GetKeyFromIndex(self.CurrentMenuFocus, self.CurrentItemFocus)]
				self.CurrentCircuit = self.GetKeyFromIndex(self.CurrentMenuFocus,0)
		elif self.level == 'circuits':
			self.level = 'legs'
			self.CurrentCircuit = self.GetKeyFromIndex(self.CurrentMenuFocus, self.CurrentItemFocus)
			self.CurrentMenuFocus = self.CurrentMenuFocus[self.GetKeyFromIndex(self.CurrentMenuFocus, self.CurrentItemFocus)]
			self.CurrentLegs = self.GetKeyFromIndex(self.CurrentMenuFocus, 0)
		elif self.level == 'legs':
			self.level = 'route'
			self.CurrentLegs = self.GetKeyFromIndex(self.CurrentMenuFocus, self.CurrentItemFocus)
			self.CurrentMenuFocus = self.CurrentMenuFocus[self.GetKeyFromIndex(self.CurrentMenuFocus, self.CurrentItemFocus)]
		elif self.level == 'route':
			self.level = 'start'
			self.CurrentRoute = self.GetKeyFromIndex(self.CurrentMenuFocus, self.CurrentItemFocus)


		if self.level == 'start':
			return False
		else:
			self.CurrentItemFocus = 0
			return True
	
	def MenuBack(self):
		if self.level == 'circuits':
			self.level = 'main'
			self.CurrentMenuFocus = self.MenuItems
			self.CurrentItemFocus = 0
			self.CurrentCircuit = "none"
		elif self.level == 'legs':
			self.level = 'circuits'
			self.CurrentMenuFocus = self.MenuItems['Circuits']
			self.CurrentLegs = "none"
		elif self.level == 'route':
			self.level = 'legs'
			self.CurrentMenuFocus = self.MenuItems['Circuits'][self.CurrentCircuit]
		elif self.level == 'start':
			self.level = 'route'
			self.CurrentMenuFocus = self.MenuItems['Circuits'][self.CurrentCircuit][self.CurrentLegs]
			self.CurrentRoute = "none"

		self.CurrentItemFocus = 0

	def Update(self, screen):
		update = False
		for event in pygame.event.get():
			if event.type == QUIT:
				self.quit = True
			elif event.type == KEYDOWN and event.key == K_UP:
				self.MenuUp()
				update = True
			elif event.type == KEYDOWN and event.key == K_DOWN:
				self.MenuDown()
				update = True
			elif event.type == KEYDOWN and event.key == K_RIGHT:
				self.show = self.MenuSelect()
				update = True
			elif event.type == KEYDOWN and event.key == K_LEFT:
				self.MenuBack()
				update = True
			elif event.type == KEYDOWN and event.key == K_RETURN:
				self.show = self.MenuSelect()
				update = True
		#if update:
		self.RenderMenu(screen)
		return True
	
	def PopulateMenu(self):
		f = open('menu.dat','r')
		self.MenuItems = eval(f.read())

	def Initialize(self):
		self.PopulateMenu()
		self.CurrentMenuFocus = self.MenuItems
		self.level = 'main'

	def GetCurrentRoutePath(self):
		return 'circuits/'+self.CurrentCircuit+'/'+self.CurrentLegs+'/'

	def __init__(self):
		self.show = True
		self.quit = False
		self.MenuItems = {}
		self.level = 'main'
		self.CurrentMenuFocus = {}
		self.CurrentItemFocus  = 0
		self.CurrentCircuit  = 'none'
		self.CurrentLegs     = 'none'
		self.CurrentRoute    = 'none'
		
		self.Initialize()

