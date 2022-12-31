from pygame import surface, draw, font
from .magnetic import MagneticField
from .board import ElectricBoard
from ..constants import k, e, Me, BLUE, RED, GREY, WHITE, LIGHTBLUE, GREEN, WIDTH, HEIGHT
from ..methods import Methods
from ..dot import ElectricityDot as Dot
from ..vector import Vector


class Particle:
    RADIUS = 8
    FONT = font.SysFont('Consolas', 18)

    def __init__(self, q: float = 0, mass: float = 0, color: tuple[int, int, int] = GREY, placed: bool = False) -> None:
        self.q = q
        self.mass = mass
        self.color = color
        self.placed = placed

        self.position = Dot()
        self.a = Vector()
        self.v = Vector()

        self.Etotal = Vector()
        self.Fe = Vector()
        self.Fb = Vector()

        self.vector = Vector()

    def update(self) -> None:
        F = self.Fe + self.Fb
        self.a.size = F.size / self.mass # a = F/m
        self.a.angle = F.angle

        self.v += self.a

        vx, vy = self.v.delta()
        self.position.x += vx
        self.position.y += vy

    def display(self, window: surface.Surface) -> None:
        if not self.placed:
            self.update()

        x, y = self.position.convert()
        draw.circle(window, self.color, (x, y), self.RADIUS)
        text = self.FONT.render(Methods.get_sign(self.q), True, WHITE)
        window.blit(text, text.get_rect(center=(x, y)))

        if not self.placed:
            self.a.display(window, LIGHTBLUE, self.position, self.RADIUS * 30)
            self.v.display(window, GREEN, self.position, self.RADIUS * 2)

    def apply_forces(self, objects: list, fields: list) -> None:
        self.apply_electric_force(objects)
        self.apply_magnetic_force(fields)

    def apply_electric_force(self, objects: list) -> None:
        self.Etotal.reset()

        for obj in objects:
            if isinstance(obj, Particle):
                particle = obj
                r = particle.position.distance(self.position)
                if r == 0:
                    continue
                Esize = k * abs(particle.q) / r ** 2 # E = kQ/r^2

                Eangle = Methods.get_angle_by_delta(self.position.x - particle.position.x, self.position.y - particle.position.y)
                if particle.q < 0:
                    Eangle += 180
            elif isinstance(obj, ElectricBoard):
                board = obj
                if not board.in_field(self.position):
                    continue
                Esize = board.E

                Eangle = board.angle
                if board.angle == 0:
                    board_x = board.start.x
                    if board.positive and self.position.x <= board_x or \
                        not board.positive and self.position.x >= board_x:
                        Eangle += 180
                elif board.positive and board.l_board.below(self.position) or \
                    not board.positive and board.l_board.above(self.position):
                    Eangle += 180
            else:
                continue

            self.vector.size = Esize
            self.vector.angle = Eangle

            self.Etotal += self.vector

        angle = 180 if self.q < 0 and len(objects) > 0 else 0

        self.Fe.size = abs(self.q) * self.Etotal.size # F = qE
        self.Fe.angle = self.Etotal.angle + angle

    def apply_magnetic_force(self, fields: list) -> None:
        self.Fb.reset()

        for field in fields:
            if not isinstance(field, MagneticField):
                continue

            d = field.position.distance(self.position)
            if d > field.radius or self.q == 0:
                continue
            Fsize = abs(self.q) * self.v.size * field.B # F = qvB

            direction = 90 if (self.q > 0 and field.inside) or (self.q < 0 and not field.inside) else -90
            Fangle = self.v.angle + direction

            self.vector.angle = Fangle
            self.vector.size = Fsize

            self.Fb += self.vector

    def reset(self) -> None:
        self.position.x = 0
        self.position.y = 0
        self.a.reset()
        self.v.reset()

    def in_bounds(self) -> bool:
        x, y = self.position.convert()
        return 0 <= x <= WIDTH and 0 <= y <= HEIGHT

    def __str__(self) -> str:
        return str(self.q)


class Electron(Particle):
    def __init__(self, placed: bool = False) -> None:
        super().__init__(q=-e, mass=Me, color=RED, placed=placed)


class Proton(Particle):
    def __init__(self, placed: bool = False) -> None:
        super().__init__(q=e, mass=Me, color=BLUE, placed=placed)