import pygame

class Enemie(pygame.sprite.Sprite):
    def __init__(self, x, y, taille):
        self.x = x
        self.y = y
        self.taille = taille
        self.rect = pygame.Rect(self.x, self.y, self.taille[0], self.taille[1])
        self.saut = 0
        self.saut_montee = 0
        self.saut_descente = 0
        self.nombre_de_saut = 0
        self.a_sauter = False
        self.a_attaquer = False
        self.tir_autorise = 2
        self.direction = 2
        self.enemie_vivant = [
            pygame.Rect(0,0,32,32),
            pygame.Rect(32, 0, 64, 32),   # a ajouter
            pygame.Rect(0, 0, 32, 32),
            pygame.Rect(64, 0, 96, 32),
        ]
        self.enemie_mort = [
            pygame.Rect(32,160,64,192),
            pygame.Rect(64, 160, 96, 192),# a ajouter

        ]
        self.enemie_attaque = [
            pygame.Rect(0, 32, 32, 64),  # a ajouter

        ]

def image_liste(self, image, dict):
    for imagedebout in self.enemie_attaque:

        image_rect = self.enemie_vivant.pop(0)
        image_joueur = image.subsurface(image_rect)
        image_joueur = pygame.transform.scale(image_joueur, (32,32))
        self.enemie_vivant.append(image_joueur)
    dict['vivant'] = self.enemie_vivant

    for image_attaque in self.enemie_attaque:
        rect_joueur = self.enemie_attaque.pop(0)
        image_joueur = image.subsurface(rect_joueur)
        image_joueur = pygame.transform.scale(image_joueur, (32,32))
        self.enemie_attaque.append(image_joueur)
    dict['attaque'] = self.enemie_attaque

    return dict
def afficher_image(self, surface, dict):
    self.index += 1
    if self.index == len(dict(self.etat)):
        self.index = 0
    if self.etat == 'attaque' and self.index == 4:
        self.index = 3

    image = dict[self.etat][self.index]

    if self.direction == -1:
        image = pygame.transform.flip(image, True, False)

    surface.blit(image, self.rect)
    pygame.draw.rect(surface, (255,0,0), self.rect, 1)


