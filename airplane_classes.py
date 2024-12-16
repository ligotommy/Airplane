import pygame

AIRPLANE_FILE = "airplane.png"


class Airplane:
    def __init__(self, pos, velo, acceleration, max_velocity, width, max_tilt=25, flipped=False):
        self.pos = pos
        self.velo = velo
        self.acceleration = acceleration
        self.max_velocity = max_velocity
        self.size = (width, 0)
        self.tilt = 0
        self.max_tilt = max_tilt
        self.flipped = flipped
        self.image = None
        self.original_image = None

    def update_pos(self, acc_direction, dtime):
        if self.velo[0] > 0 and acc_direction[0] == 0:
            self.velo[0] += -10 * self.acceleration * dtime/1000
            self.velo[0] = max(0, self.velo[0])
        if self.velo[0] < 0 and acc_direction[0] == 0:
            self.velo[0] += 10 * self.acceleration * dtime/1000
            self.velo[0] = min(0, self.velo[0])
        else:
            self.velo[0] += 10 * acc_direction[0] * self.acceleration * dtime/1000

        if self.velo[1] > 0 and acc_direction[1] == 0:
            self.velo[1] += -10 * self.acceleration * dtime / 1000
            self.velo[1] = max(0, self.velo[1])
        if self.velo[1] < 0 and acc_direction[1] == 0:
            self.velo[1] += 10 * self.acceleration * dtime / 1000
            self.velo[1] = min(0, self.velo[1])
        else:
            self.velo[1] += 10 * acc_direction[1] * self.acceleration * dtime/1000

        self.velo[0] = min(self.max_velocity, self.velo[0])
        self.velo[0] = max(-self.max_velocity, self.velo[0])
        self.velo[1] = min(self.max_velocity, self.velo[1])
        self.velo[1] = max(-self.max_velocity, self.velo[1])

        self.pos[0] += self.velo[0] * dtime/1000
        self.pos[1] += self.velo[1] * dtime/1000

    def load_image(self):
        self.image = pygame.image.load(AIRPLANE_FILE)
        self.size = self.size[0], self.image.get_height()/(self.image.get_width() / self.size[0])
        self.image = pygame.transform.smoothscale(self.image, self.size)
        self.original_image = self.image.copy()

    def draw(self, surface: pygame.Surface, tilt):
        if not self.image:
            self.load_image()
        if tilt*self.tilt != self.max_tilt and tilt != 0:
            self.tilt = -self.max_tilt*tilt
            self.image = pygame.transform.rotate(self.original_image, self.tilt)
        elif self.tilt != 0 and tilt == 0:
            self.tilt = 0
            self.image = self.original_image
        pos = self.pos[0] - self.size[0] / 2, surface.get_height() - self.pos[1] - self.size[1] / 2
        surface.blit(self.image, pos)
