from os import path

from spritesheet import SpriteSheet

def load(self):
    spritesheet = SpriteSheet(path.join(self.screen.game.img_dir, 'spritesheet.png'))

    #get image
    standing_frame = (0, 704, 64, 64)
    self.image = spritesheet.get_image(standing_frame)