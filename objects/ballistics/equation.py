from math import cos, tan, radians
from pygame import surface, draw
from ..vector import Vector
from ..dot import BallisticsDot as Dot
from ..constants import GRAVITY, WIDTH, HEIGHT, FLOAT_DIGITS


class Equation:
    STEP = 3

    def __init__(self, vector: Vector, position: Dot, color: tuple) -> None:
        self.vector = vector
        self.position = position
        self.color = color
        self.calculate()

    def calculate(self) -> None:
        self.f = lambda x: 0

        if self.vector.size == 0:
            self.value = ''
            return
        if self.vector.angle in [90, 270]:
            self.value = f'x = {round(self.position.x)}'
            return

        alpha = radians(self.vector.angle)
        v = self.vector.size

        c1 = tan(alpha)
        c2 = GRAVITY / (2 * v ** 2 * cos(alpha) ** 2)
        
        x0, y0 = self.position.get()
        self.f = lambda x: y0 + c1 * (x - x0) - c2 * (x - x0) ** 2
        
        c1, c2, x0, y0 = (round(value, FLOAT_DIGITS) for value in [c1, c2, x0, y0])
        self.value = f'y = {y0} + {c1}(x - {x0}) - {c2}(x - {x0})^2'

    def display(self, window: surface.Surface) -> None:
        self.calculate()

        if not self.value:
            return
        if 'x =' in self.value:
            draw.line(window, self.color, (self.position.x, 0), (self.position.x, HEIGHT))
            return

        direction = -1 if 90 < self.vector.angle < 270 else 1

        x = self.position.x
        y = self.f(x)
        while 0 <= x <= WIDTH and y >= 0:
            draw.circle(window, self.color, (x, HEIGHT - y), 1)
            x += self.STEP * direction
            y = self.f(x)

    def __str__(self) -> str:
        return self.value