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
            self.data[animation["type"]] = []
            for image in os.listdir(f"{path}/{animation['type']}"):
                for _ in range(round(animation["length"] / len(os.listdir(f"{path}/{animation['type']}")))):
                    self.data[animation["type"]].append(pygame.image.load(f"{path}/{animation['type']}/{image}"))
        self.current_animation = list(self.data.keys())[0]

    def update(self, dt):
        self.frame += 1
        if self.frame > len(self.data[self.current_animation]) - 1:
            self.frame = 0

    def change_animation(self, animation):
        self.current_animation = animation
        self.frame = 0

    def get_image(self):
        return self.data[self.current_animation][self.frame]
