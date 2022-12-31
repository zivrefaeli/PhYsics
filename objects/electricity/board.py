from math import pi, atan, degrees
from pygame import surface, draw
from .line import LinearLine
from ..constants import k, Y_RANGE, BLACK, BLUE, RED
from ..dot import ElectricityDot as Dot


class ElectricBoard:
    def __init__(self, start: Dot, end: Dot, positive: bool) -> None:
        self.start = start
        self.end = end
        self.positive = positive
        self.color = BLUE if positive else RED

        self.const = 2 * pi * k
        self.sigma = 10 ** -23
        self.E = self.const * self.sigma # E = 2pi * k * sigma

        self.angle = 0
        self.l_board = LinearLine()
        self.l_top = LinearLine()
        self.l_bottom = LinearLine()

        self.create_lines()

    def create_lines(self) -> None:
        if self.start.y == self.end.y:
            self.angle = 90
            self.l_board.b = self.start.y
            return

        if self.start.x == self.end.x:
            self.update_lines(0)
            return

        m = (self.start.y - self.end.y) / (self.start.x - self.end.x)
        m1 = -1 / m
        self.angle = (degrees(atan(m1)) + 180) % 180

        self.l_board = LinearLine(m, self.start)
        self.update_lines(m1)

    def update_lines(self, slope: float) -> None:
        l1 = LinearLine(slope, self.start)
        l2 = LinearLine(slope, self.end)

        if l1.b > l2.b:
            self.l_top = l1
            self.l_bottom = l2
        else:
            self.l_top = l2
            self.l_bottom = l1

    def in_field(self, dot: Dot) -> bool:
        if self.start.y == self.end.y:
            return self.start.x <= dot.x <= self.end.x or self.end.x <= dot.x <= self.start.x

        if self.start.x == self.end.x:
            return self.l_bottom.b <= dot.y <= self.l_top.b

        return self.l_top.below(dot) and self.l_bottom.above(dot)

    def display(self, window: surface.Surface) -> None:
        if self.start.x == self.end.x:
            self.draw_vertical(window, self.color, self.start.x, (self.l_top.b, self.l_bottom.b))
        else:
            self.l_board.display(window, self.color, (self.start.x, self.end.x))

        if self.start.y == self.end.y:
            self.draw_vertical(window, BLACK, self.start.x)
            self.draw_vertical(window, BLACK, self.end.x)
        else:
            self.l_top.display(window, BLACK)
            self.l_bottom.display(window, BLACK)
    
    def draw_vertical(self, window: surface.Surface, color: tuple[int, int, int], x: float, y_range: tuple[float, float] = Y_RANGE) -> None:
        dots = [Dot.convert_to(x, y_range[i]) for i in range(2)]
        draw.line(window, color, dots[0], dots[1], LinearLine.WIDTH)

    def __str__(self) -> str:
        sign = '+' if self.positive else '-'
        return f'(|{self.E}|, {sign})'