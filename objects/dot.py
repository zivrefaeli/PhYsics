from math import sqrt
from abc import ABC, abstractmethod
from .constants import WIDTH, HEIGHT


class Dot(ABC):
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def get(self) -> tuple[float, float]:
        return self.x, self.y

    @abstractmethod
    def convert(self) -> tuple[float, float]:
        """converts from coordinate system where (0, 0) is bottom left, to pygame's coordinate system"""
        pass

    def distance(self, other) -> float:
        if not isinstance(other, type(self)):
            return -1
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __str__(self) -> str:
        return str(self.get())


class BallisticsDot(Dot):
    def convert(self) -> tuple[float, float]:
        return self.x, HEIGHT - self.y


class ElectricityDot(Dot):
    def convert(self) -> tuple[float, float]:
        return WIDTH / 2 + self.x, HEIGHT / 2 - self.y