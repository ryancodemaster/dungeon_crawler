from items import Item
from character import Character
# uses tilemaps to make the... ummm... maps.
class World():

  def __init__(self):
    self.map_tiles = []
    self.obsticles = []
    self.exit = None
    self.il = []
    self.player = None
    self.character_l = []
  def data(self, data, tile_list, itemi, mob_animations):

    # generating tilemaps tiles
    self.levellen = len(data)
    for y, row in enumerate(data):
      for x, tile in enumerate(row):
        image = tile_list[tile]
        image_rect = image.get_rect()
        image_x = x * 48
        image_y = y * 48
        image_rect.center = (image_x, image_y)
        tile_data = [image, image_rect, image_x, image_y]
        if tile == 7:
          self.obsticles.append(tile_data)
        elif tile == 8:
          self.exit = tile_data
        elif tile == 9:
          tile_data[0] = tile_list[5]
          coin = Item(image_x, image_y, 0, itemi[0])
          self.il.append(coin)
        elif tile == 11:#player
          player = Character(image_x,image_y, mob_animations, 0, 100)#player
          self.player = player#player
          tile_data[0] = tile_list[2]#player
        elif tile == 10:
          potion = Item(image_x, image_y, 1, [itemi[1]])
          self.il.append(potion)
          tile_data[0] = tile_list[0]

        #make all the mobs
        elif tile == 12:
          enemy = Character(image_x,image_y, mob_animations, 1, 100)
          self.character_l.append(enemy)
          tile_data[0] = tile_list[0]
        elif tile == 13:
          enemy = Character(image_x,image_y, mob_animations, 2, 100)
          self.character_l.append(enemy)
          tile_data[0] = tile_list[0]
        elif tile == 14:
          enemy = Character(image_x,image_y, mob_animations, 3, 100)
          self.character_l.append(enemy)
          tile_data[0] = tile_list[0]
        elif tile == 15:
          enemy = Character(image_x,image_y, mob_animations, 4, 100)
          self.character_l.append(enemy)
          tile_data[0] = tile_list[0]
        elif tile == 16:
          enemy = Character(image_x,image_y, mob_animations, 5, 100)
          self.character_l.append(enemy)
          tile_data[0] = tile_list[0]
        elif tile == 17:
          enemy = Character(image_x,image_y, mob_animations, 6, 100, 2, True)
          self.character_l.append(enemy)
          tile_data[0] = tile_list[3]
        
        

        if tile >= 0:
          self.map_tiles.append(tile_data)


  
  def update (self, screen_scroll):
    for tile in self.map_tiles:
      tile[2] += screen_scroll[0]
      tile[3] += screen_scroll[1]
      tile[1].center = (tile[2], tile[3])
  


  def draw(self, surface):
    for tile in self.map_tiles:
      surface.blit(tile[0], tile[1])
