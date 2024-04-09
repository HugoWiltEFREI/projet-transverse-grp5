import pygame
import pygame_gui

import model
from functions import screen


def settings():
    game_font = pygame.font.Font("VT323-Regular.ttf", int(100))
    text_font = pygame.font.Font("VT323-Regular.ttf", int(75))
    volume_font = pygame.font.Font("VT323-Regular.ttf", int(25))
    background = pygame.image.load("textures/Menu-transformed.jpeg")
    background = pygame.transform.scale_by(background, 0.63)

    manager = pygame_gui.UIManager((int(1800), int(1800)), "other/settings.json")

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
                        model.number_of_life = 5
                    elif event.text == "Test2":
                        scalar = 0.7

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
    background = pygame.image.load("textures/Menu-transformed.jpeg")
    background = pygame.transform.scale_by(background, 0.63)
    manager = pygame_gui.UIManager((int(1800), int(1800)), "other/package.json")
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
