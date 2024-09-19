from random import random

import pygame.sprite

import unit

WID_GROWTH = 0
HEI_GROWTH = 0
MAZE_LIST:list[list[int]] = []#对于墙，"0"表封闭，"1"表打通
INIT = False
GENERATED = False
SURFACE:pygame.Surface

def maze_init(surface:pygame.Surface , wid_growth:int, hei_growth:int):
    global INIT, SURFACE, WID_GROWTH, HEI_GROWTH
    for i in range(wid_growth * 2 - 1):
        MAZE_LIST.append([0] * (hei_growth * 2 - 1))
    INIT = True
    SURFACE = surface
    WID_GROWTH = wid_growth
    HEI_GROWTH = hei_growth

def generate():
    queue = [(0, 0)]
    old = [(0, 0)]
    nx = (0, 2, 0, -2)
    ny = (2, 0, -2, 0)

    while len(queue) > 0:
        cur = queue[int(random() * len(queue))]
        ind = int(random() * 4)
        # noinspection DuplicatedCode
        tmp = (cur[0] + nx[ind], cur[1] + ny[ind])
        if tmp[0] < 0 or tmp[0] >= len(MAZE_LIST) or tmp[1] < 0 or tmp[1] >= len(MAZE_LIST[0]):
            continue
        if tmp not in old:
            MAZE_LIST[int((cur[0] + tmp[0]) / 2)][int((cur[1] + tmp[1]) / 2)] = 1
            queue.append(tmp)
            old.append(tmp)
        finish = True
        for i in range(4):
            # noinspection DuplicatedCode
            tmp = (cur[0] + nx[i], cur[1] + ny[i])
            if tmp[0] < 0 or tmp[0] >= len(MAZE_LIST) or tmp[1] < 0 or tmp[1] >= len(MAZE_LIST[0]):
                continue
            if tmp not in old:
                finish = False
                break
        if finish:
            queue.remove(cur)

def build():
    width = SURFACE.get_width()
    height = SURFACE.get_height()
    thick = 10
    level_length = int(width / WID_GROWTH)
    vertical_length = int(height / HEI_GROWTH)
    for i in range(WID_GROWTH):
        for j in range(HEI_GROWTH - 1):
            if MAZE_LIST[2 * i][2 * j + 1] == 0:
                unit.Wall(level_length * i + int(level_length / 2),
                          vertical_length * (j + 1),
                          thick, level_length + thick, 0)
    for i in range(WID_GROWTH - 1):
        for j in range(HEI_GROWTH):
            if MAZE_LIST[2 * i + 1][2 * j] == 0:
                unit.Wall(level_length * (i + 1),
                          vertical_length * j + int(vertical_length / 2),
                          thick, vertical_length + thick, 90)


