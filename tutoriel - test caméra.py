import pygame
import random
import math

pygame.init()

pygame.display.set_caption("Camera")

screen = pygame.display.set_mode((800, 400))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player
x_player = 60
y_player = 60
player_rect = pygame.Rect(50, 50, x_player, y_player)
move_left = False
move_right = False

clock = pygame.time.Clock()

run = True
while run:

    clock.tick(60)

    screen.fill(WHITE)

    if move_left:
        player_rect.x -= 3
    if move_right:
        player_rect.x += 3

    pygame.draw.rect(screen, BLACK, player_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False

    pygame.display.update()

pygame.quit()
