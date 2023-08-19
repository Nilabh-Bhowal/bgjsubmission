import pygame

import assets.scripts.ui as ui
import assets.scripts.tile as tile
import assets.scripts.inventory as inventory


class Room:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.tiles = tile.TileManager(self.rect.copy())

    def draw(self, screen, scroll, editor=False):
        if (self.rect.left - scroll[0] <= 1280 and self.rect.right - scroll[0] >= 0) and (self.rect.top - scroll[1] <= 720 and self.rect.bottom - scroll[1] >= 0):
            self.tiles.draw(screen, scroll)
            if editor:
                pygame.draw.rect(screen, (0, 0, 255), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))


class Item:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, scroll):
        if (self.rect.left - scroll[0] <= 1280 and self.rect.right - scroll[0] >= 0) and (self.rect.top - scroll[1] <= 720 and self.rect.bottom - scroll[1] >= 0):
            pygame.draw.rect(screen, self.color, (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))


class DungeonRoom(Room):
    def __init__(self, x, y):
        super().__init__(x, y, 1024, 1024)


class Corridor(Room):
    def __init__(self, x, y):
        super().__init__(x, y, 256, 128)


class Chest(Item):
    def __init__(self, x, y, storage=None):
        super().__init__(x, y, 128, 64, (255, 175, 112))
        self.items = inventory.ChestStorage()
        if storage:
            self.items.space = storage
        self.dropped_items = []
        self.empty = False

    def draw_storage(self, item_carrying, screen):
        return self.items.draw(item_carrying, screen, pygame.mouse.get_pos())


class End(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 128, 128, (255, 255, 0))


class LevelEnter(Item):
    def __init__(self, x, y, level):
        super().__init__(x, y, 256, 128, (255, 100, 0))
        self.level = level

    def check_collision(self, player):
        return self.level if player.rect.colliderect(self.rect) else None

    def draw(self, screen, scroll):
        super().draw(screen, scroll)
        ui.title(str(self.level), self.rect.centerx - scroll[0], self.rect.centery - scroll[1], screen)


class Lock(Item):
    def __init__(self, x, y, key):
        super().__init__(x, y, 256, 64, (255, 0, 0))
        self.key = key
        self.unlocked = False

    def check_collision(self, player):
        if not self.unlocked and self.rect.colliderect(player):
            if isinstance(player.inventory.hotbar[player.inventory.active_slot], list) and (player.inventory.hotbar[player.inventory.active_slot][1] == self.key):
                self.unlocked = True
                return True
            if player.rect.top <= self.rect.bottom + 5 and player.rect.top >= self.rect.top and player.rect.left >= self.rect.left and player.rect.right <= self.rect.right:
                player.rect.top = self.rect.bottom + 11
                player.movement[1] = 0
                return
            elif player.rect.bottom >= self.rect.top - 5 and player.rect.bottom <= self.rect.bottom and player.rect.left >= self.rect.left and player.rect.right <= self.rect.right:
                player.rect.bottom = self.rect.top - 11
                player.movement[1] = 0
                return
            if player.rect.left <= self.rect.right + 5 and player.rect.left >= self.rect.left:
                player.rect.left = self.rect.right + 11
                player.movement[0] = 0
                return
            elif player.rect.right >= self.rect.left - 5:
                player.rect.right = self.rect.left - 11
                player.movement[0] = 0
                return


        for item in player.keys:
            if item == self.key and item[1] == "0":
                self.unlocked = True

    def draw(self, screen, scroll, editor=False):
        if not self.unlocked:
            super().draw(screen, scroll)
            if editor:
                ui.title(self.key, self.rect.centerx - scroll[0], self.rect.centery - scroll[1], screen)


def can_pass(player, current_room, rooms):
    # sourcery skip: instance-method-first-arg-name
    pu, pd, pl, pr = [False, False, False, False]
    for room in rooms:
        if room != current_room:
            pu = pu or player.rect.top - player.rect.height < room.rect.bottom \
                and player.rect.top > room.rect.top \
                and player.rect.left >= room.rect.left - 21 \
                and player.rect.right <= room.rect.right + 21
            pd = pd or player.rect.bottom + player.rect.height > room.rect.top \
                and player.rect.bottom < room.rect.bottom\
                and player.rect.left >= room.rect.left - 21 \
                and player.rect.right <= room.rect.right + 21
            pl = pl or player.rect.left - player.rect.width < room.rect.right \
                and player.rect.left > room.rect.left \
                and player.rect.top >= room.rect.top - 21 \
                and player.rect.bottom <= room.rect.bottom + 21
            pr = pr or player.rect.right + player.rect.width > room.rect.left \
                and player.rect.right < room.rect.right \
                and player.rect.top >= room.rect.top - 21 \
                and player.rect.bottom <= room.rect.bottom + 21
    return pu, pd, pl, pr


# control player collision within room
def collide(player, rooms, dt):
    collided = False
    for room in rooms:
        if player.rect.colliderect(room):
            pu, pd, pl, pr = can_pass(player, room, rooms)
            if ((not pl) or dt > 4) and player.rect.left <= room.rect.left + 5:
                player.rect.left = room.rect.left + 11
                player.movement[0] = 0
                collided = True
            elif ((not pr) or dt > 4) and player.rect.right >= room.rect.right - 5:
                player.rect.left = room.rect.right - player.rect.width - 11
                player.movement[0] = 0
                collided = True

            if ((not pu) or dt > 4) and player.rect.top < room.rect.top + 5:
                player.rect.top = room.rect.top + 11
                player.movement[1] = 0
                collided = True
            elif ((not pd) or dt > 4) and player.rect.bottom >= room.rect.bottom - 5:
                player.rect.top = room.rect.bottom - player.rect.height - 11
                player.movement[1] = 0
                collided = True
    return collided
