import pygame, time
from math import sqrt
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Game')
game_font = pygame.font.Font("../../../../../../../Downloads/VT323-Regular.ttf", int(100))
text = game_font.render("PRESS E", False, "brown")
cpt = ""
affichage = 1


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

grassimage = pygame.image.load("grassMid.png")
grasscenter = pygame.image.load("grassCenter.png")
castleimage = pygame.image.load("castleMid.png")
castlecenter = pygame.image.load("castleCenter.png")
water = pygame.image.load("liquidWater.png")

scroll = [0, 0]

game_map1 = """
------------------------------
------------------------------
o------ooo--------o-----------
x---oooxx-----oooox-----------
x------xxoooo-----x-----------
xooo---xx-------oox-----------
x-----------------x-----------
x---ooooooooooooo-x-----------
x------xx---------------------
xooooooxx-oooooooooo----------
xxxxxxxxx-----------o---------
x-----------------------------
x---------------------o-------
xoooooooooooooooooooooxooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
""".splitlines()


game_map2 = """
-----------------------------------------------------------------------------------------------0------------------
-----------------------------------------------------------------------------------------------0------------------
-----------------------------------------------------------------------------------------------0------------------
-----------------------------------------------------------------------------------------------0------------------
o----------------------------------------------------------------------------------------------0------------------
xo------------------oooooo---------------------------------------------------------------------0------------------
xxo--------------o----------o-----------------------------------------oooooooo---------------b-0------------------
xxxo-------------x----------x----------o---------o------------oooo-------------------oooo------0------------------
xxxxoooooooooooooxooooooooooxoooooooooox--oooooooxoooooooooo-----------------ooo------------ooo0------------------
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx--xxxxxxxxxxxxxxxxxx--------------------------------xxx0------------------
""".splitlines()

game_map3 = """
-----------------------------------------------------------------------------------------------0------------------
-----------------------------------------------------------------------------------------------0------------------
-----------------------------------------------------------------------------------------------0------------------
-----------------------------------------------------------------------------------------------0------------------
-----------------------------------------------------------------------------------------------0------------------
-------------------------CCCCC-----------------------------------------------------------------0------------------
------------------------Cc---cC----------------------------------------------------------------0------------------
-----------------------Cc-----cC---------------------------------------------------------------0------------------
CCCCCCCCCCCCCCCCCCCCCCCccCCCCCccCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCwwwwwwwwwwwwwwwwww
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccwwwwwwwwwwwwwwwwww
""".splitlines()

game_map = [list(lst) for lst in game_map3]
bow = pygame.image.load("bow.png")
spike = pygame.image.load("spike.png")

tl = {}
tl["o"] = grassimage
tl["x"] = grasscenter
tl["b"] = bow
tl["w"] = water
tl["C"] = castleimage
tl["c"] = castlecenter

player_img = pygame.image.load('perso2.png')
player_img = pygame.transform.scale_by(player_img, 0.04)
player_img.set_colorkey((255, 255, 255))

player_rect = pygame.Rect(25, 25, 30, 40)

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


def isinzone(x1, x2, x3, y1, y2, y3):
    if (x1 < x2 < x3) and (y1 < y2 < y3):
        return 1
    else:
        return 0


level = 2

coeur = pygame.image.load("hud_heartFull.png")
nombre_de_vie = 3

now = 0


def life_left(nombre_de_vie):
    i = 0
    while i < nombre_de_vie:
        screen.blit(coeur, (1500 + i * 80, 50))
        i += 1


def spike_level(level):
    if level == 1:
        display.blit(spike, (1085 - scroll[0], 850 - scroll[1]))
        display.blit(spike, (750 - scroll[0], 850 - scroll[1]))
    if level == 2:
        display.blit(spike, (985 - scroll[0], 465 - scroll[1]))
        display.blit(spike, (750 - scroll[0], 465 - scroll[1]))


derniereaction = 0
loop = 1
while loop:
    # CLEAR THE SCREEN
    display.fill((146, 244, 255))

    if player_rect.x > 947:
        scroll[0] += int(player_rect.x - scroll[0] - 947)
    if player_rect.y < 150:
        scroll[1] += (player_rect.y - scroll[1] - 540)

    # Tiles are blitted  ==========================
    tile_rects = []
    y = 0
    for line_of_symbols in game_map:
        x = 0
        for symbol in line_of_symbols:
            if symbol in tl:
                # draw the symbol for image
                display.blit(
                    tl[symbol], (x * 64 - scroll[0], y * 64 - scroll[1]))
            # draw a rectangle for every symbol except for the empty one
            if symbol != "-" and symbol != "O":
                tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
            x += 1
        y += 1
    # ================================================
    spike_level(level)

    gravite = 9.81

    # MOVEMENT OF THE PLAYER
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 6
    if moving_left:
        player_movement[0] -= 6
    player_movement[1] += momentum
    momentum += 0.3
    if momentum > 10:
        momentum = momentum + 0.2*gravite

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        air_timer = 0
        momentum = 0
    else:
        air_timer += 1
    if collisions["top"]:
        momentum = 0

    # Flip the player image when goes to the left
    if stay_right:
        display.blit(
            player_img, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
    else:
        display.blit(
            pygame.transform.flip(player_img, 1, 0),
            (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    statut = isinzone(450, player_rect.x, 515, 455, player_rect.y, 515)
    if statut and affichage == 1:
        display.blit(text, (800, 875))

    isinspike1 = isinzone(725, player_rect.x, 790, 490, player_rect.y + 30, 510)
    isinspike2 = isinzone(960, player_rect.x, 1025, 490, player_rect.y + 30, 510)

    if isinspike1 or isinspike2:
        if now - derniereaction > 2000:
            nombre_de_vie -= 1
            derniereaction = now


    now = pygame.time.get_ticks()

    cpteur = game_font.render(str(cpt), False, "brown")


    for event in pygame.event.get():
        if event.type == QUIT:
            loop = 0
        if (event.type == KEYDOWN) and (statut == 1) and (affichage != 0):
            if event.key == K_e:
                cpt = "Bow acquired"
                affichage = 0

        if pygame.mouse.get_pressed()[0] == True:
            x, y = pygame.mouse.get_pos()
            print(x, y)

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                loop = 0
            if event.key == K_RIGHT:
                moving_right = True
                stay_right = True
            if event.key == K_LEFT:
                moving_left = True
                stay_right = False
            if event.key == K_SPACE or event.key == K_UP:
                if air_timer < 3:
                    momentum = -9
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False


    screen.blit(pygame.transform.scale(display, (1920, 1080)), (0, 0))
    screen.blit(cpteur, (30, 30))
    if affichage != 0:
        screen.blit(bow, (465 - scroll[0], 465 - scroll[1]))
    life_left(nombre_de_vie)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
