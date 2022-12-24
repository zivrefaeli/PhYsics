from pygame import surface, draw, font
from .magnetic import MagneticField
from ..dot import ElectricityDot as Dot
from ..constants import k, e, Me, BLUE, RED, GREY, WHITE, LIGHTBLUE, GREEN, WIDTH, HEIGHT
from ..vector import Vector
from ..methods import Methods


class Particle:
    RADIUS = 8
    FONT = font.SysFont('Consolas', 18)

    def __init__(self, q: float = 0, mass: float = 0, color: tuple[int, int, int] = GREY, placed: bool = False) -> None:
        self.position = Dot()
        self.a = Vector()
        self.v = Vector()

        self.Fe = Vector()
        self.Fb = Vector()

        self.q = q
        self.mass = mass
        self.color = color
        self.placed = placed

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

    def apply_forces(self, particles: list, fields: list) -> None:
        self.apply_electric_force(particles)
        self.apply_magnetic_force(fields)

    def apply_electric_force(self, particles: list) -> None:
        E_total = Vector()
        
        for particle in particles:
            if not isinstance(particle, Particle):
                continue
            
            Q = particle.q
            r = particle.position.distance(self.position)
            if r == 0:
                self.reset()
                return
            E = abs(k * Q / r ** 2)

            E_angle = Methods.get_angle_by_delta(self.position.x - particle.position.x, self.position.y - particle.position.y)
            if Q < 0:
                E_angle += 180

            E_total += Vector(E, E_angle)
        
        angle = 180 if self.q < 0 and len(particles) > 0 else 0
        
        self.Fe.size = E_total.size * abs(self.q)
        self.Fe.angle = E_total.angle + angle

    def apply_magnetic_force(self, fields: list) -> None:
        self.Fb.reset()

        for field in fields:
            if not isinstance(field, MagneticField):
                continue
            
            d = field.position.distance(self.position)
            if d > field.radius or self.q == 0:
                continue
            size = abs(self.q) * self.v.size * field.B

            direction = 90 if (self.q > 0 and field.inside) or (self.q < 0 and not field.inside) else -90
            angle = self.v.angle + direction

            self.Fb += Vector(size, angle)

    def reset(self) -> None:
        self.position.x = 0
        self.position.y = 0
        self.a.reset()
        self.v.reset()

    def in_bounds(self) -> bool:
        x, y = self.position.convert()
        return 0 <= x <= WIDTH and 0 <= y <= HEIGHT


class Electron(Particle):
    def __init__(self, placed: bool = False) -> None:
        super().__init__(q=-e, mass=Me, color=RED, placed=placed)


class Proton(Particle):
    def __init__(self, placed: bool = False) -> None:
        super().__init__(q=e, mass=Me, color=BLUE, placed=placed)