from pygame import surface
from ..vector import Vector
from ..dot import BallisticsDot as Dot
from ..constants import HEIGHT, RED
from ..methods import Methods


class Luncher:
    COLOR = RED
    SCALE = 0.2

    def __init__(self, position: Dot, range: float) -> None:
        self.vector = Vector()
        self.position = position
        self.range = range

    def display(self, window: surface.Surface, mouse: tuple[float, float]) -> None:
        mx, my = mouse
        mouse_dot = Dot(mx, HEIGHT - my)

        d = mouse_dot.distance(self.position)
        if d > self.range:
            mouse = self.get_dot_on_range(mouse_dot, d)
            d = self.range

        self.vector.size = d * self.SCALE
        self.vector.angle = Methods.get_angle_by_delta(mouse_dot.x - self.position.x, mouse_dot.y - self.position.y)

        self.vector.display(window, self.COLOR, self.position, mouse)

    def get_dot_on_range(self, mouse: Dot, d: float) -> tuple[float, float]:
        k = self.range
        l = d - k

        rx = (k * mouse.x + l * self.position.x) / d
        ry = (k * mouse.y + l * self.position.y) / d
        return Dot.convert_to(rx, ry)

    def __str__(self) -> str:
        return str(self.vector)