class Rainbow:
    MIN = 50
    MAX = 200

    def __init__(self) -> None:
        self.color = [self.MAX, self.MIN, self.MIN]
        self.up, self.down = 1, 0
        self.is_up = True

    def __iter__(self):
        return self

    def __next__(self) -> tuple[int, int, int]:
        if self.is_up:
            self.color[self.up] += 1
            if self.color[self.up] == self.MAX:
                self.is_up = False
                self.up = (self.up + 1) % 3
        else:
            self.color[self.down] -= 1
            if self.color[self.down] == self.MIN:
                self.is_up = True
                self.down = (self.down + 1) % 3
        return tuple(self.color)