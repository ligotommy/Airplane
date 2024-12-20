import pygame
import sys
from airplane_classes import Airplane, Joystick

ESCAPE_KEY = 27
ARROW_UP_KEY = 1073741906
ARROW_LEFT_KEY = 1073741904
ARROW_DOWN_KEY = 1073741905
ARROW_RIGHT_KEY = 1073741903

ASPECT_RATIO = 20/10


pygame.init()
WINDOW_SIZE = pygame.display.Info().current_w, pygame.display.Info().current_h
rotate_window = WINDOW_SIZE[0] < WINDOW_SIZE[1]
size = WINDOW_SIZE if not rotate_window else WINDOW_SIZE[::-1]
if size[0] > size[1]*ASPECT_RATIO:
    unit = size[1]
    offset = (size[0] - size[1]*ASPECT_RATIO)/2
    surf_pos = (0, offset) if rotate_window else (offset, 0)
else:
    unit = size[0]/ASPECT_RATIO
    offset = (size[1] - size[0]/ASPECT_RATIO)/2
    surf_pos = (offset, 0) if rotate_window else (0, offset)
window_surface = pygame.display.set_mode(WINDOW_SIZE)
surface = pygame.Surface((unit*ASPECT_RATIO, unit))

airplane = Airplane([surface.get_width()/2, surface.get_height()/2], [0, 0], unit, unit, unit*3/10)
joystick = Joystick(pygame.Vector2(unit/5, surface.get_height()-unit/5), int(unit/10), int(unit/50))
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
            if rotate_window:
                event.dict["pos"] = [event.dict["pos"][1]-surf_pos[1],
                                     window_surface.get_width()-surf_pos[0]-event.dict["pos"][0]]
            else:
                event.dict["pos"] = [event.dict["pos"][0]-surf_pos[0],
                                     event.dict["pos"][1]-surf_pos[1]]
            joystick.update(event)
    surface.fill(background_color)

    dtime = clock.tick()/1000
    # direction = pygame.Vector2(holding_right-holding_left, holding_up-holding_down)
    direction = joystick.get_vector()
    airplane.update_pos(direction, dtime)
    airplane.draw(surface, dtime)
    joystick.draw(surface)
    surf = surface if not rotate_window else pygame.transform.rotate(surface, -90)
    window_surface.blit(surf, surf_pos)
    pygame.display.update()
