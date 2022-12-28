from pygame import surface
from ..constants import RED
from ..methods import Methods
from ..dot import BallisticsDot as Dot
from ..vector import Vector


class Luncher:
    COLOR = RED
    SCALE = 0.2

    def __init__(self, position: Dot, range: float) -> None:
        self.vector = Vector()
        self.position = position
        self.range = range
        self.mouse_dot = Dot()

    def display(self, window: surface.Surface, mouse: tuple[float, float]) -> None:
        mx, my = mouse
        mx, my = Dot.convert_to(mx, my)
        self.mouse_dot.x = mx
        self.mouse_dot.y = my

        d = self.mouse_dot.distance(self.position)
        if d > self.range:
            mouse = self.get_dot_on_range(d)
            d = self.range

        self.vector.size = d * self.SCALE
        self.vector.angle = Methods.get_angle_by_delta(self.mouse_dot.x - self.position.x, self.mouse_dot.y - self.position.y)

        self.vector.display(window, self.COLOR, self.position, mouse)

    def get_dot_on_range(self, d: float) -> tuple[float, float]:
        k = self.range
        l = d - k

        rx = (k * self.mouse_dot.x + l * self.position.x) / d
        ry = (k * self.mouse_dot.y + l * self.position.y) / d
        return Dot.convert_to(rx, ry)

    def __str__(self) -> str:
        return str(self.vector)