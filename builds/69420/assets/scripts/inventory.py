import pygame
import os

class Inventory:
    def __init__(self):
        self.icons = {}
        for icon in os.listdir("assets/images/inventory_icons"):
            self.icons[icon.removesuffix(".png")] = pygame.transform.scale(pygame.image.load(f"assets/images/inventory_icons/{icon}"), (32, 32))
        print(self.icons)
        self.space = [["empty" for _ in range(9)] for _ in range(3)]
        self.hotbar = ["empty" for _ in range(9)]
        self.active_slot = 0
        self.item_carrying = "empty"
        self.pressed = False
        self.x = 640
        self.y = 600

    def handle_mouse_interaction(self, scaled_mouse_pos):
        mouse_pressed = pygame.mouse.get_pressed()[0]

        self.item_carrying = self.handle_hotbar_mouse_interaction(self.item_carrying, scaled_mouse_pos)

        for index, row in enumerate(self.space):
            for spot, item in enumerate(row):
                rect = pygame.Rect(self.x - 450 + spot * 100, self.y - 500 + index * 100, 75, 75)

                if mouse_pressed and rect.collidepoint(scaled_mouse_pos) and not self.pressed:
                    if self.item_carrying == "empty":
                        self.item_carrying, row[spot] = item, "empty"
                    elif row[spot] == "empty":
                        row[spot], self.item_carrying = self.item_carrying, "empty"
                    else:
                        row[spot], self.item_carrying = self.item_carrying, row[spot]

        self.pressed = mouse_pressed

    def handle_hotbar_mouse_interaction(self, item_carrying, scaled_mouse_pos, no_space=False):
        mouse_pressed = pygame.mouse.get_pressed()[0]
        for spot, item in enumerate(self.hotbar):
            rect = pygame.Rect(self.x - 450 + spot * 100, self.y, 75, 75)
            if mouse_pressed and rect.collidepoint(scaled_mouse_pos) and not self.pressed:
                if item_carrying == "empty":
                    item_carrying, self.hotbar[spot] = item, "empty"
                elif self.hotbar[spot] == "empty":
                    self.hotbar[spot], item_carrying = item_carrying, "empty"
                else:
                    self.hotbar[spot], item_carrying = item_carrying, self.hotbar[spot]

        if no_space:
            self.pressed = mouse_pressed

        return item_carrying

    def draw(self, screen, scaled_mouse_pos):
        self.handle_mouse_interaction(scaled_mouse_pos)

        self.draw_hotbar(screen)
        self.draw_inventory_space(screen)

        if self.item_carrying != "empty":
            if not isinstance(self.item_carrying, list):
                screen.blit(self.icons[self.item_carrying], (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))
            else:
                key = self.item_carrying[0]
                screen.blit(self.icons[key], (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))


    def draw_hotbar(self, screen):

        for spot, item in enumerate(self.hotbar):
            s = pygame.surface.Surface((75, 75))
            s.set_alpha(200)
            if spot == self.active_slot:
                s.fill((200, 200, 200))
            else:
                s.fill((127, 127, 127))
            screen.blit(s, (self.x - 450 + spot * 100, self.y, 75, 75))
            pygame.draw.rect(screen, (0, 0, 0), (self.x - 450 + spot * 100, self.y, 75, 75), 5)

            if item != "empty":
                if not isinstance(item, list):
                    screen.blit(self.icons[item], (self.x - 450 + 22 + spot * 100, self.y + 22))
                else:
                    key = item[0]
                    screen.blit(self.icons[key], (self.x - 450 + 22 + spot * 100, self.y + 22))


    def draw_inventory_space(self, screen):

        for index, row in enumerate(self.space):
            for spot, item in enumerate(row):

                rect = pygame.Rect(self.x - 450 + spot * 100, self.y - 500 + index * 100, 75, 75)
                s = pygame.surface.Surface((75, 75))
                s.set_alpha(200)
                s.fill((127, 127, 127))

                screen.blit(s, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 5)

                if item != "empty":
                    if not isinstance(item, list):
                        screen.blit(self.icons[item], (self.x - 450 + 22 + spot * 100, self.y -478 + index * 100))
                    else:
                        key = item[0]
                        screen.blit(self.icons[key], (self.x - 450 + 22 + spot * 100, self.y -478 + index * 100))



class ChestStorage:
    def __init__(self):
        self.icons = {}
        for icon in os.listdir("assets/images/inventory_icons"):
             self.icons[icon.removesuffix(".png")] = pygame.transform.scale(pygame.image.load(f"assets/images/inventory_icons/{icon}"), (32, 32))
        self.space = [["empty" for _ in range(9)] for _ in range(3)]
        self.item_carrying = "empty"
        self.pressed = False
        self.x = 640
        self.y = 600

    def handle_mouse_interaction(self, item_carrying, scaled_mouse_pos):
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for index, row in enumerate(self.space):
            for spot, item in enumerate(row):
                rect = pygame.Rect(self.x - 450 + spot * 100, self.y - 500 + index * 100, 75, 75)

                if mouse_pressed and rect.collidepoint(scaled_mouse_pos) and not self.pressed:
                    if item_carrying == "empty":
                        item_carrying, row[spot] = item, "empty"
                    elif row[spot] == "empty":
                        row[spot], item_carrying = item_carrying, "empty"
                    else:
                        row[spot], item_carrying = item_carrying, row[spot]

        self.pressed = mouse_pressed
        return item_carrying

    def draw(self, item_carrying, screen, scaled_mouse_pos):
        self.item_carrying = self.handle_mouse_interaction(item_carrying, scaled_mouse_pos)

        self.draw_storage_space(screen)

        if self.item_carrying != "empty":
            if not isinstance(self.item_carrying, list):
                screen.blit(self.icons[self.item_carrying], (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))
            else:
                key = self.item_carrying[0]
                screen.blit(self.icons[key], (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))
        return self.item_carrying


    def draw_storage_space(self, screen):

        for index, row in enumerate(self.space):
            for spot, item in enumerate(row):

                rect = pygame.Rect(self.x - 450 + spot * 100, self.y - 500 + index * 100, 75, 75)
                s = pygame.surface.Surface((75, 75))
                s.set_alpha(200)
                s.fill((127, 127, 127))

                screen.blit(s, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 5)

                if item != "empty":
                    if not isinstance(item, list):
                        screen.blit(self.icons[item], (self.x - 450 + 22 + spot * 100, self.y -478 + index * 100))
                    else:
                        key = item[0]
                        screen.blit(self.icons[key], (self.x - 450 + 22 + spot * 100, self.y -478 + index * 100))
