from math import cos, sin, radians, sqrt
from pygame import surface, draw
from .methods import Methods
from .dot import Dot


class Vector:
    WIDTH = 2
    HEAD_SIZE = 10
    HEAD_ANGLE = 30

    def __init__(self, size: float = 0, angle: float = 0) -> None:
        self.size = size
        self.angle = angle

    @property
    def angle(self) -> float:
        return self._angle
    
    @angle.setter
    def angle(self, value: float) -> None:
        self._angle = (value + 360) % 360

    def delta(self) -> tuple[float, float]:
        dx = self.size * cos(radians(self.angle))
        dy = self.size * sin(radians(self.angle))
        return dx, dy

    def reset(self) -> None:
        self.size = 0
        self.angle = 0

    def display(self, window: surface.Surface, color: tuple[int, int, int], start: Dot, value: object = 1) -> None:
        if isinstance(value, tuple):
            # value is a pygame dot
            px, py = value
        elif isinstance(value, int) or isinstance(value, float):
            # value is scale
            dx, dy = self.delta()
            x, y = start.get()
            x += dx * value
            y += dy * value
            px, py = start.convert_to(x, y)
        else:
            return
        draw.line(window, color, start.convert(), (px, py), self.WIDTH)

        angle = self.angle - self.HEAD_ANGLE + 180
        for _ in range(2):
            dx = self.HEAD_SIZE * cos(radians(angle))
            dy = self.HEAD_SIZE * sin(radians(angle))
            draw.line(window, color, (px, py), (px + dx, py - dy), 2)
            angle += 2 * self.HEAD_ANGLE
        

    def __add__(self, other):
        if not isinstance(other, Vector):
            return self

        dx1, dy1 = self.delta()
        dx2, dy2 = other.delta()
        dx, dy = dx1 + dx2, dy1 + dy2

        size = sqrt(dx ** 2 + dy ** 2)
        angle = Methods.get_angle_by_delta(dx, dy)
        return Vector(size, angle)

    def __str__(self) -> str:
        return f'(|{self.size}|, {self.angle})'