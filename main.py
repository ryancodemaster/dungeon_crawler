# IMPORT IMPORT IMPORT IMPORT IMPORT IIIIMMMMMMPPPPPPOOOORRRRRRRRRRRRTTTTTTTT!!!!!!!!!!
import csv
import pygame
from pygame import mixer
import constants
from character import Character
from items import Item
from weapon import Bow
from world import World
from weapon import Sword
from button import Button
mixer.init()
pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HIGHT))
pygame.display.set_caption("My Dungeon")
# varyables that do important things
world = World()
start_game = False
pause_game = False
start_intro = False
level = 1
screen_scroll = [0,0]

m_l = False
m_r = False
m_u = False
m_d = False
# a font for the damage text
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)
# scale for images
def scale_img(image, scale):
  w = image.get_width()
  h = image.get_height()
  return pygame.transform.scale(image, (w * scale, h * scale))
# music
pygame.mixer.music.load('assets/audio/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
shot_fx = pygame.mixer.Sound('assets/audio/arrow_shot.mp3')
hit_fx = pygame.mixer.Sound('assets/audio/arrow_hit.wav')
coin_fx = pygame.mixer.Sound('assets/audio/coin.wav')
potion_fx = pygame.mixer.Sound('assets/audio/heal.wav')

# images loading section
tile_list = []
for t in range (18):
  tile_img =scale_img(pygame.image.load(f'assets/images/tiles/{t}.png').convert_alpha(), 3)
  tile_list.append(tile_img)


# buttons images
restart_img = scale_img(pygame.image.load('assets/images/buttons/button_restart.png').convert_alpha(), 1)
start_img = scale_img(pygame.image.load('assets/images/buttons/button_start.png').convert_alpha(), 1)
exit_img = scale_img(pygame.image.load('assets/images/buttons/button_exit.png').convert_alpha(), 1)
resume_img = scale_img(pygame.image.load('assets/images/buttons/button_resume.png').convert_alpha(), 1)
# more images
coins = []
for x in range(4):
  image = scale_img(pygame.image.load(f'assets/images/items/coin_f{x}.png').convert_alpha(), constants.ITEM_SCALE)
  coins.append(image)
potion_image = scale_img(pygame.image.load('assets/images/items/potion_red.png').convert_alpha(), 2)
sheild = scale_img(pygame.image.load('assets/images/weapons/shield.png').convert_alpha(), constants.ITEM_SCALE)

sword = scale_img(pygame.image.load('assets/images/weapons/sword.png').convert_alpha(), constants.ITEM_SCALE)

eh = scale_img(pygame.image.load('assets/images/items/heart_empty.png').convert_alpha(), constants.ITEM_SCALE)
hh = scale_img(pygame.image.load('assets/images/items/heart_half.png').convert_alpha(), constants.ITEM_SCALE)
fh = scale_img(pygame.image.load('assets/images/items/heart_full.png').convert_alpha(), constants.ITEM_SCALE)
bow_image = scale_img(pygame.image.load('assets/images/weapons/bow.png').convert_alpha(), constants.WEPON_SCALE)
arrow_image = scale_img(pygame.image.load('assets/images/weapons/arrow.png').convert_alpha(), constants.WEPON_SCALE)
fire_img = scale_img(pygame.image.load('assets/images/weapons/fireball.png').convert_alpha(), 1)
# load character animations (enemy and player)
mob_animations = []
mob_types = ['elf','imp','skeleton','goblin', 'muddy', 'tiny_zombie','big_demon']

animation_types = ['idle', 'run']
for mob in mob_types:
  animation_list=[]
  for animation in animation_types:
    temp_list = []
    for i in range(4):
     img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
     img = scale_img(img, constants.SCALE)
     temp_list.append(img)
    animation_list.append(temp_list)
  mob_animations.append(animation_list)
# defining lots of things
def texting(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def info():
  pygame.draw.rect(screen, constants.BLUE, (0, 0, constants.SCREEN_WIDTH, 50))
  pygame.draw.line(screen, constants.WIHTE,(0, 50),(constants.SCREEN_WIDTH, 50))
  hh_exists = False
  for i in range (5):
   if player.hp >= ((i + 1) * 20):
     screen.blit(fh, (10 + i * 50, 0))
   elif (player.hp % 20 > 0) and not hh_exists:
     screen.blit(hh, (10 + i * 50, 0))
     hh_exists = True
   else:
     screen.blit(eh, (10 + i * 50, 0))
  texting("LEVEL: " + str(level), font, constants.WIHTE, constants.SCREEN_WIDTH / 2, 15)
  texting(f"X{player.score}", font, constants.WIHTE, constants.SCREEN_WIDTH - 100, 15)

world_data = []
for row in range (150):
  r = [-1] * 150
  world_data.append(r)
with open(f'levels/level{level}_data.csv', newline="") as csvfile:
  reader = csv.reader(csvfile, delimiter = ",")
  for x, row in enumerate(reader):
    for y, tile in enumerate(row):
      world_data[x][y] = int(tile)

def reset():
  DT_group.empty()
  arrow_group.empty()
  i_group.empty()
  fire_group.empty()
  world_data = []
  for row in range (150):
    r = [-1] * 150
    world_data.append(r)
  return world_data
  
# my smaller classes
class DT(pygame.sprite.Sprite):
  def __init__(self, x, y, damage, color):
    pygame.sprite.Sprite.__init__(self)
    self.image = font.render(damage, True, color)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.counter = 0
  def update(self):
    self.rect.x += screen_scroll[0]
    self.rect.y += screen_scroll[1]
    self.rect.y -= 1
    self.counter += 1
    if self.counter > 30:
      self.kill()
      
class fade():
  def __init__(self, direction, color, speed):
    self.direction = direction
    self.color = color
    self.speed = speed
    self.fade_counter = 0
  def fadeing(self):
    fade_complete = False
    if self.direction == 1:
      self.fade_counter += self.speed
      pygame.draw.rect(screen, self.color, (0 - self.fade_counter,0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HIGHT))
      pygame.draw.rect(screen, self.color, (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HIGHT))
      pygame.draw.rect(screen, self.color, (0,0 - self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HIGHT // 2))
      pygame.draw.rect(screen, self.color, (0, constants.SCREEN_HIGHT // 2 + self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HIGHT ))
    elif self.direction == 2:
       pygame.draw.rect(screen, self.color, (0,0 , constants.SCREEN_WIDTH, 0 + self.fade_counter))
      
    if self.fade_counter >= constants.SCREEN_WIDTH:
      fade_complete = True
    return fade_complete
      
# sprite groups
DT_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
i_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 115,23,0,coins, True)
i_group.add(score_coin)
itemi = []

itemi.append(coins)
itemi.append(potion_image)

world = World()
world.data(world_data, tile_list, itemi, mob_animations)
player = world.player
for item in world.il:
  i_group.add(item)

bow = Bow(bow_image, arrow_image, sheild, sword)
blade = Sword()
enemy_list = world.character_l

intro_fade = fade(1, constants.PINK, 4)
death_fade = fade(2, constants.RED, 6)

#buttons
restart_button = Button(constants.SCREEN_WIDTH // 2 - 175,constants.SCREEN_HIGHT // 2 - 50, restart_img)
start_button = Button(constants.SCREEN_WIDTH // 2 - 145,constants.SCREEN_HIGHT // 2 - 150, start_img)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 110,constants.SCREEN_HIGHT // 2 + 50, exit_img)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175,constants.SCREEN_HIGHT // 2 - 150, resume_img)



#main game loop
run = True
while run:

  constants.CLOCK.tick(90)
  # starting game menu
  if start_game == False:
    screen.fill(constants.PINK)
    if start_button.draw(screen):
      start_game = True
      start_intro = True
    if exit_button.draw(screen):
      run = False
  else:
    # press space to pause, then you get this pause screen
    if pause_game:
      screen.fill(constants.BLACK)
      if exit_button.draw(screen):
        run = False
      if resume_button.draw(screen):
        pause_game = False
    else:
  
      screen.fill(constants.GRAY) #background color
      world.draw(screen)
      
      dx=0
      dy=0
      if player.alive:
        if m_l is True:
          dx = -5
        if m_r is True:
          dx = 5
        if m_u is True:
          dy = -5
        if m_d is True:
          dy = 5
      
        screen_scroll, level_conplete = player.move(dx, dy, world.obsticles, world.exit)
    
        world.update(screen_scroll)
        for enemy in enemy_list:
          fireball = enemy.ai(player, world.obsticles, screen_scroll , fire_img) 
          # update everything
          if fireball:
            fire_group.add(fireball)
          if enemy.alive:
            enemy.update(player)
        player.update(player)
        arrow = bow.update(player)
        DT_group.update()
        fire_group.update(screen_scroll, player)
        blade.update(player, enemy_list)
        i_group.update(screen_scroll,player, coin_fx, potion_fx)
      # draw everything
      i_group.draw(screen)
      if arrow:
        arrow_group.add(arrow)
        shot_fx.play()
      for arrow in arrow_group:
        damage, damage_pos = arrow.update(screen_scroll, enemy_list, world.obsticles)
        if damage:
          dt = DT(damage_pos.centerx, damage_pos.y, str(damage), constants.BLUE)
          DT_group.add(dt)
          hit_fx.play()
      damage, damage_pos = blade.update(player , enemy_list)
      if damage:
        dt = DT(damage_pos.centerx, damage_pos.centery, str(damage), constants.BLUE)
        DT_group.add(dt)
      for enemy in enemy_list:
        enemy.draw(screen)
      player.draw(screen)
      bow.draw(screen)
      for arrow in arrow_group:
        arrow.draw(screen)
      for hot in fire_group:
        hot.draw(screen)
      DT_group.draw(screen)
      info()
      score_coin.draw(screen)
      # transition to next level
      if level_conplete:
        start_intro = True
        level += 1
        world_data = reset()
        for row in range (150):
          r = [-1] * 150
          world_data.append(r)
        if level == 7:
          level = 1
        with open(f'levels/level{level}_data.csv', newline="") as csvfile:
          reader = csv.reader(csvfile, delimiter = ",")
          for x, row in enumerate(reader):
            for y, tile in enumerate(row):
              world_data[x][y] = int(tile)
        world = World()
        world.data(world_data, tile_list, itemi, mob_animations)
        tempscore = player.score
        temphp = player.hp
        player = world.player
        player.hp = temphp
        player.score = tempscore
        enemy_list = world.character_l
        score_coin = Item(constants.SCREEN_WIDTH - 115,23,0,coins, True)
        i_group.add(score_coin)
        for item in world.il:
          i_group.add(item)
      # the fade class coming into use
      if start_intro:
        if intro_fade.fadeing():
          start_intro = False
          intro_fade.fade_counter = 0
      if player.alive == False:
        death_fade.fade_counter += 1
        if death_fade.fadeing():
          if restart_button.draw(screen):
            death_fade.fade_counter = 0
            # basicly the level generator
            level = 1
            start_intro = True
            world_data = reset()
            for row in range (150):
              r = [-1] * 150
              world_data.append(r)
            with open(f'levels/level{level}_data.csv', newline="") as csvfile:
              reader = csv.reader(csvfile, delimiter = ",")
              for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                  world_data[x][y] = int(tile)
            world = World()
            world.data(world_data, tile_list, itemi, mob_animations)
            player = world.player
            enemy_list = world.character_l
            score_coin = Item(constants.SCREEN_WIDTH - 115,23,0,coins, True)
            i_group.add(score_coin)
            for item in world.il:
              i_group.add(item)
      
    
      
  # event handeler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        m_l = True
      if event.key == pygame.K_RIGHT:
        m_r = True
      if event.key == pygame.K_UP:
        m_u = True
      if event.key == pygame.K_DOWN:
        m_d = True
      if event.key == pygame.K_a:
        m_l = True
      if event.key == pygame.K_d:
        m_r = True
      if event.key == pygame.K_w:
        m_u = True
      if event.key == pygame.K_s:
        m_d = True
      if event.key == pygame.K_SPACE:
       pause_game = True
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT:
        m_l = False
      if event.key == pygame.K_RIGHT:
        m_r = False
      if event.key == pygame.K_UP:
        m_u = False
      if event.key == pygame.K_DOWN:
        m_d = False
      if event.key == pygame.K_a:
        m_l = False
      if event.key == pygame.K_d:
        m_r = False
      if event.key == pygame.K_w:
        m_u = False
      if event.key == pygame.K_s:
        m_d = False
    
  pygame.display.update()
# ヾ(•ω•`)o    <-- text emoji 
pygame.quit()