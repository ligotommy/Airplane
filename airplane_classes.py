import math
import pygame
import pygame.gfxdraw
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

    def update_pos(self, direction, dtime):
        angle = math.atan2(direction[1], direction[0])
        if not any(direction):
            new_tilt_dir = 0
        elif 3*math.pi/4 <= angle <= math.pi or -math.pi <= angle < -math.pi/4:
            new_tilt_dir = -1
        else:
            new_tilt_dir = 1
        if self.tilt_dir != new_tilt_dir:
            self.tilt_time = time.time()
            self.tilt_dir = new_tilt_dir

        acc_direction = direction
        if self.velo[0] > 0 and acc_direction[0] == 0:
            self.velo[0] += -10 * self.acceleration * dtime
            self.velo[0] = max(0, self.velo[0])
        elif self.velo[0] < 0 and acc_direction[0] == 0:
            self.velo[0] += 10 * self.acceleration * dtime
            self.velo[0] = min(0, self.velo[0])
        else:
            self.velo[0] += 10 * math.copysign(1, acc_direction[0]) * self.acceleration * dtime

        if self.velo[1] > 0 and acc_direction[1] == 0:
            self.velo[1] += -10 * self.acceleration
            self.velo[1] = max(0, self.velo[1])
        elif self.velo[1] < 0 and acc_direction[1] == 0:
            self.velo[1] += 10 * self.acceleration * dtime
            self.velo[1] = min(0, self.velo[1])
        else:
            self.velo[1] += 10 * math.copysign(1, acc_direction[1]) * self.acceleration * dtime

        self.velo[0] = min(self.max_velocity*abs(acc_direction[0]), self.velo[0])
        self.velo[0] = max(-self.max_velocity*abs(acc_direction[0]), self.velo[0])
        self.velo[1] = min(self.max_velocity*abs(acc_direction[1]), self.velo[1])
        self.velo[1] = max(-self.max_velocity*abs(acc_direction[1]), self.velo[1])

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


class Joystick:
    def __init__(self, center: pygame.Vector2, radius: int, small_circle_radius: int,
                 circle_color=(50, 50, 50, 150), small_circle_color=(0, 0, 0)):
        self.center = center
        self.radius = radius
        self.small_circle_radius = small_circle_radius
        self.small_circle_center = pygame.Vector2(0, 0)
        self.circle_color = circle_color
        self.small_circle_color = small_circle_color

        self.is_held = False

    def update(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            cursor_position = pygame.Vector2(event.dict["pos"])
            max_distance = self.radius - self.small_circle_radius
            distance = cursor_position.distance_to(self.center)
            if distance < max_distance:
                self.small_circle_center = cursor_position - self.center
                self.is_held = True
            elif distance < 1.3*self.radius:
                self.small_circle_center = (cursor_position - self.center).normalize()*max_distance
                self.is_held = True
        if event.type == pygame.MOUSEMOTION:
            cursor_position = pygame.Vector2(event.dict["pos"])
            max_distance = self.radius - self.small_circle_radius
            distance = cursor_position.distance_to(self.center)
            if self.is_held:
                if distance < max_distance:
                    self.small_circle_center = cursor_position - self.center
                    self.is_held = True
                else:
                    self.small_circle_center = (cursor_position - self.center).normalize()*max_distance
                    self.is_held = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.is_held = False
            self.small_circle_center = pygame.Vector2(0, 0)

    def get_vector(self) -> pygame.Vector2:
        return (pygame.Vector2(self.small_circle_center.x, -self.small_circle_center.y) /
                (self.radius-self.small_circle_radius))

    def draw(self, surface: pygame.Surface):
        alpha_surface = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)

        # pygame.draw.circle(alpha_surface, self.circle_color, self.center, self.radius)
        # pygame.draw.circle(alpha_surface, self.small_circle_color,
        #                    self.small_circle_center+self.center, self.small_circle_radius)
        pygame.gfxdraw.aacircle(alpha_surface, int(self.center.x), int(self.center.y), self.radius, self.circle_color)
        pygame.gfxdraw.filled_circle(alpha_surface,  int(self.center.x), int(self.center.y), self.radius, self.circle_color)
        small_circle_position = self.center + self.small_circle_center
        pygame.gfxdraw.aacircle(alpha_surface,  int(small_circle_position.x), int(small_circle_position.y),
                                self.small_circle_radius, self.small_circle_color)
        pygame.gfxdraw.filled_circle(alpha_surface, int(small_circle_position.x), int(small_circle_position.y),
                                     self.small_circle_radius, self.small_circle_color)

        surface.blit(alpha_surface, (0, 0))
