import pygame
import sys
from pygame.locals import *


pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Game')

WINDOW_SIZE = (0, 0)
# This will be the Surface where we will blit everything
display = pygame.Surface((1920, 1080))
# Then we will scale (every frame) the display onto the screen
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)

moving_right = False
moving_left = False
# For the pygame.transform.flip(player_img, 1, 0)
stay_right = True
momentum = 0
air_timer = 0
dirtimage = pygame.image.load('dirt.jpg')
dirtimage = pygame.transform.scale_by(dirtimage,0.32)
game_map1 = """
<---->xxxx<----xxxx------xxxo
ox<----ooo-------oo---xxxxxxo
o------ooo--------o---xxxxxxo
o--->xxoo-----xxxxo---xxxxxxo
o------ooxxx<-----o---xxxxxxo
oxx<---oo-------xxo---xxxxxxo
o------oo---------o---xxxxxxo
o--->xxooxxxxxxx<-o---xxxxxxo
o------oo---------o---xxxxxxo
oxxxxxxoo-xxxxxxxxo---xxxxxxo
ooooooooo-------------xxxxxxo
ooooooooooooooooooo---xxxxxxo
ooooooooooooooooooo---xxxxxxo
ooooooooooooooooooo---xxxxxxo
ooooooooooooooooooo---xxxxxxo
ooooooooooooooooooo---------o
xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
""".splitlines()

game_map = [list(lst) for lst in game_map1]

tl = {}
tl["o"] = dirt_img = dirtimage
tl["x"] = grass_img = dirtimage
tl["<"] = grassr = dirtimage
tl[">"] = grassr = dirtimage


player_img = pygame.image.load('perso2.png')
player_img = pygame.transform.scale_by(player_img, 0.04)
player_img.set_colorkey((255, 255, 255))

player_rect = pygame.Rect(50, 50, 5, 13)


def collision_test(rect, tiles):
    "Returns the Rect of the tile with which the player collides"
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {
        'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


loop = 1
while loop:
    # CLEAR THE SCREEN
    display.fill((146, 244, 255))

    # Tiles are blitted  ==========================
    tile_rects = []
    y = 0
    for line_of_symbols in game_map:
        x = 0
        for symbol in line_of_symbols:
            if symbol in tl:
                # draw the symbol for image
                display.blit(
                    tl[symbol], (x * 64, y * 64))
            # draw a rectangle for every symbol except for the empty one
            if symbol != "-":
                tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
            x += 1
        y += 1
    # ================================================


    # MOVEMENT OF THE PLAYER
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 5
    if moving_left:
        player_movement[0] -= 5
    player_movement[1] += momentum
    momentum += 0.3
    if momentum > 3:
        momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        air_timer = 0
        momentum = 0
    else:
        air_timer += 1

    # Flip the player image when goes to the left
    if stay_right:
        display.blit(
            player_img, (player_rect.x, player_rect.y-25))
    else:
        display.blit(
            pygame.transform.flip(player_img, 1, 0),
            (player_rect.x, player_rect.y-25))

    for event in pygame.event.get():
        if event.type == QUIT:
            loop = 0

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                loop = 0
            if event.key == K_RIGHT:
                moving_right = True
                stay_right = True
            if event.key == K_LEFT:
                moving_left = True
                stay_right = False
            if event.key == K_SPACE:
                if air_timer < 6:
                    momentum = -9
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    screen.blit(pygame.transform.scale(display, (1920, 1080)), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
