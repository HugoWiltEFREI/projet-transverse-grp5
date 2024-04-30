import pygame
from pygame.locals import KEYDOWN, K_r

import model
from levels import game_map1, game_map2, game_map3


def is_dead(event):
    if model.number_of_life == 0:
        model.display_dead = 1
        model.player_velocity_multi = 0
        if event.type == KEYDOWN and event.key == K_r:
            model.number_of_life = 3
            model.display_dead = 0
            player_rect.x = 10
            player_rect.y = 10
            model.player_velocity_multi = 1
            scroll[0], scroll[1] = 0, 0


def collision_test(rect, tiles):
    # Return le rect en collision avec le player
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile[0]):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {
        'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile[0].left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile[0].right
            collision_types['left'] = True
        collisionPortal(tile)

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile[0].top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile[0].bottom
            collision_types['top'] = True
        collisionPortal(tile)
    return rect, collision_types


def collisionPortal(tile):
    if tile[1] == 's':
        forward_lvl()
        player_rect.x = 30
        player_rect.y = 30
        scroll[0] = 0
        scroll[1] = 0


def isinzone(x1, x2, x3, y1, y2, y3):
    if (x1 < x2 < x3) and (y1 < y2 < y3):
        return 1
    else:
        return 0


def life_left():
    i = 0
    while i < model.number_of_life:
        screen.blit(heart, (1740 - i * 80, 50))
        i += 1


def spike_level(level):
    if level == 1:
        display.blit(spike, (985 - scroll[0], 465 - scroll[1]))
        display.blit(spike, (750 - scroll[0], 465 - scroll[1]))
    if level == 2:
        display.blit(spike, (1110 + 200 - scroll[0], 465 - scroll[1]))
        display.blit(spike, (875 + 200 - scroll[0], 465 - scroll[1]))


def select_map(level):
    global game_map
    if level == 1:
        game_map = [list(lst) for lst in game_map1]
    if level == 2:
        game_map = [list(lst) for lst in game_map2]
    if level == 3:
        game_map = [list(lst) for lst in game_map3]
    return game_map


def diedFromVoid(posY):
    if posY > 900:
        model.number_of_life = 0
        model.display_dead = 1


def level_actions(level):
    spike_level(level)


display = pygame.Surface((1920, 1080))
WINDOW_SIZE = (0, 0)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
heart = pygame.image.load("textures/hud_heartFull.png")
spike = pygame.image.load("textures/spike.png")
scroll = [0, 0]
player_rect = pygame.Rect(25, 25, 30, 40)


def forward_lvl():
    model.level %= 3
    model.level += 1
