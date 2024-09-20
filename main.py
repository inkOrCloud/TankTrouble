import pygame

import controller
import maze
import ui
import unit
from controller import control_init
from players import player0_preset_create, player1_preset_create

WIDTH = 1280
HEIGHT = 720
FRAME_RATE = 60

WHITE = (255, 255, 255)

SCREEN:pygame.Surface
CLOCK:pygame.time.Clock

RUNNING = True
GAMING = True

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Tank Trouble")
    global SCREEN, CLOCK
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    ui.ui_init(WIDTH, HEIGHT)

    main_ui = ui.main_ui()
    SCREEN.blit(main_ui, (0, 0))
    pygame.display.flip()
    global RUNNING, GAMING
    while RUNNING:
        CLOCK.tick(25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN and ui.is_click(event, main_ui.get_rect(), ui.END_BUTTON):
                RUNNING = False
            elif event.type == pygame.MOUSEBUTTONDOWN and ui.is_click(event, main_ui.get_rect(), ui.START_BUTTON):
                GAMING = True
                gaming()
                SCREEN.blit(main_ui, (0, 0))
                pygame.display.flip()

def menu():
    menu_ui = ui.menu_ui()
    menu_rect = menu_ui.get_rect(center = (WIDTH/2, HEIGHT/2))
    SCREEN.blit(menu_ui, menu_rect)
    pygame.display.update()
    running = True
    while running:
        CLOCK.tick(25)
        global GAMING, RUNNING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                GAMING = False
                RUNNING = False
            elif event.type == pygame.MOUSEBUTTONDOWN and ui.is_click(event, menu_rect, ui.CONTINUE_BUTTON):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and ui.is_click(event, menu_rect, ui.EXIT_BUTTON):
                running = False
                GAMING = False

def gaming():
    gaming_map = pygame.Surface((WIDTH * 2 / 3, HEIGHT))
    gaming_map.fill(WHITE)
    unit.unit_init(FRAME_RATE, gaming_map)
    control_init(3, 5)
    maze.maze_init(gaming_map, 5, 5)
    maze.generate()
    maze.build()
    score = ui.ScoringBoard(int(WIDTH / 3), HEIGHT, 2)
    player0, player0_control = player0_preset_create(gaming_map)
    player1, player1_control = player1_preset_create(gaming_map)
    def score_count(tank: unit.Tank, ball: unit.Cannonball):
        if tank.ser_num == ball.player_ser:
            score.score_down(tank.ser_num)
        else:
            score.score_up(ball.player_ser)
            score.score_down(tank.ser_num)
    def resurgence(tank: unit.Tank, ball: unit.Cannonball):
        match tank.ser_num:
            case 0:
                nonlocal player0, player0_control
                player0_control.remove()
                player0, player0_control = player0_preset_create(gaming_map)

            case 1:
                nonlocal player1, player1_control
                player1_control.remove()
                player1, player1_control = player1_preset_create(gaming_map)
    unit.hit_func.append(score_count)
    unit.hit_func.append(resurgence)
    global GAMING, RUNNING
    while GAMING:
        CLOCK.tick(FRAME_RATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAMING = False
                RUNNING = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu()
        controller.player_click()
        unit.cannonball_group.update()
        gaming_map.fill(WHITE)
        unit.cannonball_group.draw(gaming_map)
        unit.tanks_group.draw(gaming_map)
        unit.wall_group.draw(gaming_map)
        unit.frame_counter_update()
        SCREEN.blit(gaming_map, (0, 0))
        SCREEN.blit(score.surface, (gaming_map.get_width(), 0))
        pygame.display.update()


main()






