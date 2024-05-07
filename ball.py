import pygame
import sys
import math

# Initialisation de Pygame
pygame.init()

# Définition de la taille de la fenêtre
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouvement Parabolique")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Paramètres de la balle
BALL_RADIUS = 10
BALL_COLOR = RED
ANGLE_DEG = 65
v0 = 60  # Vitesse initiale de la balle
GRAVITY = 9.81  # Accélération due à la gravité en m/s^2
TIME_INTERVAL = 0.5  # Intervalle de temps entre chaque frame

# Convertir l'angle de degrés en radians
ANGLE_RAD = math.radians(ANGLE_DEG)

# Calculer les composantes de la vitesse initiale
INITIAL_VX = v0 * math.cos(ANGLE_RAD)
INITIAL_VY = -v0 * math.sin(ANGLE_RAD)

# Position initiale de la balle
ball_x = 50
ball_y = 500

# Boucle principale
while True:
    WIN.fill(WHITE)

    # Dessiner la balle
    pygame.draw.circle(WIN, BALL_COLOR, (round(ball_x), round(ball_y)), BALL_RADIUS)

    # Mise à jour de la position de la balle
    ball_x += INITIAL_VX * TIME_INTERVAL
    ball_y += (INITIAL_VY * TIME_INTERVAL) + (0.5 * GRAVITY * TIME_INTERVAL**2)

    # Vérifier si la balle touche le sol
    if ball_y >= HEIGHT//2 - BALL_RADIUS:
        ball_y = HEIGHT//2 - BALL_RADIUS
        INITIAL_VY = -INITIAL_VY * 0.9  # Perte d'énergie lors du rebond

    # Mise à jour de l'accélération verticale
    INITIAL_VY += GRAVITY * TIME_INTERVAL


    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mettre à jour l'affichage
    pygame.display.update()
    pygame.time.Clock().tick(60)




