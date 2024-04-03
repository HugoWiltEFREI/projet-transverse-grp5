import pygame
from pygame.locals import *

from functions import *

pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption('Game')
game_font = pygame.font.Font("VT323-Regular.ttf", int(100))
text = game_font.render("PRESS E", False, "brown")
zone_de_text = ""
affichage = 1


moving_right = False
moving_left = False
# For the pygame.transform.flip(player_img, 1, 0)
stay_right = True
momentum = 0
air_timer = 0

grassimage = pygame.image.load("grassMid.png")
grasscenter = pygame.image.load("grassCenter.png")
bow = pygame.image.load("bow.png")

tl = {"o": grassimage, "x": grasscenter}
game_font2 = pygame.font.Font("VT323-Regular.ttf", int(150))
text2 = game_font2.render("PRESS R TO RESTART", False, "brown")

player_img = pygame.image.load('perso.png')
player_img = pygame.transform.scale_by(player_img, 0.04)
player_img.set_colorkey((255, 255, 255))

nombre_de_vie = 3
now = 0
level = 1
display_dead = 0
derniereaction = 0
loop = 1
player_velocity_multi = 1


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
    for line_of_symbols in select_map(level):
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
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 6 * player_velocity_multi
    if moving_left:
        player_movement[0] -= 6 * player_velocity_multi
    player_movement[1] += momentum
    momentum += 0.3 * player_velocity_multi
    if momentum > 3:
        momentum = 3

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

        is_dead(event, nombre_de_vie, player_velocity_multi, display_dead)
        diedFromVoid(player_rect.y)

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                loop = 0
            if event.key == K_c:
                print(player_rect.x, player_rect.y)

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
    if display_dead != 0:
        screen.blit(text2, (400, 100))
    life_left(nombre_de_vie)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
