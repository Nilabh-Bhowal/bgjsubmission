import pygame
import os
import json

class Animation:
    def __init__(self, folder):
        self.frame = 0
        path = f"assets/images/animations/{folder}"
        with open(f"{path}/data.json", "r") as f:
            animations = json.load(f)
        self.data = {}
        for animation in animations:
            self.data[animation["name"]] = []
            for image in os.listdir(f"{path}/{animation['name']}"):
                for _ in range(round(animation["length"] / len(os.listdir(f"{path}/{animation['name']}")))):
                    self.data[animation["name"]].append(pygame.transform.scale2x(pygame.image.load(f"{path}/{animation['name']}/{image}")))
        self.current_animation = list(self.data.keys())[0]

    def update(self):
        self.frame += 1
        if self.frame > len(self.data[self.current_animation]) - 1:
            self.frame = len(self.data[self.current_animation]) - 1
            return True
        return False

    def change_animation(self, animation):
        if self.current_animation != animation:
            self.current_animation = animation
            self.frame = 0

    def get_image(self):
        return self.data[self.current_animation][self.frame]
