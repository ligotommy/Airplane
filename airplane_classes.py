import math

import pygame
import time

AIRPLANE_FILE = "airplane.png"


class Airplane:
    def __init__(self, pos, velo, acceleration, max_velocity, width, tilt_speed=200, max_tilt=20, flipped=False):
        self.pos = pos
        self.velo = velo
        self.acceleration = acceleration
        self.max_velocity = max_velocity
        self.size = (width, 0)
        self.tilt_time = -5
        self.tilt_dir = 0
        self.tilt_deg = 0
        self.max_tilt = max_tilt
        self.tilt_speed = tilt_speed
        self.flipped = flipped
        self.image = None
        self.original_image = None

    def update_pos(self, up, down, left, right, dtime):
        forward = right if self.flipped else left
        backwards = left if self.flipped else right
        new_tilt_dir = backwards - forward
        if not new_tilt_dir:
            new_tilt_dir = up - down
        if self.tilt_dir != new_tilt_dir:
            self.tilt_time = time.time()
            self.tilt_dir = new_tilt_dir

        acc_direction = [right-left, up-down]
        if self.velo[0] > 0 and acc_direction[0] == 0:
            self.velo[0] += -10 * self.acceleration * dtime
            self.velo[0] = max(0, self.velo[0])
        if self.velo[0] < 0 and acc_direction[0] == 0:
            self.velo[0] += 10 * self.acceleration * dtime
            self.velo[0] = min(0, self.velo[0])
        else:
            self.velo[0] += 10 * acc_direction[0] * self.acceleration * dtime

        if self.velo[1] > 0 and acc_direction[1] == 0:
            self.velo[1] += -10 * self.acceleration
            self.velo[1] = max(0, self.velo[1])
        if self.velo[1] < 0 and acc_direction[1] == 0:
            self.velo[1] += 10 * self.acceleration * dtime
            self.velo[1] = min(0, self.velo[1])
        else:
            self.velo[1] += 10 * acc_direction[1] * self.acceleration * dtime

        self.velo[0] = min(self.max_velocity, self.velo[0])
        self.velo[0] = max(-self.max_velocity, self.velo[0])
        self.velo[1] = min(self.max_velocity, self.velo[1])
        self.velo[1] = max(-self.max_velocity, self.velo[1])

        self.pos[0] += self.velo[0] * dtime
        self.pos[1] += self.velo[1] * dtime

    def load_image(self):
        self.image = pygame.image.load(AIRPLANE_FILE)
        self.size = self.size[0], self.image.get_height()/(self.image.get_width() / self.size[0])
        self.image = pygame.transform.smoothscale(self.image, self.size)
        self.original_image = self.image.copy()

    def draw(self, surface: pygame.Surface, dtime):
        if self.image is None:
            self.load_image()
        if -self.tilt_dir*self.tilt_deg != self.max_tilt and self.tilt_dir != 0:
            self.tilt_deg += -self.tilt_dir * dtime * self.tilt_speed
            self.tilt_deg = min(self.max_tilt, self.tilt_deg)
            self.tilt_deg = max(-self.max_tilt, self.tilt_deg)
            self.image = pygame.transform.rotate(self.original_image, self.tilt_deg)
        elif self.tilt_deg != 0 and self.tilt_dir == 0:
            tilt_dir = int(math.copysign(1, self.tilt_deg))
            self.tilt_deg += -tilt_dir * dtime * self.tilt_speed
            self.tilt_deg = max(0, tilt_dir*self.tilt_deg)*tilt_dir
            self.image = pygame.transform.rotate(self.original_image, self.tilt_deg)
        pos = self.pos[0] - self.image.get_width() / 2, surface.get_height() - self.pos[1] - self.image.get_height() / 2
        surface.blit(self.image, pos)
