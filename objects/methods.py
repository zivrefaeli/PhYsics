from math import degrees, atan

class Methods:
    @staticmethod
    def get_angle_by_delta(dx: float, dy: float) -> float:
        if dy == 0:
            if dx >= 0:
                return 0
            return 180
        
        if dx == 0:
            if dy > 0:
                return 90
            return 270
        
        alpha = degrees(atan(dy / dx))
        if dx > 0:
            if dy > 0:
                return alpha
            return 360 + alpha
        return 180 + alpha