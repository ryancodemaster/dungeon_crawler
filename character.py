import math

import pygame

import constants
from weapon import Fireball
# the character class includes the player and enemies

class Character():
  def __init__(self, x, y, mob_animations, char_type, hp, size = 1, boss = False):
    self.char_type = char_type
    self.boss = boss
    self.flip = False
    self.animation_list = mob_animations[char_type]
    self.frame_index = 0
    self.running = False
    self.hp = hp
    self.action = 0
    self.update_time = pygame.time.get_ticks()
    self.image = self.animation_list[self.action][self.frame_index]
    self.rect = pygame.Rect(0,0,48 * size,48 * size)
    self.rect.center = (x,y)
    self.alive = True
    self.score = 0
    self.hit = False
    self.lasthit = pygame.time.get_ticks()
    self.lastfireball = pygame.time.get_ticks()
    self.stunned = False

  def move(self, dx, dy, obsticles, exit = None):
    # you probobly know what this does...
    # (moves character for anyone who doesen't know)
    screen_scroll = [0,0]
    self.running = False
    level_conplete = False
    if dx or dy != 0:
      self.running = True
    
    if dx < 0:
      self.flip = True
    elif dx > 0:
      self.flip = False

    if dx and dy != 0:
      dx = dx * (math.sqrt(2)/2)
      dy = dy * (math.sqrt(2)/2)
    
    self.rect.x += dx
    for ob in obsticles:
      if ob[1].colliderect(self.rect):
        if dx > 0:
          self.rect.right = ob[1].left
        if dx < 0:
          self.rect.left = ob[1].right
    self.rect.y += dy
    for ob in obsticles:
      if ob[1].colliderect(self.rect):
        if dy > 0:
          self.rect.bottom = ob[1].top
        if dy < 0:
          self.rect.top = ob[1].bottom

    if self.char_type == 0:
      if self.rect.right > (constants.SCREEN_WIDTH - 200):
        screen_scroll[0] = (constants.SCREEN_WIDTH - 200) - self.rect.right
        self.rect.right = constants.SCREEN_WIDTH - 200
      if self.rect.left < 200:
        screen_scroll[0] = 200 - self.rect.left
        self.rect.left = 200
      if self.rect.bottom > (constants.SCREEN_HIGHT - 200):
        screen_scroll[1] = (constants.SCREEN_HIGHT- 200) - self.rect.bottom
        self.rect.bottom = constants.SCREEN_HIGHT - 200
      if self.rect.top < 200:
        screen_scroll[1] = 200 - self.rect.top
        self.rect.top = 200
      if exit[1].colliderect(self.rect):
        exit_dist = math.sqrt(((self.rect.centerx - exit[1].centerx) ** 2) + ((self.rect.centery - exit[1].centery) ** 2))
        if exit_dist < 20:
          level_conplete = True
    return screen_scroll, level_conplete
    
  def ai(self,player, obs, screen_scroll, fire_img):
    fireball = None
    blocked_seing = ()
    stun_cool = 100
    dx_ai = 0
    dy_ai = 0
    self.rect.x += screen_scroll[0]
    self.rect.y += screen_scroll[1]
    seeing = ((self.rect.centerx, self.rect.centery), (player.rect.centerx,player.rect.centery))
    for ob in obs:
      if ob[1].clipline(seeing):
        blocked_seing = ob[1].clipline(seeing)
    dist = math.sqrt(((self.rect.centerx - player.rect.centerx)**2) + ((self.rect.centery - player.rect.centery)**2))
    if dist > 50 and not blocked_seing:
      if self.rect.centerx > player.rect.centerx:
        dx_ai = -4
      if self.rect.centery > player.rect.centery:
        dy_ai = -4
      if self.rect.centerx < player.rect.centerx:
        dx_ai = 4
      if self.rect.centery < player.rect.centery:
        dy_ai = 4
      if self.alive and not self.stunned:
        self.move(dx_ai, dy_ai, obs, exit)
        if dist < 60 and not player.hit:
          if not pygame.mouse.get_pressed()[1]: # this was my own doing, I made this button a sheild
            player.hp -= 10
            player.hit = True
            player.lasthit = pygame.time.get_ticks()
        if self.hit:
          self.hit = False
          self.lasthit = pygame.time.get_ticks()
          self.stunned = True
          self.running = False
          self.update_action(0)
      if pygame.time.get_ticks() - self.lasthit >= stun_cool:
        self.stunned = False
    if dist > 50 and self.alive:
      # boss code ONLY
      if self.boss:
        firecool = 700
        if dist < 500:
          if pygame.time.get_ticks() - self.lastfireball >= firecool:
              fireball = Fireball(fire_img, self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
              self.lastfireball = pygame.time.get_ticks()
    
    return fireball
  def update(self, player):
    if self.hp <= 0:
      self.hp = 0
      self.alive = False
    
    hitcoll = 1000
    if self.char_type == 0 and self.hit:
      if pygame.time.get_ticks() - self.lasthit > hitcoll:
        self.hit = False
    
    if self.running is True:
      self.update_action(1)
    else:
      self.update_action(0)
    
    animation_cooldown = 70
    self.image = self.animation_list[self.action][self.frame_index]
    if pygame.time.get_ticks() - self. update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    if self.frame_index >= len(self.animation_list[self.action]):
      self.frame_index = 0
  
  def update_action(self, new_action):
    if new_action != self.action:
      self.action = new_action
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()
    
  def draw(self, surface):
    current_frame = self.image
    flipped_image = pygame.transform.flip(current_frame, self.flip, False)
    if self.char_type == 0:
      surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET))
    else:
      surface.blit(flipped_image, self.rect)