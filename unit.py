import math
import os.path
from typing import Tuple, Callable
import pygame


SURFACE:pygame.Surface
RES_PATH = "res"
GREEN_PATH = os.path.join(RES_PATH, "tank3.png")
RED_PATH = os.path.join(RES_PATH, "tank1.png")
BLUE_PATH = os.path.join(RES_PATH, "tank2.png")

FRAME_RATE = 60
FRAME_COUNTER = 0

def unit_init(frame_rate, surface):
    global SURFACE, FRAME_RATE
    FRAME_RATE = frame_rate
    SURFACE = surface
    pass

def frame_counter_update():
    global FRAME_COUNTER
    FRAME_COUNTER += 1
pass

class Wall(pygame.sprite.Sprite):
    thickness: int
    length: int
    angle: float #默认水平
    def __init__(self, centerx:int, centery:int, thick: int, length: int, angle = 0):
        super().__init__()
        self.thickness = thick
        self.length = length
        self.angle = angle
        self.image = pygame.transform.rotate(pygame.Surface((length, thick)), angle)
        self.rect = self.image.get_rect(center = (centerx, centery))
        self.add(wall_group)
        pass
    pass

wall_group = pygame.sprite.Group()

class Cannonball(pygame.sprite.Sprite):
    distance: int
    speed: int
    angle: float
    max_distance: int

    def __init__(self, centerx:int, centery:int, angle:float, player_ser:int, speed = 5, max_distance = 225):
        super().__init__()
        radius = 4
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 0), (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.distance = 0
        self.angle = angle
        self.speed = speed
        self.max_distance = max_distance
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.player_ser = player_ser
        self.add(cannonball_group)
        pass

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if self.rect.centerx < 0:
            self.rect.centerx = SURFACE.get_width()
        elif self.rect.centerx > SURFACE.get_width():
            self.rect.centerx = 0
        if self.rect.centery < 0:
            self.rect.centery = SURFACE.get_height()
        elif self.rect.centery > SURFACE.get_height():
            self.rect.centery = 0
        pass

    def update(self):
        if self.distance >= self.max_distance:
            cannonball_group.remove(self)
            return
        hit(self)
        radian = math.radians(self.angle)
        self.move(self.speed * math.cos(radian), -self.speed * math.sin(radian))
        for wall in wall_group.sprites():
            cannonball_crash(self, wall)
        self.distance += self.speed
        pass
    pass

cannonball_group = pygame.sprite.Group()

def cannonball_crash(ball: Cannonball, wall: Wall):
    if pygame.sprite.collide_rect(ball, wall):
        ball.angle = -(ball.angle - wall.angle) + wall.angle
    pass

class TankBox(pygame.sprite.Sprite):
    def __init__(self, centerx:int, centery:int, angle:float):
        super().__init__()
        self.angle = angle
        self.original_image = pygame.Surface((25, 19), pygame.SRCALPHA)
        self.original_image.fill((255, 0, 0))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(centerx, centery))
        self.add(box_group)
        pass

    def relocate(self, centerx:int, centery:int, angle:float):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        pass

    def move_to(self, centerx, centery):
        self.rect.center = (centerx, centery)
        pass

    def try_move_to(self, centerx, centery) -> bool:
        old_center = self.rect.center
        self.rect.center = (centerx, centery)
        if pygame.sprite.spritecollide(self, wall_group, False):
            self.rect.center = old_center
            return False
        return True
    pass

box_group = pygame.sprite.Group()

class Tank(pygame.sprite.Sprite):
    center: [float, float]
    skewing: Tuple[int, int] #图像中心相对于单位中心的偏移
    live: bool
    last_fire: int
    ser_num: int

    def __init__(self, x:int, y:int, ser_num, image_path:str):
        super().__init__()
        self.live = True
        self.last_fire = FRAME_COUNTER
        self.image = pygame.image.load(image_path).convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.center = (self.rect.centerx - 2, self.rect.centery)
        self.angle = 0
        self.skewing = (2, 0)
        self.box = TankBox(x, y, self.angle)
        self.ser_num = ser_num
        self.add(tanks_group)
        pass

    def relocate(self):
        radian = math.radians(self.angle)
        self.rect.center = (self.center[0] + self.skewing[0] * math.cos(radian) - self.skewing[1] * math.sin(radian),
                            self.center[1] - self.skewing[0] * math.sin(radian) + self.skewing[1] * math.cos(radian))
        pass

    def move(self, x:float, y:float):
        old_center = self.center
        width = SURFACE.get_width()
        height = SURFACE.get_height()
        self.center = [self.center[0]+x, self.center[1]+y]
        if self.center[0] > width:
            self.center[0] = 0
        elif self.center[0] < 0:
            self.center[0] = width
        if self.center[1] > height:
            self.center[1] = 0
        elif self.center[1] < 0:
            self.center[1] = height
        if not self.box.try_move_to(self.center[0], old_center[1]):
            self.center[0] = old_center[0]
        if not self.box.try_move_to(self.center[0], self.center[1]):
            self.center[1] = old_center[1]
        self.relocate()
        pass

    def rotate(self, angle:float):
        self.angle += angle
        if self.angle < 0:
            self.angle %= -360
        else:
            self.angle %= 360
        if self.angle > 180:
            self.angle -= 360
        elif self.angle < -180:
            self.angle += 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.relocate()
        self.box.relocate(self.center[0], self.center[1], self.angle)
        pass

    def fire(self):
        if not self.live or FRAME_COUNTER - self.last_fire < FRAME_RATE/6:
            return
        radian = math.radians(self.angle)
        Cannonball(self.center[0] + 20 * math.cos(radian), self.center[1] - 20 * math.sin(radian),
                   self.angle, self.ser_num, max_distance = SURFACE.get_width())
        self.last_fire = FRAME_COUNTER
    pass

tanks_group = pygame.sprite.Group()
hit_func: list[Callable[[Tank, Cannonball], None]] = []

def hit(ball: Cannonball):
    for tank in tanks_group.sprites():
        if pygame.sprite.collide_mask(tank.box, ball):
            tank.live = False
            tanks_group.remove(tank)
            cannonball_group.remove(ball)
            for func in hit_func:
                func(tank, ball)
    pass
