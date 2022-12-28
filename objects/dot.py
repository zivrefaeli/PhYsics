from math import sqrt
from abc import ABC, abstractmethod
from .constants import WIDTH, HEIGHT


class Dot(ABC):
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def get(self) -> tuple[float, float]:
        return self.x, self.y

    def convert(self) -> tuple[float, float]:
        return self.convert_to(self.x, self.y)

    @staticmethod
    @abstractmethod
    def convert_to(x: float, y: float) -> tuple[float, float]:
        """converts TO pygame's coordinate system from a normal coordinate system"""
        pass

    @staticmethod
    @abstractmethod
    def convert_from(x: float, y: float) -> tuple[float, float]:
        """converts FROM pygame's coordinate system to a normal coordinate system"""
        pass

    def distance(self, other) -> float:
        if not isinstance(other, type(self)):
            return -1
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __str__(self) -> str:
        return str(self.get())


class BallisticsDot(Dot):
    @staticmethod
    def convert_from(x: float, y: float) -> tuple[float, float]:
        return x, HEIGHT - y

    @staticmethod
    def convert_to(x: float, y: float) -> tuple[float, float]:
        return BallisticsDot.convert_from(x, y)


class ElectricityDot(Dot):
    @staticmethod
    def convert_from(x: float, y: float) -> tuple[float, float]:
        return x - WIDTH / 2, HEIGHT / 2 - y

    @staticmethod
    def convert_to(x: float, y: float) -> tuple[float, float]:
        return x + WIDTH / 2, HEIGHT / 2 - y