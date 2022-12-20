from pygame import surface, draw, font
from ..dot import ElectricityDot as Dot
from ..constants import k, e, Me, BLUE, RED, GREY, WHITE
from ..vector import Vector
from ..methods import Methods

def get_sign(q: float) -> str:
    if q > 0:
        return '+'
    if q < 0:
        return '-'
    return '0'


class Particle:
    RADIUS = 8
    FONT = font.SysFont('Consolas', 18)

    def __init__(self, q: float = 0, mass: float = 0, color: tuple[int, int, int] = GREY, placed: bool = False) -> None:
        self.position = Dot()
        self.a = Vector()
        self.v = Vector()

        self.q = q
        self.mass = mass
        self.color = color
        self.placed = placed

    def update(self) -> None:
        self.v += self.a

        vx, vy = self.v.delta()
        self.position.x += vx
        self.position.y += vy

    def display(self, window: surface.Surface) -> None:
        if not self.placed:
            self.update()

        x, y = self.position.convert()
        draw.circle(window, self.color, (x, y), self.RADIUS)
        text = self.FONT.render(get_sign(self.q), True, WHITE)
        window.blit(text, text.get_rect(center=(x, y)))

    def apply_force(self, particles: list) -> None:
        E_total = Vector()
        
        for particle in particles:
            if not isinstance(particle, Particle):
                continue
            
            Q = particle.q
            r = particle.position.distance(self.position)
            if r == 0:
                continue # TODO: lunch particle out of screen

            E = abs(k * Q / r ** 2)

            E_angle = Methods.get_angle_by_delta(self.position.x - particle.position.x, self.position.y - particle.position.y)
            if Q < 0:
                E_angle += 180

            E_total += Vector(E, E_angle)
        
        F = E_total
        F.size *= abs(self.q) # F = qE
        if self.q < 0:
            F.angle += 180
        
        self.a.size = F.size / self.mass # a = F / m
        self.a.angle = F.angle


class Electron(Particle):
    def __init__(self, placed: bool = False) -> None:
        super().__init__(q=-e, mass=Me, color=RED, placed=placed)


class Proton(Particle):
    def __init__(self, placed: bool = False) -> None:
        super().__init__(q=e, mass=Me, color=BLUE, placed=placed)