import pygame
from pygame import display, time, event, draw, surface, mouse, font
from objects import BLACK, WIDTH, HEIGHT, WHITE, FPS, Particle, Electron, Proton, MagneticField, Rainbow 

running = True
particles: list[Particle] = []
particle_charge = 1
fields: list[MagneticField] = [MagneticField(100, True)]


def handle_events() -> None:
    global running, particle_charge

    for e in event.get():
        if e.type == pygame.QUIT:
            running = False
            break

        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_c:
                particles.clear()

        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button in [1, 3]:
                particle = generate_particle(e.button, particle_charge)
                particles.append(particle)

            elif e.button in [4, 5]:
                if e.button == 4 and particle_charge < 5:
                    particle_charge += 1
                elif e.button == 5 and particle_charge > 1:
                    particle_charge -= 1


def draw_axes(window: surface.Surface) -> None:
    draw.line(window, BLACK, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    draw.line(window, BLACK, (0, HEIGHT / 2), (WIDTH, HEIGHT / 2))

    particle = Particle()
    dots = [(WIDTH / 2, 0, 90), (WIDTH, HEIGHT / 2, 0)]
    for x, y, angle in dots:
        x, y = particle.position.convert_from(x, y)
        particle.position.x = x
        particle.position.y = y
        particle.v.angle = angle
        particle.v.display(window, BLACK, particle.position)


def display_info(window: surface.Surface, electron: Particle, charge: int) -> None:
    TEXT_FONT = font.SysFont('Consolas', 14)
    PADDING = 10

    objects = [electron.position, electron.a, electron.v]
    names = ['Position', 'a', 'v']
    heights = 0

    for i in range(len(objects)):
        text = TEXT_FONT.render(f'{names[i]}: {str(objects[i])}', True, BLACK)
        window.blit(text, (PADDING, heights + (i + 1) * PADDING))
        heights += text.get_height()

    charge_text = TEXT_FONT.render(f'{charge}e', True, BLACK)
    window.blit(charge_text, charge_text.get_rect(bottomright=(WIDTH - PADDING, HEIGHT - PADDING)))


def generate_particle(type: int, charge: int) -> Particle:
    particle = Proton(True) if type == 1 else Electron(True)
    particle.q *= charge

    mx, my = mouse.get_pos()
    mx, my = particle.position.convert_from(mx, my)
    particle.position.x = mx
    particle.position.y = my

    return particle


def electricity() -> None:
    display.set_caption('Pygame Electricity')
    window = display.set_mode((WIDTH, HEIGHT))
    clock = time.Clock()

    particle = Proton()

    path: list[tuple[float, float, tuple]] = []
    colors = iter(Rainbow())

    while running:
        window.fill(WHITE)
        clock.tick(FPS)

        handle_events()
        
        draw_axes(window)
        display_info(window, particle, particle_charge)

        for field in fields:
            field.display(window)
        for _particle in particles:
            _particle.display(window)

        for x, y, color in path:
            draw.circle(window, color, (x, y), 1)

        particle.apply_forces(particles, fields)
        particle.display(window)
        
        if particle.v.size > 0:
            x, y = particle.position.convert()
            path.append((x, y, next(colors)))
        if not particle.in_bounds():
            particle.reset()
            particles.clear()
            path.clear()

        display.update()

    pygame.quit()


if __name__ == '__main__':
    electricity()