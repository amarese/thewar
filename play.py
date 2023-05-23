import pygame
import math

initial_dot_positions = [
    (100, 100, (255, 0, 0), 5),
    (200, 100, (0, 255, 0), 10),
    (100, 200, (0, 255, 255), 10),
    (200, 200, (255, 255, 0), 5),
    (300, 200, (255, 255, 0), 7),
    (300, 300, (0, 0, 255), 4),
    (200, 300, (0, 0, 255), 10),
    (200, 400, (0, 0, 255), 1),
    (300, 400, (255, 255, 0), 3),
    (500, 400, (255, 255, 0), 3),
    (700, 500, (255, 255, 0), 3),
    (700, 100, (0, 0, 255), 9),
    (500, 300, (0, 255, 0), 10),
]


class ColorInfectionGame:
    def __init__(self):
        pygame.init()

        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.dot_positions = initial_dot_positions
        self.selected_dot = None

        self.game_started = False
        self.victory = False

        self.font = pygame.font.Font(None, 36)

        self.start_button = pygame.Rect(self.width // 2 - 100, self.height // 2 - 50, 200, 100)
        self.victory_button = pygame.Rect(self.width // 2 - 100, self.height // 2 - 50, 200, 100)

        self.draw_line = False
        self.line_start = (0, 0)
        self.line_end = (0, 0)

        self.animation_duration = 3
        self.animation_start_time = 0

        pygame.display.set_caption("THE War")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if not self.game_started:
                        if self.start_button.collidepoint(mouse_x, mouse_y):
                            self.game_started = True
                    elif self.victory:
                        if self.victory_button.collidepoint(mouse_x, mouse_y):
                            self.reset_game()
                    else:
                        for x, y, color, radius in self.dot_positions:
                            if math.sqrt((mouse_x - x) ** 2 + (mouse_y - y) ** 2) <= radius:
                                self.selected_dot = (x, y, color)
                                self.draw_line = True
                                self.line_start = (x, y)
                                break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.game_started and not self.victory:
                    if self.selected_dot is not None:
                        drop_x, drop_y = pygame.mouse.get_pos()
                        for i, (x, y, color, radius) in enumerate(self.dot_positions):
                            if (drop_x - x) ** 2 + (drop_y - y) ** 2 <= radius ** 2:
                                self.dot_positions[i] = (x, y, self.selected_dot[2], radius)
                                break
                        self.selected_dot = None
                        self.draw_line = False
                        self.line_start = (0, 0)
                        self.line_end = (0, 0)

    def update(self):
        if not self.game_started:
            return

        colors = set([color for _, _, color, _ in self.dot_positions])
        if len(colors) == 1:
            self.victory = True

    def draw(self):
        self.screen.fill((255, 255, 255))

        if not self.game_started:
            pygame.draw.rect(self.screen, (0, 0, 0), self.start_button)
            start_text = self.font.render("Start", True, (255, 255, 255))
            self.screen.blit(start_text, (
            self.width // 2 - start_text.get_width() // 2, self.height // 2 - start_text.get_height() // 2))
        else:
            for x, y, color, radius in self.dot_positions:
                pygame.draw.circle(self.screen, color, (x, y), radius)

            if self.selected_dot is not None and self.draw_line:
                pygame.draw.line(self.screen, self.selected_dot[2], self.line_start, pygame.mouse.get_pos(), 2)

        if self.victory:
            pygame.draw.rect(self.screen, (0, 0, 0), self.victory_button)
            victory_text = self.font.render("Victory!", True, (255, 255, 255))
            self.screen.blit(victory_text, (
            self.width // 2 - victory_text.get_width() // 2, self.height // 2 - victory_text.get_height() // 2))

        pygame.display.flip()

    def reset_game(self):
        self.game_started = False
        self.victory = False
        self.dot_positions = initial_dot_positions

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()


game = ColorInfectionGame()
game.run()
