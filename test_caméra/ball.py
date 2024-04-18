import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des constantes
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5
JUMP_HEIGHT = 10

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialisation de la fenêtre de jeu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mon jeu Pygame")

ball = pygame.image.load("balle.png")

# Position et vélocité du personnage
player_x = WIDTH // 2
player_y = HEIGHT - PLAYER_SIZE
player_velocity_x = 0
player_is_jumping = False


# Fonction pour dessiner le personnage
def draw_player():
    pygame.draw.rect(screen, WHITE, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))


# Fonction pour dessiner la balle
def draw_bullet(bullet_x, bullet_y,screen):
    screen.blit(ball, (bullet_x,bullet_y))

bullet_fired = False
bullet_x = 0
bullet_y = 0
bullet_velocity_y = 0

# Boucle de jeu principale
running = True
while running:
    screen.fill("turquoise")

    if bullet_fired:
        draw_bullet(bullet_x, bullet_y, screen)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_fired == False:
                # Tirer une balle
                bullet_x = player_x + PLAYER_SIZE // 2
                bullet_y = player_y - PLAYER_SIZE // 2
                bullet_velocity_y = 10 # Vitesse de la balle en y
                bullet_fired = True

    # Déplacement du personnage
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_velocity_x = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT]:
        player_velocity_x = PLAYER_SPEED
    else:
        player_velocity_x = 0

    player_x += player_velocity_x
    bullet_x += bullet_velocity_y

    # Dessiner le personnage
    draw_player()

    # Mise à jour de l'affichage
    pygame.display.flip()

    # Limiter la vitesse de la boucle
    pygame.time.Clock().tick(60)

# Quitter Pygame
pygame.quit()
sys.exit()
