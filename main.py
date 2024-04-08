import pygame_gui
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

music = pygame.mixer.Sound("Rick Astley - Never Gonna Give You Up (Official Music Video).wav")

grassimage = pygame.image.load("grassMid.png")
grasscenter = pygame.image.load("grassCenter.png")
bow = pygame.image.load("bow.png")
darkBlock = pygame.image.load("texture mario underground.png")

tl = {"o": grassimage, "x": grasscenter, 'd':darkBlock}
game_font2 = pygame.font.Font("VT323-Regular.ttf", int(150))
text2 = game_font2.render("PRESS R TO RESTART", False, "brown")

player_img = pygame.image.load('perso.png')
player_img = pygame.transform.scale_by(player_img, 0.04)
player_img.set_colorkey((255, 255, 255))

now = 0
level = 2
derniereaction = 0


def event_manager():
    global is_running, zone_de_text, affichage, x, y, moving_right, stay_right, moving_left, momentum, level
    for event in pygame.event.get():
        if event.type == QUIT:
            is_running = False

        if (event.type == KEYDOWN) and (statut == 1) and (affichage != 0):
            if event.key == K_e:
                zone_de_text = "Bow acquired"
                affichage = 0

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
                if level == 1:
                    level = 2
                else:
                    level = 1
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


def unnamed():
    global y, x, momentum, player_rect, air_timer, statut, derniereaction, now
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
        player_movement[0] += 6 * model.player_velocity_multi
    if moving_left:
        player_movement[0] -= 6 * model.player_velocity_multi
    player_movement[1] += momentum
    momentum += 0.3 * model.player_velocity_multi
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
    if model.player_velocity_multi == 1:
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

    if level == 1:
        isinspike1 = isinzone(725, player_rect.x, 790, 490, player_rect.y + 30, 510)
        isinspike2 = isinzone(960, player_rect.x, 1025, 490, player_rect.y + 30, 510)
    else:
        isinspike1 = isinzone(850 + 200, player_rect.x, 915 + 200, 490, player_rect.y + 30, 510)
        isinspike2 = isinzone(1085 + 200, player_rect.x, 1150 + 200, 490, player_rect.y + 30, 510)

    if isinspike1 or isinspike2:
        if now - derniereaction > 2000:
            model.number_of_life -= 1
            derniereaction = now

    now = pygame.time.get_ticks()
    cpteur = game_font.render(str(zone_de_text), False, "brown")
    diedFromVoid(player_rect.y)
    event_manager()
    screen.blit(pygame.transform.scale(display, (1920, 1080)), (0, 0))
    screen.blit(cpteur, (30, 30))
    if affichage != 0:
        screen.blit(bow, (465 - scroll[0], 465 - scroll[1]))
    if model.display_dead != 0:
        screen.blit(text2, (400, 100))
    life_left()
    pygame.display.update()
    clock.tick(60)


def settings():
    game_font = pygame.font.Font("VT323-Regular.ttf", int(100))
    text_font = pygame.font.Font("VT323-Regular.ttf", int(75))
    volume_font = pygame.font.Font("VT323-Regular.ttf", int(25))
    background = pygame.image.load("Menu-transformed.jpeg")
    background = pygame.transform.scale_by(background, 0.63)

    manager = pygame_gui.UIManager((int(1800), int(1800)), "settings.json")

    dropdown = pygame_gui.elements.UIDropDownMenu(["Test1", "Test2", "Test3"], "Test1",
                                                  pygame.Rect((715, 375), (900, 30)), manager)

    sound = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((715, 485), (900, 30)), 50, (0, 100), manager)
    music = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((715, 620), (900, 30)), 50, (0, 100), manager)

    settings_background1 = pygame.surface.Surface((415, 75))
    settings_background1.fill("#032058")
    settings_background2 = pygame.surface.Surface((350, 20))
    settings_background2.fill("#c0ffee")

    slider_background1 = pygame.surface.Surface((1315, 55))
    slider_background1.fill("#032058")
    slider_background2 = pygame.surface.Surface((1230, 20))
    slider_background2.fill("#c0ffee")

    text = game_font.render("SETTINGS :", False, "lightblue")
    text_resolution = text_font.render("RESOLUTION : ", False, "lightblue")
    text_sound = text_font.render("SOUND :", False, "lightblue")
    text_music = text_font.render("MUSIC :", False, "lightblue")
    text_back = pygame_gui.elements.UIButton(pygame.Rect((1440, 240), (150, 75)), "BACK>", manager)

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if pygame.mouse.get_pressed()[0] == True:
                x, y = pygame.mouse.get_pos()
                print(x, y)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == text_back:
                    is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False

            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == dropdown:
                    if event.text == "Test1":
                        scalar = 1
                    elif event.text == "Test2":
                        scalar = 0.73

            manager.process_events(event)

        manager.update(time_delta)
        value_sound = volume_font.render(str(sound.get_current_value()), False, "lightblue")
        value_music = volume_font.render(str(music.get_current_value()), False, "lightblue")

        screen.blit(background, (0, -80))

        screen.blit(settings_background2, (430, 310))
        screen.blit(settings_background1, (320, 240))

        screen.blit(slider_background2, (430, 410))
        screen.blit(slider_background1, (320, 360))

        screen.blit(slider_background2, (430, 520))
        screen.blit(slider_background1, (320, 470))

        screen.blit(slider_background2, (430, 655))
        screen.blit(slider_background1, (320, 605))

        screen.blit(value_sound, (600, 485))
        screen.blit(value_music, (600, 620))

        screen.blit(text, (335, 225))
        screen.blit(text_resolution, (335, 350))
        screen.blit(text_sound, (335, 460))
        screen.blit(text_music, (335, 595))
        manager.draw_ui(screen)

        pygame.display.update()
        val_music = float(music.get_current_value() / 100)
        pygame.mixer.music.set_volume(val_music)


def menu():
    background = pygame.image.load("Menu-transformed.jpeg")
    background = pygame.transform.scale_by(background, 0.63)
    manager = pygame_gui.UIManager((int(1800), int(1800)), "package.json")
    coffe_zone = pygame.surface.Surface((250, 25))
    coffe_zone.fill("#c0ffee")
    zone_for_play = pygame_gui.elements.UIButton(pygame.Rect((850, 300), (280, 75)), "PLAY", manager)
    zone_for_settings = pygame_gui.elements.UIButton(pygame.Rect((850, 450), (280, 75)), "SETTINGS", manager)
    zone_for_credits = pygame_gui.elements.UIButton(pygame.Rect((850, 600), (280, 75)), "CREDITS", manager)
    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == zone_for_play:
                is_running = False
                model.show_menu = 0

            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == zone_for_settings:
                settings()

            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == zone_for_credits:
                print("no")

            manager.process_events(event)

        if model.show_menu == 1:
            manager.update(time_delta)
            screen.blit(background, (0, -80))
            screen.blit(coffe_zone, (900, 360))
            screen.blit(coffe_zone, (900, 510))
            screen.blit(coffe_zone, (900, 660))
            manager.draw_ui(screen)

        pygame.display.update()


pygame.mixer.music.load('Rick Astley - Never Gonna Give You Up (Official Music Video).wav')
pygame.mixer.music.play(-1)

is_running = True

while is_running:
    if model.show_menu == 1:
        menu()
    else:
        unnamed()
