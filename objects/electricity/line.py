from pygame import surface, draw
from ..constants import X_RANGE
from ..dot import ElectricityDot as Dot


class LinearLine:
    WIDTH = 2

    def __init__(self, slope: float = 0, dot: Dot = Dot()) -> None:
        self.m = slope
        self.b = dot.y - slope * dot.x # y = mx + (y1 - m * x1)

    def evaluate(self, x: float) -> float:
        return self.m * x + self.b

    def above(self, dot: Dot) -> bool:
        return dot.y >= self.evaluate(dot.x)

    def below(self, dot: Dot) -> bool:
        return dot.y <= self.evaluate(dot.x)

    def display(self, window: surface.Surface, color: tuple[int, int, int], x_range: tuple[float, float] = X_RANGE) -> None:
        dots = [Dot.convert_to(x_range[i], self.evaluate(x_range[i])) for i in range(2)]
        draw.line(window, color, dots[0], dots[1], self.WIDTH)

    def __str__(self) -> str:
        return f'y = {self.m}x + {self.b}'