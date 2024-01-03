import pygame
# for coin and potion
class Item(pygame.sprite.Sprite):
  def __init__(self, x, y, item_type, animaion_list, dc = False):
    pygame.sprite.Sprite.__init__(self)
    self.item_type = item_type
    self.animation_list = animaion_list
    self.timer = pygame.time.get_ticks()
    self.frame = 0
    self.image = self.animation_list[self.frame]
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.dc = dc

  def update(self,screen_scroll, player, coin_fx, potion_fx):
    if not self.dc:
      self.rect.x += screen_scroll[0]
      self.rect.y += screen_scroll[1]
    if self.rect.colliderect(player.rect):
      if self.item_type == 0:
        player.score += 1
        coin_fx.play()
      elif self.item_type == 1:
        player.hp += 50
        potion_fx.play()
        if player.hp > 100:
          player.hp = 100
      self.kill()
        
      
    cooldown = 150
    self.image = self.animation_list[self.frame]
    if (pygame.time.get_ticks() - self.timer >= cooldown):
      self.frame += 1
      self.timer = pygame.time.get_ticks()
    if self.frame >= len(self.animation_list):
      self.frame = 0

  def draw(self,surface):
    surface.blit(self.image, self.rect)