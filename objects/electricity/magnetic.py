from pygame import surface, draw
from ..constants import RED, BLUE
from ..dot import ElectricityDot as Dot


class MagneticField:
    WIDTH = 3
    DELTA = 8
    GAP = 12
    SIZE = DELTA * 2 + GAP
    COLOR = RED
    DIRECTION_COLOR = BLUE

    def __init__(self, radius: float, inside: bool) -> None:
        self.radius = radius
        self.position = Dot(100, 100)
        self.inside = inside

        self.B = 10 ** -13 # Tesla
        self.tester = Dot()
        self.init_dots()

    def init_dots(self) -> None:
        self.dots: list[tuple[float, float]] = []

        diameter = int(self.radius * 2)
        px, py = self.position.convert()

        x, y = Dot.convert_from(px - self.radius, py - self.radius)
        x += self.GAP + self.DELTA
        y -= self.GAP + self.DELTA
        
        amount = (diameter - self.WIDTH * 2) // self.SIZE
        amount_width = self.GAP + amount * self.SIZE
        diff = self.radius * 2 - amount_width
        x += diff / 2
        y -= diff / 2
        xi = x

        for _ in range(amount):
            for _ in range(amount):
                self.tester.x = x
                self.tester.y = y
                if self.tester.distance(self.position) <= self.radius - self.WIDTH:
                    self.dots.append(Dot.convert_to(x, y))
                x += self.SIZE
            x = xi
            y -= self.SIZE

    def display(self, window: surface.Surface) -> None:
        draw.circle(window, self.COLOR, self.position.convert(), self.radius, self.WIDTH)
        # draw.rect(window, RED, (int(px - self.radius), int(py - self.radius), diameter, diameter), self.WIDTH)

        for x, y in self.dots:
            if self.inside:
                self.draw_x(window, x, y)
            else:
                draw.circle(window, self.DIRECTION_COLOR, (x, y), self.WIDTH)

    def draw_x(self, window: surface.Surface, x: float, y: float) -> None:
        x1, y1, x2, y2 = x - self.DELTA, y + self.DELTA, x + self.DELTA, y - self.DELTA
        x1, y1, x2, y2 = (int(n) for n in [x1, y1, x2, y2])
        draw.line(window, self.DIRECTION_COLOR, (x1, y1), (x2, y2), self.WIDTH)
        draw.line(window, self.DIRECTION_COLOR, (x1, y2), (x2, y1), self.WIDTH)