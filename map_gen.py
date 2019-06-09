import pygame
import random
import numpy as np


class Empire:
    def __init__(self, empire_ID):
        self.empire_ID = empire_ID
        self.empire_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.town_list = []


class Tile:
    def __init__(self):
        self.color = (0, 0, 0)
        self.tile_ID = -1

    def set_color(self, r, g, b):
        self.color = (r, g, b)


class Land(Tile):
    def __init__(self):
        super().__init__()
        self.set_color(255, 255, 255)
        self.tile_ID = 0


class Water(Tile):
    def __init__(self):
        super().__init__()
        self.set_color(0, 0, 255)
        self.tile_ID = 1


class Town(Tile):
    def __init__(self, color):
        self.BASE_STRENGTH_MIN = 5
        self.BASE_STRENGTH_MAX = 10

        self.BASE_POPULATION_MIN = 10
        self.BASE_POPULATION_MAX = 20

        self.BASE_HEALTH = 50

        self.strength = random.randint(self.BASE_STRENGTH_MIN, self.BASE_STRENGTH_MAX)
        self.population = random.randint(self.BASE_POPULATION_MIN, self.BASE_POPULATION_MAX)
        self.health = self.BASE_HEALTH
        self.plague = False

        self.set_color(color)

        super().__init__()
        self.tile_ID = 2

    def set_color(self, color):
        self.color = color


class Map:
    def __init__(self, empire_amount):
        # set dimensions
        self.TILESIZE = 5
        self.MAPW = 100
        self.MAPH = 50
        self.BODIES_OF_WATER = 3
        self.SPREAD_AMOUNT = 15

        self.empire_count = 0
        self.empire_list = []*empire_amount
        print(len(self.empire_list))

        for i in range(empire_amount):
            self.generate_empire(i)

        # set tilemap
        self.tilemap = [[Land() for i in range(self.MAPW)] for j in range(self.MAPH)]
        '''
        self.tilemap = np.empty(shape=(self.MAPH, self.MAPW))
        self.tilemap.fill(Land())
        '''
        print(self.tilemap)
        print(len(self.tilemap), "x", len(self.tilemap[0]))

        for i in range(self.BODIES_OF_WATER):
            self.water_spawn()

        for i in range(self.SPREAD_AMOUNT):
            self.water_spread()

        # set display
        pygame.init()
        self.DISPLAY_SURFACE = pygame.display.set_mode((self.MAPW * self.TILESIZE, self.MAPH * self.TILESIZE))

    @staticmethod
    def coin_flip():
        return 1 if random.random() < 0.5 else -1

    def water_spawn(self):
        r = random.randint(1, self.MAPH - 1)
        c = random.randint(1, self.MAPW - 1)
        self.tilemap[r][c] = Water()

    def water_spread(self):
        for r in range(0, self.MAPH - 1):
            for c in range(0, self.MAPW - 1):
                if self.tilemap[r][c].tile_ID == Water().tile_ID:
                    pot_r = r + self.coin_flip()
                    pot_c = c + self.coin_flip()

                    if pot_r < self.MAPH and pot_c < self.MAPW:
                        self.tilemap[pot_r][pot_c] = Water()

    def generate_empire(self, i):
        self.empire_list.append(Empire(i))

    def town_spawn(self):
        for empire in self.empire_list:
            r = random.randint(1, self.MAPH - 1)
            c = random.randint(1, self.MAPW - 1)
            if self.tilemap[r][c].tile_ID == Land().tile_ID:
                self.tilemap[r][c] = Town(empire.empire_color)

    def update_map(self):
        for row in range(self.MAPH):
            for col in range(self.MAPW):
                pygame.draw.rect(self.DISPLAY_SURFACE, self.tilemap[row][col].color,
                                 (col * self.TILESIZE, row * self.TILESIZE, self.TILESIZE, self.TILESIZE))

        pygame.display.update()
