import math

import pygame.event
from pygame.key import key_code

import unit

SPEED = 0
ANGULAR_SPEED = 0#单位为度

SWITCH_MENU = 10


def control_init(speed:int, angular_speed:float):
    global SPEED, ANGULAR_SPEED
    SPEED = speed
    ANGULAR_SPEED = angular_speed

class PlayerControl:
    def __init__(self, up:int, down:int, right:int, light:int, fire:int, tank:unit.Tank):
        self.key_up = up
        self.key_down = down
        self.key_right = right
        self.key_light = light
        self.key_fire = fire
        self.key_tank = tank
        player_controllers.append(self)
        pass

    def remove(self):
        player_controllers.remove(self)

    def click(self, key):
        if key[self.key_up]:
            self.tank_up()
        if key[self.key_down]:
            self.tank_down()
        if key[self.key_right]:
            self.tank_right()
        if key[self.key_light]:
            self.tank_light()
        if key[self.key_fire]:
            self.tank_fire()
        pass

    def tank_up(self):
        radian = math.radians(self.key_tank.angle)
        self.key_tank.move(math.cos(radian) * SPEED, -math.sin(radian) * SPEED)

    def tank_down(self):
        radian = math.radians(self.key_tank.angle)
        self.key_tank.move(-math.cos(radian) * SPEED, math.sin(radian) * SPEED)

    def tank_right(self):
        self.key_tank.rotate(-ANGULAR_SPEED)

    def tank_light(self):
        self.key_tank.rotate(ANGULAR_SPEED)

    def tank_fire(self):
        self.key_tank.fire()

class MainControl:
    def __init__(self, menu:int):
        self.key_menu = menu

    def click(self, event:pygame.event.Event) -> int:
        if event.type != pygame.KEYDOWN:
            return False
        key = pygame.key.get_pressed()
        match key:
            case self.key_menu:
                return SWITCH_MENU

player_controllers:list[PlayerControl] = []

def player_click():
    key = pygame.key.get_pressed()
    for p in player_controllers:
        p.click(key)
