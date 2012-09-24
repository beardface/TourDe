import pygame
from bike import bike

def get_hud(abike, width, height):
  hud = pygame.Surface((width, 80))
  
  hud.blit(get_rpmbar(abike.rpm), (0,0))
  hud.blit(get_timebar(abike.time), (width/2.0-170, 0))
  hud.blit(get_distbar(abike.dist), (width-150,0))
  hud.set_colorkey((0,0,0))
  return hud

def get_rpmbar(rpm):
  width = 160
  height = 80

  rpmbar = pygame.Surface((width, height))
  rpmbar.fill((250,250,250))
  font = pygame.font.SysFont("monospace", 30)
  text = font.render(str(rpm)+"MPH", 1, (10, 10, 10))
  textpos = text.get_rect()
  textpos.centerx = rpmbar.get_rect().centerx
  textpos.centery = rpmbar.get_rect().centery
  rpmbar.blit(text, textpos)

  return rpmbar

def get_timebar(t):
  width = 340
  height = 80

  timebar = pygame.Surface((width, height))
  timebar.fill((0,100,0))

  timebar = pygame.Surface((width, height))
  timebar.fill((250,250,250))
  font = pygame.font.SysFont("monospace", 60)
  text = font.render(t, 1, (10, 10, 10))
  textpos = text.get_rect()
  textpos.centerx = timebar.get_rect().centerx
  textpos.centery = timebar.get_rect().centery
  timebar.blit(text, textpos)
  timebar.set_colorkey((250,250,250))

  return timebar

def get_distbar(d):
  width = 150
  height = 80

  distbar = pygame.Surface((width, height))
  distbar.fill((0,0,100))

  distbar = pygame.Surface((width, height))
  distbar.fill((250,250,250))
  font = pygame.font.SysFont("monospace", 30)
  text = font.render(str(d)+"mi", 1, (10, 10, 10))
  textpos = text.get_rect()
  textpos.centerx = distbar.get_rect().centerx
  textpos.centery = distbar.get_rect().centery
  distbar.blit(text, textpos)

  return distbar

