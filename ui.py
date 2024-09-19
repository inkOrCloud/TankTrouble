import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SILVER = (192, 192, 192)
DARKGRAY = (169, 169, 169)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WIDTH = 0
HEIGHT = 0

# 按钮的Rect
START_BUTTON: pygame.Rect
END_BUTTON: pygame.Rect
CONTINUE_BUTTON: pygame.Rect
EXIT_BUTTON: pygame.Rect

# ui的Rect
MENU_RECT: pygame.Rect


def ui_init(width: int, height: int):
    global WIDTH, HEIGHT
    WIDTH = width
    HEIGHT = height
    pass


def main_ui() -> pygame.Surface:
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(WHITE)
    button_size = (WIDTH / 6, HEIGHT / 6)
    start_center = (WIDTH / 2, HEIGHT / 2)
    end_center = (WIDTH / 2, 3 * HEIGHT / 4)

    title_font = pygame.font.Font(None, int(HEIGHT / 10))
    title_image = title_font.render("Tank Trouble", True, BLACK)
    title_rect = title_image.get_rect()
    start_surface = pygame.Surface(button_size, pygame.SRCALPHA)
    pygame.draw.rect(start_surface, BLACK, (0, 0) + button_size, 4)
    start_rect = start_surface.get_rect()
    button_text = pygame.font.Font(None, int(button_size[1] / 2))
    start_image = button_text.render("Start", True, BLACK)
    start_image_rect = start_image.get_rect()
    end_surface = pygame.Surface(button_size, pygame.SRCALPHA)
    pygame.draw.rect(end_surface, BLACK, (0, 0) + button_size, 4)
    end_rect = end_surface.get_rect()
    end_image = button_text.render("Exit", True, BLACK)
    end_image_rect = end_image.get_rect()
    title_rect.y = HEIGHT / 5
    title_rect.centerx = WIDTH / 2
    start_rect.center, start_image_rect.center = start_center, start_center
    end_rect.center, end_image_rect.center = end_center, end_center
    surface.blit(title_image, title_rect)
    surface.blit(start_surface, start_rect)
    surface.blit(end_surface, end_rect)
    surface.blit(start_image, start_image_rect)
    surface.blit(end_image, end_image_rect)
    global START_BUTTON, END_BUTTON
    START_BUTTON = start_rect
    END_BUTTON = end_rect
    return surface


def menu_ui() -> pygame.Surface:
    alpha = 128
    width, height = WIDTH / 5, HEIGHT / 3
    screen = pygame.Surface((width, height), pygame.SRCALPHA)
    button_size = (WIDTH / 8, HEIGHT / 10)
    continue_center = (width / 2, height / 3)
    end_center = (width / 2, height * 2 / 3)
    screen.fill(SILVER + (alpha,))
    button_font = pygame.font.Font(None, int(button_size[0] / 4))

    continue_surface = pygame.Surface(button_size, pygame.SRCALPHA)
    continue_surface.fill(DARKGRAY + (alpha,))
    continue_rect = continue_surface.get_rect()
    continue_rect.center = continue_center
    continue_text = button_font.render("Continue", True, WHITE)
    continue_text_rect = continue_text.get_rect()
    continue_text_rect.center = continue_center

    end_surface = pygame.Surface(button_size, pygame.SRCALPHA)
    end_surface.fill(DARKGRAY + (alpha,))
    end_rect = end_surface.get_rect()
    end_rect.center = end_center
    end_text = button_font.render("Exit", True, WHITE)
    end_text_rect = end_text.get_rect()
    end_text_rect.center = end_center

    global CONTINUE_BUTTON, EXIT_BUTTON
    CONTINUE_BUTTON = continue_rect
    EXIT_BUTTON = end_rect
    screen.blit(continue_surface, continue_rect)
    screen.blit(continue_text, continue_text_rect)
    screen.blit(end_surface, end_rect)
    screen.blit(end_text, end_text_rect)
    return screen


def is_click(event: pygame.event.Event, ui_rect: pygame.Rect, button: pygame.Rect) -> bool:
    if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
        return False
    button_absolute_x = button.x + ui_rect.x
    button_absolute_y = button.y + ui_rect.y
    if (button_absolute_x <= event.pos[0] <= button_absolute_x + button.width and
            button_absolute_y <= event.pos[1] <= button_absolute_y + button.height):
        return True
    return False



COLORS = [RED, BLUE, GREEN]

class ScoringBoard:
    def __init__(self, width: int, height: int, player_count: int):
        self.surface = pygame.Surface((width, height))
        self.surface.fill(WHITE)
        self.player_count = player_count
        self.font = pygame.font.Font(None, int(height / (player_count + 2)))
        self.players_score = [0] * player_count
        for i in range(player_count):
            score_img = self.font.render("0", True, COLORS[i])
            score_rect = score_img.get_rect(center = (width / 2, (i + 1) * height / (player_count + 1)))
            self.surface.blit(score_img, score_rect)

    def score_up(self, player_ser:int):
        self.players_score[player_ser] += 1
        self.update()

    def score_down(self, plater_ser:int):
        self.players_score[plater_ser] -= 1
        self.update()

    def update(self):
        self.surface.fill(WHITE)
        for i in range(self.player_count):
            score_img = self.font.render(str(self.players_score[i]), True, COLORS[i])
            score_rect = score_img.get_rect(
                center = (self.surface.get_width() / 2, (i + 1) * self.surface.get_height() / (self.player_count + 1)))
            self.surface.blit(score_img, score_rect)

