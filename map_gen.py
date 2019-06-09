import pygame
import random
import numpy as np


class Map:
    def __init__(self):
        # base colors
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)

        # base cell types
        self.WATER = -1
        self.LAND = 0

        self.color_dict = {
            self.WATER: self.BLUE,
            self.LAND: self.WHITE
        }

        # set dimensions
        self.TILESIZE = 5
        self.MAPW = 150
        self.MAPH = 100
        self.BODIES_OF_WATER = 4
        self.SPREAD_AMOUNT = 25

        # set tilemap
        # tilemap = [[LAND for pos in range(MAPH)] for pos in range(MAPW)]
        self.tilemap = np.empty(shape=(self.MAPH, self.MAPW))
        self.tilemap.fill(self.LAND)

        for i in range(self.BODIES_OF_WATER):
            self.water_spawn()

        for i in range(self.SPREAD_AMOUNT):
            self.water_spread()

        # set display
        pygame.init()
        self.DISPLAY_SURFACE = pygame.display.set_mode((self.MAPW * self.TILESIZE, self.MAPH * self.TILESIZE))
        print(self.tilemap)

    def coin_flip(self):
        return 1 if random.random() < 0.5 else -1

    def water_spawn(self):
        r = random.randint(1, self.MAPH - 1)
        c = random.randint(1, self.MAPW - 1)
        self.tilemap[[r], [c]] = self.WATER

    def water_spread(self):
        for r in range(0, self.MAPH):
            for c in range(0, self.MAPW):
                if self.tilemap[r, c] == self.WATER:
                    pot_r = r + self.coin_flip()
                    pot_c = c + self.coin_flip()

                    if pot_r < self.MAPH and pot_c < self.MAPW:
                        self.tilemap[[pot_r], [pot_c]] = self.WATER

    def update_map(self):
        for row in range(self.MAPH):
            for col in range(self.MAPW):
                pygame.draw.rect(self.DISPLAY_SURFACE, self.color_dict[self.tilemap[row][col]],
                                 (col * self.TILESIZE, row * self.TILESIZE, self.TILESIZE, self.TILESIZE))

        pygame.display.update()
