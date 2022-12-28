from pygame import surface, draw
from .luncher import Luncher
from .equation import Equation
from ..constants import BLACK, GRAY, GREEN, BLUE, HEIGHT, WIDTH, GRAVITY
from ..dot import BallisticsDot as Dot
from ..vector import Vector


class Ball:
    RADIUS = 25
    RANGE = 5 * RADIUS
    WALLS_FRICTION = 0.5

    def __init__(self) -> None:
        self.position = Dot(self.RADIUS, self.RADIUS + HEIGHT / 2)
        self.a = Vector(GRAVITY, 270)
        self.v = Vector()

        self.luncher = Luncher(self.position, self.RANGE)
        self.lunched = False

        self.equation = Equation(self.luncher.vector, self.position, BLUE)
        self.path = Equation(self.v, self.position, GREEN)

    def update(self) -> None:
        if self.position.y <= self.RADIUS and not self.lunched:
            self.position.y = self.RADIUS
            self.v.size = 0
            return

        self.lunched = False
        self.v += self.a

        vx, vy = self.v.delta()
        self.position.x += vx
        self.position.y += vy

    def display(self, window: surface.Surface, mouse: tuple[float, float]) -> None:
        self.update()

        x, y = self.position.convert()
        draw.circle(window, GRAY, (x, y), self.RANGE)
        draw.circle(window, BLACK, (x, y), self.RADIUS)

        self.luncher.display(window, mouse)
        self.equation.display(window)

        self.path.vector = self.v
        self.path.display(window)

    def lunch(self) -> None:
        self.lunched = True
        self.v += self.luncher.vector

    def bounce(self, x1: float = 0, x2: float = WIDTH) -> None:
        bounced = False
        x1 += self.RADIUS
        x2 -= self.RADIUS

        if self.position.x < x1:
            self.position.x = x1
            bounced = True
        elif self.position.x > x2:
            self.position.x = x2
            bounced = True

        if bounced:
            self.v.angle = 180 - self.v.angle
            self.v.size *= self.WALLS_FRICTION

    def __str__(self) -> str:
        return str(self.equation)