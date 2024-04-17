# Mouvement Uniformément Accéléré (MRUA)
# x = x0 + v0*t + 1/2*a*t^2
# x la position, x0 la position initiale
# v0 la vitesse initiale, a l'accélération et t le temps écoulé
# L'idée est d"implémenter ça dans pygame sur un objet
# De par la nature du mouvement, l'objet bougera en accélérant petit à petit, le but et de réinitialiser la vitesse et la position initiale à chaque fois que l'objet s'arrête


import pygame
import math

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([1500, 1000])

positionInitiale = 0
vitesseInitiale = 10
temps = 0
acceleration = 5

player = pygame.Rect(positionInitiale, 50, 100, 100)

moveRight = False
moveLeft = False

running = True
while running:

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, "black", player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RIGHT:
                moveRight = True
            elif event.key == pygame.K_LEFT:
                moveLeft = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moveRight = False
                positionInitiale = player.x
                temps = 0
            if event.key == pygame.K_LEFT:
                moveLeft = False
                positionInitiale = player.x
                temps = 0

    if moveRight:
        player.x = positionInitiale + vitesseInitiale*temps + 1/2*acceleration*(temps**2)
        temps += 1/6  # 60 frames par millisecondes
    elif moveLeft:
        player.x = positionInitiale - (vitesseInitiale*temps + 1/2*acceleration*(temps**2))
        temps += 1/6  # 60 frames par millisecondes




    pygame.display.update()

    clock.tick(60)

pygame.quit()
