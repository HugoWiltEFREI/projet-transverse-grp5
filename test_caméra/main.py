import pygame
from pygame.locals import *
import equations

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Game')
game_font = pygame.font.Font("VT323-Regular.ttf", int(100))
text = game_font.render("PRESS E", False, "brown")
zone_de_text = ""
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

scroll = [0, 0]

game_map2 = """
------------------------------
------------------------------
o------ooo--------o-----------
x---oooxx--------ox-----------
x------xxoooo-----x-----------
xooo---xx-------oox-----------
x-----------------x-----------
x---ooooooooooooo-x-----------
x------xx---------x-----------
xooooooxx-oooooooox-----------
xxxxxxxxx---------------------
x-----------------------------
x-----------------------------
xooooooooooooooooooooooooooooo
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
""".splitlines()

game_map1 = """
-------------------------------------------------------------------------------------------------0------------------
-------------------------------------------------------------------------------------------------0------------------
-------------------------------------------------------------------------------------------------0------------------
-------------------------------------------------------------------------------------------------0------------------
-------------------------------------------------------------------------------------------------0------------------
ooo----------------------------------------------------------------------------------------------0------------------
xxxo------------------oooooo---------------------------------------------------------------------0------------------
xxxxooooooooooooooo----------o-----------------------------------------oooooooo-----------------0------------------
xxxxxxxxxxxxxxxxxxxo----------x----------o---------o------------oooo-------------------oooo------0------------------
xxxxxxxxxxxxxxxxxxxxooooooooooxoooooooooox--oooooooxoooooooooo-----------------ooo------------ooo0------------------
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx--xxxxxxxxxxxxxxxxxx--------------------------------xxx0------------------
""".splitlines()

game_map = [list(lst) for lst in game_map1]
bow = pygame.image.load("bow.png")
spike = pygame.image.load("spike.png")

tl = {"o": grassimage, "x": grasscenter}

player_img = pygame.image.load('perso.png')
player_img = pygame.transform.scale_by(player_img, 0.04)
player_img.set_colorkey((255, 255, 255))

player_rect = pygame.Rect(25, 25, 30, 40)

nombre_de_vie = 3
now = 0
level = 2
display_dead = 0
derniereaction = 0

loop = 1
player_velocity_multi = 1


coeur = pygame.image.load("hud_heartFull.png")
game_font2 = pygame.font.Font("VT323-Regular.ttf", int(150))
text2 = game_font2.render("PRESS R TO RESTART", False, "brown")

def collision_test(rect, tiles):
    #Return le rect en collision avec le player
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



# def __moveBall():
#     """ Calculates the new position (x,y), new speed (speedX, speedY) of the ball.
#         Also controls its bounce.
#             x(t+1) = x(t) + Vx(t) * cos(α) * Δt
#             Vx(t+1) = Vx(t) with no bounce
#             Vx(t+1) = Vx(t) * frictionX on a bounce
#             y(t+1) = y(t) + Δt * (Vy(t) - (g * Δt))
#             Vy(t+1) = Vy(t) - g * Δt with no bounce
#             Vy(t+1) = (Vy(t) - g * Δt) * frictionX on a bounce
#     """
#
#     """ Calculates the new y, y(t+1)."""
#     BallBounceModel.ball['y'] += BallBounceModel.INTERVAL * (
#                 BallBounceModel.ball['speedY'] - (BallBounceModel.GRAVITY * BallBounceModel.INTERVAL))
#
#     """ Calculates the new speedY, Vy(t+1)."""
#     BallBounceModel.ball['speedY'] += - BallBounceModel.GRAVITY * BallBounceModel.INTERVAL
#
#
#     """ Calculates the new speedY, Vy(t+1)."""
#     if bounceX:
#         """ Change angle after a bounce."""
#         BallBounceModel.ball['angle'] = (180 - BallBounceModel.ball['angle']) % 360
#         """ Applies friction on the new speedX."""
#         BallBounceModel.ball['speedX'] = BallBounceModel.ball['speedX'] * BallBounceModel.FRICTION_X


def isinzone(x1, x2, x3, y1, y2, y3):
    if (x1 < x2 < x3) and (y1 < y2 < y3):
        return 1
    else:
        return 0


def life_left(nombre_de_vie):
    i = 0
    while i < nombre_de_vie:
        screen.blit(coeur, (1500 + i * 80, 50))
        i += 1

def diedFromVoid(posY):
    global nombre_de_vie
    if (posY>1000):
        nombre_de_vie = 0


def spike_level(level):
    if level == 1:
        display.blit(spike, (1085 - scroll[0], 850 - scroll[1]))
        display.blit(spike, (750 - scroll[0], 850 - scroll[1]))
    if level == 2:
        display.blit(spike, (985 - scroll[0], 465 - scroll[1]))
        display.blit(spike, (750 - scroll[0], 465 - scroll[1]))


def is_dead():
    global display_dead, nombre_de_vie, player_velocity_multi
    if nombre_de_vie <= 0:
        display_dead = 1
        player_velocity_multi = 0
        if event.type == KEYDOWN:
            if event.key == K_r:
                nombre_de_vie = 3
                display_dead = 0
                player_rect.x = 10
                player_rect.y = 10
                player_velocity_multi = 1
                scroll[0], scroll[1] = 0, 0

def level_actions(level):
    spike_level(level)


while loop:
    # CLEAR THE SCREEN
    display.fill((146, 244, 255))

    if player_rect.x > 950:
        scroll[0] += int(player_rect.x - scroll[0] - 950)
    if player_rect.y < 150:
        scroll[1] += (player_rect.y - scroll[1] - 540)

    # Affichage des blocks
    tile_rects = []
    y = 0
    for line_of_symbols in game_map:
        x = 0
        for symbol in line_of_symbols:
            if symbol in tl:
                # Blit des images avec coords
                display.blit(
                    tl[symbol], (x * 64 - scroll[0], y * 64 - scroll[1]))
            # Hitboxs pour les images avec collisions
            if symbol != "-" and symbol != "O":
                tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
            x += 1
        y += 1

    spike_level(level)

    # MOVEMENT OF THE PLAYER
    INTERVAL = 0.22  # The time interval, Δt.
    pos = {'x': 0, 'y': 0}
    GRAVITE = 9.80665

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 6 * player_velocity_multi
    if moving_left:
        player_movement[0] -= 6 * player_velocity_multi
    player_movement[1] += momentum
    momentum += 0.3 * player_velocity_multi
    if momentum > 3:
        momentum = 3*GRAVITE*INTERVAL        #_____________________________________________________

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        air_timer = 0
        momentum = 0
    else:
        air_timer += 1
    if collisions["top"]:
        momentum = 0

    # Flip the player image when goes to the left
    if player_velocity_multi == 1:
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

    cpteur = game_font.render(str(zone_de_text), False, "brown")

    for event in pygame.event.get():
        if event.type == QUIT:
            loop = 0

        if (event.type == KEYDOWN) and (statut == 1) and (affichage != 0):
            if event.key == K_e:
                zone_de_text = "Bow acquired"
                affichage = 0

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            print(x, y)

        is_dead()
        diedFromVoid(player_rect.y)

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
                    momentum = -3*GRAVITE*INTERVAL
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    screen.blit(pygame.transform.scale(display, (1920, 1080)), (0, 0))
    screen.blit(cpteur, (30, 30))
    if affichage != 0:
        screen.blit(bow, (465 - scroll[0], 465 - scroll[1]))
    if display_dead != 0:
        screen.blit(text2, (400, 100))
    life_left(nombre_de_vie)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
