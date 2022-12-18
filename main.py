import pygame
from pygame import display, time, event, mouse, font, surface
from objects import WIDTH, HEIGHT, WHITE, BLACK, Ball

FPS = 60
CAPTION = 'Pygame Physics'


def display_info(window: surface.Surface, ball: Ball) -> None:
    TEXT_FONT = font.SysFont('Consolas', 16)
    PADDING = 10

    equation_text = TEXT_FONT.render(str(ball.equation), True, BLACK)
    window.blit(equation_text, (PADDING, PADDING))


def main() -> None:
    pygame.init()
    
    display.set_caption(CAPTION)
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
        
        ball.bounce()
        ball.display(window, mouse.get_pos())
        display_info(window, ball)

        display.update()

    pygame.quit()


if __name__ == '__main__':
    main()