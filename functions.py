import pygame
from pygame.locals import KEYDOWN, K_r

from levels import game_map1, game_map2



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


def isinzone(x1, x2, x3, y1, y2, y3):
    if (x1 < x2 < x3) and (y1 < y2 < y3):
        return 1
    else:
        return 0


def life_left(nombre_de_vie):
    i = 0
    while i < nombre_de_vie:
        screen.blit(heart, (1740 - i * 80, 50))
        i += 1


def diedFromVoid(posY):
    global nombre_de_vie
    if (posY>900):
        nombre_de_vie = 0


def spike_level(level):
    if level == 2:
        display.blit(spike, (1085 - scroll[0], 850 - scroll[1]))
        display.blit(spike, (750 - scroll[0], 850 - scroll[1]))
    if level == 1:
        display.blit(spike, (985 - scroll[0], 465 - scroll[1]))
        display.blit(spike, (750 - scroll[0], 465 - scroll[1]))


def is_dead(event, nombre_de_vie, player_velocity_multi, display_dead):
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
    return display_dead, player_velocity_multi, nombre_de_vie


def select_map(level):
    global game_map
    if level ==1:
       game_map = [list(lst) for lst in game_map1]
    if level == 2:
        game_map = [list(lst) for lst in game_map2]
    return game_map


def level_actions(level):
    spike_level(level)


display = pygame.Surface((1920, 1080))
WINDOW_SIZE = (0, 0)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
heart = pygame.image.load("hud_heartFull.png")
spike = pygame.image.load("spike.png")
scroll = [0, 0]
player_rect = pygame.Rect(25, 25, 30, 40)
