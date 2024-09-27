import pygame
import random
from puyo.colors import COLORS

class Puyo:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.color1 = random.choice(COLORS)
        self.color2 = random.choice(COLORS)
        self.rotation = 0

    def rotate(self) -> None:
        self.rotation = (self.rotation + 1) % 4

    def move(self, dx: int) -> None:
        self.x += dx

    def get_positions(self, rotation=None) -> list[tuple[int, int]]:
        if rotation is None:
            rotation = self.rotation
        if rotation == 0:
            return [(0, 0), (0, 1)]
        elif rotation == 1:
            return [(0, 0), (1, 0)]
        elif rotation == 2:
            return [(0, 1), (0, 0)]
        else:
            return [(1, 0), (0, 0)]

    def draw(self, screen: pygame.Surface) -> None:
        grid_size = 30
        for i, (dx, dy) in enumerate(self.get_positions()):
            color = self.color1 if i == 0 else self.color2
            pygame.draw.rect(screen, color, ((self.x + dx) * grid_size, (self.y + dy) * grid_size, grid_size, grid_size))
