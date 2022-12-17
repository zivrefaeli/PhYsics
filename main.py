import pygame
from pygame import display, time, event
from objects import WIDTH, HEIGHT, WHITE

FPS = 60


def main() -> None:
    pygame.init()

    window = display.set_mode((WIDTH, HEIGHT))
    clock = time.Clock()
    running = True

    while running:
        window.fill(WHITE)
        clock.tick(FPS)

        for e in event.get():
            if e.type == pygame.QUIT:
                running = False
                break
        
        display.update()

    pygame.quit()


if __name__ == '__main__':
    main()