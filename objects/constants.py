import pygame
pygame.init()

# Measurements
WIDTH, HEIGHT = 800, 600
FLOAT_DIGITS = 5
FPS = 60
X_RANGE = (-WIDTH / 2, WIDTH / 2)
Y_RANGE = (-HEIGHT / 2, HEIGHT / 2)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (74, 224, 83)
BLUE = (0, 0, 255)
GRAY = (240, 240, 240)
GREY = (200, 200, 200)
LIGHTBLUE = (11, 166, 222)

# Physics
GRAVITY = 0.5
k = 9 * 10 ** 9 # N * m^2 / C^2
e = 1.6 * 10 ** -19 # C
Me = 9.11 * 10 ** -31 # kg