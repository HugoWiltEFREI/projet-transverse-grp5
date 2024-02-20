import pygame

pygame.init()

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

clock = pygame.time.Clock()

GRAY = pygame.Color('gray12')

display_width, display_height = display.get_size()

x = display_width * 0.45
y = display_height * 0.8

x_change = 0
y_change = 0
accel_x = 0
accel_y = 0
max_speed = 4

crashed = False
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
            crashed = True

    # handle left and right movement
    if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        x_change = max(x_change-0.2, -max_speed)
    elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
        x_change = min(x_change+0.2, max_speed)
    else:
        x_change *= 0.98

    # handle up and down movement
    if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        y_change = max(y_change-0.2, -max_speed)

    else:
        y_change *= 0.98

    x += x_change  # Move the object.
    y += y_change

    display.fill(GRAY)
    pygame.draw.rect(display, (0, 120, 250), (x, y, 20, 40))

    pygame.display.update()
    clock.tick(60)