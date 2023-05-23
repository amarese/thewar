import pygame
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

dot_radius = 10
dot_positions = [(100, 100, (255, 0, 0)),  # 빨간색 점
                 (200, 100, (0, 255, 0)),  # 초록색 점
                 (100, 200, (0, 0, 255)),  # 파란색 점
                 (200, 200, (255, 255, 0))]  # 노란색 점
selected_dot = None

game_started = False
victory = False

font = pygame.font.Font(None, 36)

start_button = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 100)
victory_button = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 100)

pygame.display.set_caption("THE War")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if not game_started:
                    if start_button.collidepoint(mouse_x, mouse_y):
                        game_started = True
                elif victory:
                    if victory_button.collidepoint(mouse_x, mouse_y):
                        game_started = False
                        victory = False
                        dot_positions = [(100, 100, (255, 0, 0)),
                                         (200, 100, (0, 255, 0)),
                                         (100, 200, (0, 0, 255)),
                                         (200, 200, (255, 255, 0))]
                else:
                    for x, y, color in dot_positions:
                        if math.sqrt((mouse_x - x) ** 2 + (mouse_y - y) ** 2) <= dot_radius:
                            selected_dot = (x, y, color)
                            break
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and game_started and not victory:
                if selected_dot is not None:
                    drop_x, drop_y = pygame.mouse.get_pos()
                    for i, (x, y, color) in enumerate(dot_positions):
                        if (drop_x - x) ** 2 + (drop_y - y) ** 2 <= dot_radius ** 2:
                            dot_positions[i] = (x, y, selected_dot[2])
                            break
                    selected_dot = None

    screen.fill((255, 255, 255))

    if not game_started:
        pygame.draw.rect(screen, (0, 0, 0), start_button)
        start_text = font.render("Start", True, (255, 255, 255))
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 - start_text.get_height() // 2))
    else:
        for x, y, color in dot_positions:
            pygame.draw.circle(screen, color, (x, y), dot_radius)

        if selected_dot is not None:
            selected_x, selected_y, selected_color = selected_dot
            pygame.draw.circle(screen, selected_color, (selected_x, selected_y), dot_radius)

            closest_dot = None
            closest_distance = float("inf")
            for x, y, color in dot_positions:
                distance = math.sqrt((selected_x - x) ** 2 + (selected_y - y) ** 2)
                if distance < closest_distance and color == selected_color:
                    closest_distance = distance
                    closest_dot = (x, y)

            if closest_dot is not None:
                pygame.draw.line(screen, selected_color, (selected_x, selected_y), closest_dot, 2)

        colors = set([color for _, _, color in dot_positions])
        if len(colors) == 1:
            victory = True

    if victory:
        pygame.draw.rect(screen, (0, 0, 0), victory_button)
        victory_text = font.render("Victory!", True, (255, 255, 255))
        screen.blit(victory_text,
                    (width // 2 - victory_text.get_width() // 2, height // 2 - victory_text.get_height() // 2))

    pygame.display.flip()

pygame.quit()
