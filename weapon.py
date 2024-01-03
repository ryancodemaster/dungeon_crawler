import pygame
import constants
import random
import math
# for the bow, arrow, fireball, and two of my own weapons: sword and sheild
class Bow():
  def __init__(self, image, arrow_image, sheild, sword):
    self.og_image = image
    self.ogsword = sword
    self.sheild = sheild
    self.angle = 0
    self.image = pygame.transform.rotate(self.og_image, self.angle)
    self.sword = pygame.transform.rotate(self.ogsword, self.angle)
    self.arrow_image = arrow_image
    self.rect = self.image.get_rect()
    self.fired = False
    self.last_shot = pygame.time.get_ticks()


  def update(self,player):
    shoot_cooldown = 300
    arrow = None
    
    self.rect.center = player.rect.center

    pos = pygame.mouse.get_pos()
    x_dist = pos[0] - self.rect.centerx
    y_dist = -(pos[1] - self.rect.centery)
    self.angle = math.degrees(math.atan2(y_dist, x_dist))

    if pygame.mouse.get_pressed()[0] == True and self.fired == False and (pygame.time.get_ticks() - self.last_shot >= shoot_cooldown):
      arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
      self.fired = True
      self.last_shot = pygame.time.get_ticks()
      return arrow

    if not pygame.mouse.get_pressed()[0] and self.fired == True:
      self.fired = False
        

  def draw(self, surface):
    # this was intended pureley for the bow, but I borrowed it for my own weapons, because you should only hold one at a time
    if pygame.mouse.get_pressed()[1]: # activates if you press the sheild button
      surface.blit(self.sheild, (self.rect.centerx - 23 , self.rect.centery - 10))
    elif pygame.mouse.get_pressed()[2]: # sword
      self.image = pygame.transform.rotate(self.ogsword, self.angle)
      surface.blit(self.sword, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.sword.get_width()/2)))
    else: # I made bow the default thing to hold
      self.image = pygame.transform.rotate(self.og_image, self.angle)
      surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_width()/2)))
      
class Arrow(pygame.sprite.Sprite): # arrow, shot by player
  def __init__(self, image, x, y, angle):
    pygame.sprite.Sprite.__init__(self)
    self.ogimage = image
    self.angle = angle
    self.image = pygame.transform.rotate(self.ogimage, self.angle - 90)
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)
    self.dx = math.cos(math.radians(self.angle)) * constants.A_SPEED
    self.dy = -(math.sin(math.radians(self.angle)) * constants.A_SPEED)

  def update(self,screen_scroll, enemy_list, obs):
    damage = 0
    damage_pos = None
    
    self.rect.x += screen_scroll[0] + (self.dx)
    self.rect.y += screen_scroll[1] + (self.dy)
    for ob in obs:
      if ob[1].colliderect(self.rect):
        self.kill()
        break

    if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HIGHT:
      self.kill()

    for enemy in enemy_list:
      if enemy.rect.colliderect(self.rect) and enemy.alive:
        damage = 10 + random.randint(-5,6)
        if damage == 6:
          damage += 44
        damage_pos = enemy.rect
        enemy.hp -= damage
        enemy.hit = True
        self.kill()
        break
    return damage, damage_pos
  def draw(self, surface):
    surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_width()/2)))
    
class Sword():
  # I made this personaly
  def __init__(self):
    self.rect = pygame.Rect(0, 0, 200, 200)
    self.attack = False
    self.cooldown_timer = pygame.time.get_ticks()
  def update(self, player, enemy_list):
    cooldown = 200
    damage = 0
    damage_pos = None
    self.rect.centerx = player.rect.centerx
    self.rect.centery = player.rect.centery
    for enemy in enemy_list:
      if enemy.rect.colliderect(self.rect) and enemy.alive and pygame.mouse.get_pressed()[2] and self.attack == False:
        damage = 20
        damage_pos = enemy.rect
        self.cooldown_timer = pygame.time.get_ticks()
        enemy.hp -= damage
        enemy.hit = True
        self.attack = True
      if pygame.time.get_ticks() - self.cooldown_timer >= cooldown:
        self.attack = False
      
    return damage, damage_pos
    
class Fireball(pygame.sprite.Sprite):
  # similar to the arrow, but shot by the big demon
  def __init__(self, image, x, y, tx, ty):
    pygame.sprite.Sprite.__init__(self)
    self.ogimage = image
    x_dist = -(tx - x)
    y_dist = -(ty - y)
    self.angle = (math.degrees(math.atan2(x_dist, y_dist))) + 90
    self.image = pygame.transform.rotate(self.ogimage, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)
    self.dx = math.cos(math.radians(self.angle)) * 3
    self.dy = -(math.sin(math.radians(self.angle)) * 3)

  def update(self,screen_scroll, player):

    self.rect.x += screen_scroll[0] + (self.dx)
    self.rect.y += screen_scroll[1] + (self.dy)


    if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HIGHT:
      self.kill()
      
    if player.rect.colliderect(self.rect) and player.hit == False:
      player.hit = True
      player.lasthit = pygame.time.get_ticks()
      
      if pygame.mouse.get_pressed()[1]: # sheild functoinality, but not conpleteley nullifiying the damage to increse the difficulty
        player.hp -= 2.5
      else:
        player.hp -= 10

  
  def draw(self, surface):
    surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_width()/2)))

# if you are searching for a sheild class, I didn't make one, just seprateley made the functions in different places to draw and reduce damage, united by one button.