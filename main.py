import pygame.mixer
from pygame.locals import *

from functions import *
from menu import menu

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Game')
game_font = pygame.font.Font("VT323-Regular.ttf", int(100))
text = game_font.render("PRESS E", False, "brown")
# For the pygame.transform.flip(player_img, 1, 0)
liste_music = ["musics/Rick Astley - Never Gonna Give You Up (Official Music Video).wav", "musics/Undertale_Chill.wav",
               "musics/Rick Astley - Never Gonna Give You Up (Official Music Video).wav", "musics/Undertale_Chill.wav"]

grassimage = pygame.image.load("textures/grassMid.png")
grasscenter = pygame.image.load("textures/grassCenter.png")
bow = pygame.image.load("textures/bow.png")
bluegrass = pygame.image.load("textures/grassCenterBlue.png")
bluegrassMid = pygame.image.load("textures/grassMiddleBlue.png")
darkBlock = pygame.image.load("textures/texture mario underground.png")
portal_entrance = pygame.image.load("textures/entrance_portal.png")
portal_exit = pygame.image.load("textures/exit_portal.png")

tl = {"o": grassimage, "x": grasscenter, "l": bluegrass, "b": bluegrassMid, 'd': darkBlock, 'e': portal_entrance,
      's': portal_exit}
game_font2 = pygame.font.Font("VT323-Regular.ttf", int(150))
text2 = game_font2.render("PRESS R TO RESTART", False, "brown")

player_img = pygame.image.load('textures/perso.png')
player_img = pygame.transform.scale_by(player_img, 0.04)
player_img.set_colorkey((255, 255, 255))

now = 0
level = 1
derniereaction = 0


def event_manager():
    global is_running, x, y
    for event in pygame.event.get():
        if event.type == QUIT:
            is_running = False

        if (event.type == KEYDOWN) and (statut == 1) and (model.affichage != 0):
            if event.key == K_e:
                model.zone_de_text = "Bow acquired"
                model.affichage = 0

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            print(x, y)

        is_dead(event)

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                is_running = False
            if event.key == K_c:
                print(player_rect.x, player_rect.y)
            if event.key == K_n:
                forward_lvl()
                pygame.mixer.music.load(liste_music[model.level - 1])
                pygame.mixer.music.play()
            if event.key == K_RIGHT or event.key == K_d:
                model.moving_right = True
                model.stay_right = True
            if event.key == K_LEFT or event.key == K_q:
                model.moving_left = True
                model.stay_right = False
            if event.key == K_SPACE or event.key == K_UP or event.key == K_z:
                if 0 in model.falling:
                    model.momentumY = 10
                    model.falling.pop(0)
                    model.falling.append(1)
        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_d:
                model.moving_right = False
            if event.key == K_LEFT or event.key == K_q:
                model.moving_left = False


def game():
    global y, x, player_rect, statut
    display.fill((146, 244, 255))
    if player_rect.x > 950:
        scroll[0] = player_rect.x - 950
    if player_rect.y < 150:
        scroll[1] = player_rect.y - 540
    # Affichage des blocks
    tile_rects = []
    y = 0
    for line_of_symbols in select_map(model.level):
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
    spike_level(model.level)
    # MOVEMENT OF THE PLAYER
    player_movement = [0, 0]
    if model.moving_right:
        player_movement[0] += 6 * model.player_velocity_multi
    if model.moving_left:
        player_movement[0] -= 6 * model.player_velocity_multi
    player_movement[1] -= model.momentumY
    if model.falling[-1]:
        model.momentumY -= 0.3 * model.player_velocity_multi
    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if collisions['bottom']:
        model.momentumY = 0
        model.falling.append(0)
        model.falling.pop(0)
    else:
        model.falling.append(1)
        model.falling.pop(0)
    if collisions["top"]:
        model.momentumY *= -1
    # Flip the player image when goes to the left
    if model.player_velocity_multi == 1:
        if model.stay_right:
            display.blit(
                player_img, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
        else:
            display.blit(
                pygame.transform.flip(player_img, True, False),
                (player_rect.x - scroll[0], player_rect.y - scroll[1]))
    statut = isinzone(450, player_rect.x, 515, 455, player_rect.y, 515)
    if statut and model.affichage == 1:
        display.blit(text, (800, 875))

    if model.level == 1:
        isinspike1 = isinzone(725, player_rect.x, 790, 490, player_rect.y + 30, 510)
        isinspike2 = isinzone(960, player_rect.x, 1025, 490, player_rect.y + 30, 510)
    elif model.level == 2:
        isinspike1 = isinzone(850 + 200, player_rect.x, 915 + 200, 490, player_rect.y + 30, 510)
        isinspike2 = isinzone(1085 + 200, player_rect.x, 1150 + 200, 490, player_rect.y + 30, 510)
    else:
        isinspike1 = False
        isinspike2 = False

    if isinspike1 or isinspike2:
        if model.now - model.derniereaction > 2000:
            model.number_of_life -= 1
            model.derniereaction = model.now

    model.now = pygame.time.get_ticks()
    cpteur = game_font.render(str(model.zone_de_text), False, "brown")
    diedFromVoid(player_rect.y)
    event_manager()
    screen.blit(pygame.transform.scale(display, (1920, 1080)), (0, 0))
    screen.blit(cpteur, (30, 30))
    if model.affichage != 0:
        screen.blit(bow, (465 - scroll[0], 465 - scroll[1]))
    if model.display_dead != 0:
        screen.blit(text2, (400, 100))
    life_left()
    pygame.display.update()
    clock.tick(60)


pygame.mixer.music.load(liste_music[model.level - 1])
pygame.mixer.music.play()

is_running = True

while is_running:
    if model.show_menu == 1:
        menu()
    else:
        game()