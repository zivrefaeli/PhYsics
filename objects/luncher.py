from math import cos, sin, radians 
from pygame import surface, draw
from .vector import Vector
from .dot import Dot
from .constants import HEIGHT, RED
from .methods import Methods


class Luncher:
    COLOR = RED
    WIDTH = 2
    SCALE = 0.2
    HEAD_LENGTH = 10
    HEAD_ANGLE = 30

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

        draw.line(window, self.COLOR, self.position.convert(), mouse, self.WIDTH)
        self.draw_head(window, mouse)

    def draw_head(self, window: surface.Surface, mouse: tuple[float, float]) -> None:
        alpha = self.HEAD_ANGLE
        beta = self.vector.angle
        d = self.HEAD_LENGTH
        
        mx, my = mouse
        for i in range(2):
            if i == 0:
                angle = 180 - alpha + beta
            else:
                angle = alpha + beta - 180
            
            dx = d * cos(radians(angle))
            dy = d * sin(radians(angle))
            draw.line(window, self.COLOR, mouse, (mx + dx, my - dy), self.WIDTH)

    def get_dot_on_range(self, mouse: Dot, d: float) -> tuple[float, float]:
        k = self.range
        l = d - k

        rx = (k * mouse.x + l * self.position.x) / d
        ry = (k * mouse.y + l * self.position.y) / d
        return rx, HEIGHT - ry

    def __str__(self) -> str:
        return str(self.vector)