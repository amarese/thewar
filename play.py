import pygame
import random
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

# Game class
class ColorInfectionGame:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Color Infection Game")
        self.running = False
        self.game_started = False
        self.victory = False
        self.game_over = False
        self.dot_positions = initial_dot_positions
        self.selected_dot = None
        self.line_start = (0, 0)
        self.line_end = (0, 0)
        self.line_color = (0, 0, 0)
        self.font = pygame.font.SysFont("Arial", 24)
        self.start_button = pygame.Rect(self.width // 2 - 50, self.height // 2 - 25, 100, 50)
        self.victory_button = pygame.Rect(self.width // 2 - 50, self.height // 2 - 25, 100, 50)
        self.particles = []  # Particle list
        self.start_time = 0
        self.remaining_time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.game_started and self.start_button.collidepoint(event.pos):
                        self.game_started = True
                        self.start_time = pygame.time.get_ticks()
                    else:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for i, (x, y, color, radius) in enumerate(self.dot_positions):
                            if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 <= radius ** 2:
                                self.selected_dot = self.dot_positions[i]
                                break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.selected_dot is not None:
                        drop_x, drop_y = pygame.mouse.get_pos()
                        for i, (x, y, color, radius) in enumerate(self.dot_positions):
                            if (drop_x - x) ** 2 + (drop_y - y) ** 2 <= radius ** 2:
                                self.dot_positions[i] = (x, y, self.selected_dot[2], radius)
                                break
                        self.selected_dot = None

    def update(self):
        if self.game_started and not self.victory and not self.game_over:
            for i, (x1, y1, color1, radius1) in enumerate(self.dot_positions):
                for j, (x2, y2, color2, radius2) in enumerate(self.dot_positions):
                    if i != j and color1 == color2:
                        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                        if distance <= radius1 + radius2:
                            self.dot_positions[j] = (x2, y2, color1, radius2)

            if all(color == self.dot_positions[0][2] for _, _, color, _ in self.dot_positions):
                self.victory = True

        # Particle system update
        for particle in self.particles:
            particle.update()
            if particle.finished:
                self.particles.remove(particle)

        # Calculate remaining time
        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.remaining_time = max(0, 600000 - elapsed_time) // 1000  # 600000 milliseconds = 10 minutes

        # Check if game over
        if self.remaining_time <= 0:
            self.game_over = True

    def draw(self):
        self.screen.fill((255, 255, 255))

        if not self.game_started:
            pygame.draw.rect(self.screen, (0, 0, 255), self.start_button)
            start_text = self.font.render("Start", True, (255, 255, 255))
            self.screen.blit(start_text, (self.width // 2 - start_text.get_width() // 2, self.height // 2 - start_text.get_height() // 2))
        else:
            for x, y, color, radius in self.dot_positions:
                pygame.draw.circle(self.screen, color, (x, y), radius)

            # Draw lines
            if self.selected_dot is not None:
                mouse_pos = pygame.mouse.get_pos()
                self.line_start = (self.selected_dot[0], self.selected_dot[1])
                self.line_end = mouse_pos
                self.line_color = self.selected_dot[2]
                pygame.draw.line(self.screen, self.line_color, self.line_start, self.line_end, 2)

            # Draw particles
            for particle in self.particles:
                particle.draw(self.screen)

            if self.victory:
                pygame.draw.rect(self.screen, (0, 0, 0), self.victory_button)
                victory_text = self.font.render("Victory!", True, (255, 255, 255))
                self.screen.blit(victory_text, (self.width // 2 - victory_text.get_width() // 2, self.height // 2 - victory_text.get_height() // 2))
            elif self.game_over:
                game_over_text = self.font.render("Game Over!", True, (255, 0, 0))
                self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, self.height // 2 - game_over_text.get_height() // 2))

        # Draw remaining time
        time_text = self.font.render("Time: {}s".format(self.remaining_time), True, (0, 0, 0))
        self.screen.blit(time_text, (10, 10))

        pygame.display.flip()

    def run(self):
        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            clock.tick(60)

        pygame.quit()


# Particle class
class Particle:
    def __init__(self, position, color, radius):
        self.position = position
        self.color = color
        self.radius = radius
        self.speed = random.uniform(0.5, 1.5)
        self.angle = random.uniform(0, 2 * math.pi)
        self.opacity = 255
        self.fade_rate = random.randint(1, 5)
        self.finished = False

    def update(self):
        self.position = (self.position[0] + self.speed * math.cos(self.angle),
                         self.position[1] + self.speed * math.sin(self.angle))
        self.opacity -= self.fade_rate
        if self.opacity <= 0:
            self.finished = True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color + (self.opacity,), (int(self.position[0]), int(self.position[1])), self.radius)


# Game instance creation and execution
game = ColorInfectionGame()
game.run()
