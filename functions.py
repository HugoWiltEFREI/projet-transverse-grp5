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
    pygame.draw.rect(display, "yellow", rect, 2)
    collision_types = {
        'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        pygame.draw.rect(display, "green", tile[0], 2)
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
        pygame.draw.rect(display, "green", tile[0], 2)
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


def create_ball(liste, vX, vY):
    liste.append({"vx": vX, "vy": vY, "rebond_count": 0, "rect": False, "rect_collision": None})


def lancer_ball(liste, ball_image, list_tiles):
    for ball in liste:
        if not (ball["rect"]):
            ball["rect"] = ball_image.get_rect()
            ball["rect"].left = player_rect.left
            ball["rect"].bottom = player_rect.bottom
            ball["rect_collision"] = pygame.Rect(0, 0, 21, 21)

        if ball["rebond_count"] < 5:
            # pygame.draw.circle(display, "red", (round(ball["x"]) - scroll[0], round(ball["y"]) - scroll[1]),model.BALL_RADIUS)
            ball["rect"].left += ball["vx"] * model.temps
            ball["rect"].bottom += (ball["vy"] * model.temps) + (0.5 * model.gravite * model.temps ** 2)

            pygame.draw.rect(display, "purple", ball["rect_collision"])
            print("purple : ", ball["rect_collision"].x, ball["rect_collision"].y)

            ball["rect_collision"].left = ball["rect"].left + (ball["vx"] + model.gravite * model.temps) * model.temps
            ball["rect_collision"].bottom = ball["rect"].bottom + (
                    (ball["vy"] + model.gravite * model.temps) * model.temps) + (
                                                    0.5 * model.gravite * model.temps ** 2)

            # display.blit(ball_image, (round(ball["x"]) - scroll[0], round(ball["y"]) - scroll[1]))
            display.blit(ball_image, (ball["rect"].x - scroll[0], ball["rect"].y - scroll[1]))
            """
            pygame.draw.rect(display, "red", ball["rect"], 2)
            print("red : ", ball["rect"].x, ball["rect"].y)
            pygame.draw.rect(display, "orange", ball["rect_collision"])
            print("orange : ", ball["rect_collision"].x, ball["rect_collision"].y)"""

            for tile in list_tiles:
                pygame.draw.rect(display, "black", tile[0], 2)

            hit_list_ball = collision_test(ball["rect_collision"], list_tiles)
            for tile in hit_list_ball:

                test_right = abs(ball["rect"].right - tile[0].x)
                test_left = abs(ball["rect"].left - tile[0].x)
                test_bottom = abs(ball["rect"].bottom - tile[0].y)
                test_top = abs(ball["rect"].top - tile[0].y)

                if min(test_right, test_left) < min(test_top, test_bottom):
                    if test_right < test_left:
                        result = "right"
                    elif test_left < test_right:
                        result = "left"
                else:
                    if test_bottom < test_top:
                        result = "bottom"
                    elif test_top < test_bottom:
                        result = "top"

                if ball["rect_collision"].bottom > tile[0].top:
                    ball["rect"].bottom = tile[0].top
                    ball["vy"] = -ball["vy"] * 0.9
                    ball["rebond_count"] += 1


                elif ball["rect_collision"].top < tile[0].bottom:
                    ball["rect"].top = tile[0].bottom
                    ball["vy"] = -ball["vy"] * 1.2
                    # ball["rebond_count"] += 1

                elif ball["rect_collision"].right > tile[0].left:
                    ball["rect"].right = tile[0].left
                    ball["rebond_count"] = 5

                elif ball["rect_collision"].left < tile[0].right:
                    ball["rect"].left = tile[0].right
                    ball["rebond_count"] = 5
                    #"""

                pygame.draw.rect(display, "magenta", tile[0], 2)

            ball["vy"] += model.gravite * model.temps
