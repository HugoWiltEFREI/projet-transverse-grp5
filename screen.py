import pygame as pg

class SpriteSheet:
    def __init__(self, filename, bg=None):
        self.spritesheet = pg.image.load(filename).convert()
        self.bg = bg
    def get_image(self, frame):
        image = self.spritesheet.subsurface(pg.Rect(frame))

        if self
        return image

