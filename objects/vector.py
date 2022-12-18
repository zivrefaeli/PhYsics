from math import cos, sin, radians, sqrt
from .methods import Methods


class Vector:
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