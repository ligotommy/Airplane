import pygame
import sys
from airplane_classes import Airplane, Joystick

ESCAPE_KEY = 27
ARROW_UP_KEY = 1073741906
ARROW_LEFT_KEY = 1073741904
ARROW_DOWN_KEY = 1073741905
ARROW_RIGHT_KEY = 1073741903


pygame.init()
WINDOW_SIZE = pygame.display.Info().current_w, 500  # pygame.display.Info().current_h
surface = pygame.display.set_mode(WINDOW_SIZE)
airplane = Airplane([WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2], [0, 0], 1000, 1000, 300)
joystick = Joystick(pygame.Vector2(100, surface.get_height()-100), 50, 20)
background_color = 100, 130, 200

clock = pygame.time.Clock()

holding_up = False
holding_down = False
holding_right = False
holding_left = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            event_key = event.dict["key"]
            if event_key == ESCAPE_KEY:
                pygame.quit()
                sys.exit()
            if event_key == ARROW_UP_KEY:
                holding_up = True
            if event_key == ARROW_DOWN_KEY:
                holding_down = True
            if event_key == ARROW_RIGHT_KEY:
                holding_right = True
            if event_key == ARROW_LEFT_KEY:
                holding_left = True
        if event.type == pygame.KEYUP:
            event_key = event.dict["key"]
            if event_key == ARROW_UP_KEY:
                holding_up = False
            if event_key == ARROW_DOWN_KEY:
                holding_down = False
            if event_key == ARROW_RIGHT_KEY:
                holding_right = False
            if event_key == ARROW_LEFT_KEY:
                holding_left = False
        if (event.type == pygame.MOUSEBUTTONDOWN or
                event.type == pygame.MOUSEBUTTONUP or
                event.type == pygame.MOUSEMOTION):
            joystick.update(event)
    surface.fill(background_color)

    dtime = clock.tick()/1000
    # direction = pygame.Vector2(holding_right-holding_left, holding_up-holding_down)
    direction = joystick.get_vector()
    airplane.update_pos(direction, dtime)
    airplane.draw(surface, dtime)
    joystick.draw(surface)
    pygame.display.update()
