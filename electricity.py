import pygame
from pygame import display, time, event, draw, mouse, font
from objects import BLACK, WIDTH, HEIGHT, WHITE, FPS, Methods, ElectricityDot as Dot, Vector, Particle, Electron, Proton, MagneticField, ElectricBoard, Rainbow

CHARGE_RANGE = (1, 5)
AXES_VECTOR = Vector()
AXES_VALUES = [(Dot(WIDTH / 2, 0), 0), (Dot(0, HEIGHT / 2), 90)]
INFO_NAMES = ['Position', 'a', 'v']
INFO_FONT = font.SysFont('Consolas', 14)
PADDING = 10
INSIDE, OUTSIDE, POSITIVE, NEGATIVE, MAGNETIC, ELECTRIC = 'inside', 'outside', 'positive', 'negative', 'Magnetic', 'Electric'

window = display.set_mode((WIDTH, HEIGHT))
running = True

particle = Proton()

particles: list[Particle] = []
charge = CHARGE_RANGE[0]

fields: list[MagneticField] = []
boards: list[ElectricBoard] = []
create_field, origin_selected, field_direction, is_magnetic, shift_clicked = False, False, False, False, False
field_vector = Vector()
field_origin = Dot()


def handle_events() -> None:
    global running, charge, create_field, origin_selected, field_direction, is_magnetic, shift_clicked

    for e in event.get():
        if e.type == pygame.QUIT:
            running = False
            break

        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_c:
                if shift_clicked:
                    fields.clear()
                    boards.clear()
                else:
                    particles.clear()

            elif e.key == pygame.K_m or e.key == pygame.K_e:
                create_field = not create_field
                origin_selected = False
                is_magnetic = e.key == pygame.K_m

            elif e.key == pygame.K_s:
                if create_field:
                    field_direction = not field_direction

            elif e.key == pygame.K_LSHIFT:
                shift_clicked = True

        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_LSHIFT:
                shift_clicked = False

        elif e.type == pygame.MOUSEBUTTONDOWN:
            mx, my = e.pos

            if create_field:
                if e.button != 1:
                    continue
                mx, my = Dot.convert_from(mx, my)
                if origin_selected:
                    second_dot = Dot(mx, my)
                    radius = second_dot.distance(field_origin)

                    if is_magnetic and radius > particle.RADIUS:
                        fields.append(MagneticField(Dot(field_origin.x, field_origin.y), radius, field_direction))
                    elif not is_magnetic and radius > particle.RADIUS * 4:
                        boards.append(ElectricBoard(Dot(field_origin.x, field_origin.y), second_dot, field_direction))

                    origin_selected = False
                    create_field = False
                else:
                    field_origin.x = mx
                    field_origin.y = my
                    origin_selected = True
                continue

            if e.button in [1, 3]:
                _particle = generate_particle(e.button)
                particles.append(_particle)

            elif e.button in [4, 5]:
                if e.button == 4 and charge < CHARGE_RANGE[1]:
                    charge += 1
                elif e.button == 5 and charge > CHARGE_RANGE[0]:
                    charge -= 1


def draw_axes() -> None:
    draw.line(window, BLACK, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    draw.line(window, BLACK, (0, HEIGHT / 2), (WIDTH, HEIGHT / 2))

    for dot, angle in AXES_VALUES:
        AXES_VECTOR.angle = angle
        AXES_VECTOR.display(window, BLACK, dot)


def display_info() -> None:
    objects = [particle.position, particle.a, particle.v]
    heights = 0

    for i in range(len(objects)):
        text = INFO_FONT.render(f'{INFO_NAMES[i]}: {str(objects[i])}', True, BLACK)
        window.blit(text, (PADDING, heights + (i + 1) * PADDING))
        heights += text.get_height()

    charge_text = INFO_FONT.render(f'{charge}e', True, BLACK)
    window.blit(charge_text, charge_text.get_rect(bottomright=(WIDTH - PADDING, HEIGHT - PADDING)))

    if create_field:
        direction = (INSIDE if field_direction else OUTSIDE) if is_magnetic else (POSITIVE if field_direction else NEGATIVE)
        field_type = MAGNETIC if is_magnetic else ELECTRIC
        create_field_text = INFO_FONT.render(f'Creating {field_type} Field: {direction}', True, BLACK)
        window.blit(create_field_text, create_field_text.get_rect(bottomleft=(PADDING, HEIGHT - PADDING)))


def generate_particle(type: int) -> Particle:
    particle = Proton(True) if type == 1 else Electron(True)
    particle.q *= charge

    mx, my = mouse.get_pos()
    mx, my = particle.position.convert_from(mx, my)
    particle.position.x = mx
    particle.position.y = my

    return particle


def electricity() -> None:
    display.set_caption('Pygame Electricity')
    clock = time.Clock()

    path: list[tuple[float, float, tuple]] = []
    colors = iter(Rainbow())

    while running:
        window.fill(WHITE)
        clock.tick(FPS)

        handle_events()

        draw_axes()
        display_info()

        if create_field and origin_selected:
            mx, my = mouse.get_pos()
            cx, cy = Dot.convert_from(mx, my)
            field_vector.angle = Methods.get_angle_by_delta(cx - field_origin.x, cy - field_origin.y)
            field_vector.display(window, BLACK, field_origin, (mx, my))

        for board in boards:
            board.display(window)
        for field in fields:
            field.display(window)
        for _particle in particles:
            _particle.display(window)

        for x, y, color in path:
            draw.circle(window, color, (x, y), 1)

        particle.apply_forces(particles + boards, fields)
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