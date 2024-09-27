import pygame
from puyo.colors import COLORS
from collections import deque

class Board:
    def __init__(self, width, height):
        self.grid_size = 30
        self.grid_width = width // self.grid_size
        self.grid_height = height // self.grid_size
        self.grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def is_valid_move(self, puyo, dx, dy):
        for px, py in puyo.get_positions():
            new_x, new_y = px + puyo.x + dx, py + puyo.y + dy
            if new_x < 0 or new_x >= self.grid_width or new_y >= self.grid_height:
                return False
            if new_y >= 0 and self.grid[new_y][new_x]:
                return False
        return True

    def place_puyo(self, puyo):
        for (x, y), color in zip(puyo.get_positions(), [puyo.color1, puyo.color2]):
            self.grid[y + puyo.y][x + puyo.x] = color

    def clear_matches(self) -> int:
        cleared = set()
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x] and (x, y) not in cleared:
                    matched = self.find_matches(x, y, self.grid[y][x])
                    if len(matched) >= 4:
                        cleared.update(matched)
        for x, y in cleared:
            self.grid[y][x] = None
        self.apply_gravity()
        return len(cleared)

    def find_matches(self, x: int, y: int, color: str) -> set:
        matched = set()
        stack = [(x, y)]

        while stack:
            current_x, current_y = stack.pop()
            if (current_x, current_y) in matched or \
               current_x < 0 or current_x >= self.grid_width or \
               current_y < 0 or current_y >= self.grid_height or \
               self.grid[current_y][current_x] != color:
                continue

            matched.add((current_x, current_y))

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                stack.append((current_x + dx, current_y + dy))

        return matched

    def apply_gravity(self):
        for x in range(self.grid_width):
            column = [self.grid[y][x] for y in range(self.grid_height) if self.grid[y][x]]
            column = [None] * (self.grid_height - len(column)) + column
            for y in range(self.grid_height):
                self.grid[y][x] = column[y]

    def draw(self, screen):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x]:
                    pygame.draw.rect(screen, self.grid[y][x], (x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size))
