import pygame
from pygame import display, time, event, mouse, font, surface
from objects import BLACK, WHITE, WIDTH, HEIGHT, FPS, FLOAT_DIGITS, Ball

TEXT_FONT = font.SysFont('Consolas', 16)
PADDING = 10


def display_info(window: surface.Surface, ball: Ball) -> None:
    equation_text = TEXT_FONT.render(str(ball.equation), True, BLACK)
    window.blit(equation_text, (PADDING, PADDING))

    angle_text = TEXT_FONT.render(f'Target Angle: {round(ball.luncher.vector.angle, FLOAT_DIGITS)}°', True, BLACK)
    window.blit(angle_text, (PADDING, equation_text.get_height() + 2 * PADDING))


def ballistics() -> None:    
    display.set_caption('Pygame Ballistics')
    window = display.set_mode((WIDTH, HEIGHT))
    clock = time.Clock()
    running = True

    ball = Ball()

    while running:
        window.fill(WHITE)
        clock.tick(FPS)

        for e in event.get():
            if e.type == pygame.QUIT:
                running = False
                break

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    ball.lunch()

        ball.display(window, mouse.get_pos())
        display_info(window, ball)

        display.update()

    pygame.quit()


if __name__ == '__main__':
    ballistics()