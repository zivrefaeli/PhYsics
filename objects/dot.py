from math import sqrt
from .constants import HEIGHT


class Dot:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def get(self) -> tuple[float, float]:
        return self.x, self.y

    def convert(self) -> tuple[float, float]:
        """converts from coordinate system where (0, 0) is bottom left, to pygame's coordinate system"""
        return self.x, HEIGHT - self.y

    def distance(self, other) -> float:
        if not isinstance(other, Dot):
            return -1
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __str__(self) -> str:
        return str(self.get())