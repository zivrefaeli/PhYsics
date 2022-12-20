import pygame
from pygame import display, time, event, draw, surface, mouse
from objects import BLACK, WIDTH, HEIGHT, WHITE, FPS, Particle, Electron, Proton


def draw_axes(window: surface.Surface) -> None:
    draw.line(window, BLACK, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    draw.line(window, BLACK, (0, HEIGHT / 2), (WIDTH, HEIGHT / 2))


def generate_particle(type: int) -> Particle:
    mx, my = mouse.get_pos()
    particle = Proton(True) if type == 1 else Electron(True)
    
    particle.position.x = mx - WIDTH / 2
    particle.position.y = HEIGHT / 2 - my

    return particle


def electricity() -> None:    
    display.set_caption('Pygame Electricity')
    window = display.set_mode((WIDTH, HEIGHT))
    clock = time.Clock()
    running = True

    electron = Electron()
    particles: list[Particle] = []

    while running:
        window.fill(WHITE)
        clock.tick(FPS)

        for e in event.get():
            if e.type == pygame.QUIT:
                running = False
                break

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_c:
                    particles.clear()

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button in [1, 3]:
                    particle = generate_particle(e.button)
                    particles.append(particle)
        
        draw_axes(window)

        electron.apply_force(particles)
        electron.display(window)

        for particle in particles:
            particle.display(window)

        display.update()

    pygame.quit()


if __name__ == '__main__':
    electricity()