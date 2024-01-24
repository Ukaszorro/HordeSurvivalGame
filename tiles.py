import pygame
from settings import tile_size


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super(Tile, self).__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.tiles = pygame.sprite.Group()

    def setup_level(self, layout):

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 1:
                    x = col_index * tile_size
                    y = row_index * tile_size
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)

    def run(self):
        self.tiles.draw(self.display_surface)
