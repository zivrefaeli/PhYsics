import pygame
pygame.init()

# Measurements 
WIDTH, HEIGHT = 800, 600
FLOAT_DIGITS = 5
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (74, 224, 83)
BLUE = (0, 0, 255)
GRAY = (240, 240, 240)
GREY = (200, 200, 200)
YELLOW = (242, 228, 75)
PINK = (240, 62, 213)

# Physics
GRAVITY = 0.5
k = 9 * 10 ** 9
e = 1.6 * 10 ** -19
Me = 9.11 * 10 ** -31