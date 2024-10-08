from random import random

import pygame

import controller
import unit


def player0_preset_create(surface:pygame.Surface) -> (unit.Tank, controller.PlayerControl):
    player = None
    is_crash = True
    while is_crash:
        player = unit.Tank(int(random() * surface.get_width()), int(random() * surface.get_height())
                           , 0, unit.RED_PATH)
        if  pygame.sprite.spritecollide(player, unit.wall_group, False, None):
            unit.tanks_group.remove(player)
        else:
            is_crash = False
    player_control = controller.PlayerControl(
        pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_SPACE, player)
    return player, player_control

def player1_preset_create(surface:pygame.Surface) -> (unit.Tank, controller.PlayerControl):
    player = None
    is_crash = True
    while is_crash:
        player = unit.Tank(int(random() * surface.get_width()), int(random() * surface.get_height())
                           , 1, unit.BLUE_PATH)
        if  pygame.sprite.spritecollide(player, unit.wall_group, False, None):
            unit.tanks_group.remove(player)
        else:
            is_crash = False
    player_control = controller.PlayerControl(
    pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_e, player)
    return player, player_control
