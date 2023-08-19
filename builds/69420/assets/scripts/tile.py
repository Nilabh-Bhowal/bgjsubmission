import pygame
import os
import json

class TileManager:
    def __init__(self, rect):
        self.rect = rect
        self.tile_path = "assets/images/tiles"
        with open(f"{self.tile_path}/tile_types.json", "r") as f:
            tiles = json.load(f)
        self.tiles = {}
        for number, image in enumerate(os.listdir(self.tile_path)):
            if image.endswith("png"):
                self.tiles[f"{list(tiles.keys())[number]}"] = pygame.transform.scale(pygame.image.load(f"{self.tile_path}/{image}").convert(), (32, 32))

        self.tile_map = [[{"type": "empty", "top": False, "bottom": False, "left": False, "right": False} for _ in range(self.rect.width // 32)] for _ in range(self.rect.height // 32)]

    def load_rooms(self, rooms):
        for y, row in enumerate(self.tile_map):
            for x, tile in enumerate(row):
                tile_rect = pygame.Rect(self.rect.x + x * 32, self.rect.y + y * 32, 32, 32)
                for room in rooms:
                    if room.rect != self.rect:
                        if not tile["left"] and (room.rect.colliderect(tile_rect.move(-5, 0)) or x > 0):
                            tile["left"] = True
                        if not tile["right"] and (room.rect.colliderect(tile_rect.move(5, 0)) or x < self.rect.width // 32 - 1):
                            tile["right"] = True
                        if not tile["top"] and (room.rect.colliderect(tile_rect.move(0, -5)) or y > 0):
                            tile["top"] = True
                        if not tile["bottom"] and (room.rect.colliderect(tile_rect.move(0, 5)) or y < self.rect.height // 32 - 1):
                            tile["bottom"] = True

        self.add_to_map()

    def add_to_map(self):
        for row in self.tile_map:
            for tile in row:
                if tile["bottom"] and tile["top"] and tile["left"] and tile["right"]:
                    tile["type"] = "center"
                elif tile["bottom"] and not tile["top"]:
                    if tile["right"] and not tile["left"]:
                        tile["type"] = "topleft"
                    elif tile["left"] and not tile["right"]:
                        tile["type"] = "topright"
                    else:
                        tile["type"] = "top"
                elif tile["top"] and not tile["bottom"]:
                    if tile["right"] and not tile["left"]:
                        tile["type"] = "bottomleft"
                    elif tile["left"] and not tile["right"]:
                        tile["type"] = "bottomright"
                    else:
                        tile["type"] = "bottom"
                elif tile["right"]:
                    tile["type"] = "left"
                elif tile["left"]:
                    tile["type"] = "right"

    def draw(self, screen, scroll):
        for y, row in enumerate(self.tile_map):
            for x, tile in enumerate(row):
                if tile["type"] != "empty":
                    screen.blit(self.tiles[tile["type"]], (self.rect.x + (x * 32) - scroll[0], self.rect.y + (y * 32) - scroll[1]))
