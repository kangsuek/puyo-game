import pygame
from puyo.board import Board
from puyo.puyo import Puyo
from puyo.colors import BLACK, WHITE

class Game:
    def __init__(self):
        self.width, self.height = 300, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("뿌요뿌요")
        self.clock = pygame.time.Clock()
        self.board = Board(self.width, self.height)
        self.current_puyo = Puyo(self.board.grid_width // 2 - 1, 0)
        self.game_over = False
        self.score = 0
        self.drop_time = 0

    def run(self):
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        print(f"게임 오버! 최종 점수: {self.score}")
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_puyo(-1)
                elif event.key == pygame.K_RIGHT:
                    self.move_puyo(1)
                elif event.key == pygame.K_UP:
                    self.rotate_puyo()
                elif event.key == pygame.K_DOWN:
                    self.drop_puyo()

    def move_puyo(self, dx):
        new_x = self.current_puyo.x + dx
        if self.is_valid_position(new_x, self.current_puyo.y, self.current_puyo.rotation):
            self.current_puyo.move(dx)

    def rotate_puyo(self):
        new_rotation = (self.current_puyo.rotation + 1) % 4
        if self.is_valid_position(self.current_puyo.x, self.current_puyo.y, new_rotation):
            self.current_puyo.rotate()
        else:
            # Try to shift left if rotation is not valid
            if self.is_valid_position(self.current_puyo.x - 1, self.current_puyo.y, new_rotation):
                self.current_puyo.x -= 1
                self.current_puyo.rotate()
            # If shifting left doesn't work, try shifting right
            elif self.is_valid_position(self.current_puyo.x + 1, self.current_puyo.y, new_rotation):
                self.current_puyo.x += 1
                self.current_puyo.rotate()

    def is_valid_position(self, x, y, rotation):
        positions = self.current_puyo.get_positions(rotation)
        for dx, dy in positions:
            new_x, new_y = x + dx, y + dy
            if new_x < 0 or new_x >= self.board.grid_width or new_y >= self.board.grid_height:
                return False
            if new_y >= 0 and self.board.grid[new_y][new_x] is not None:
                return False
        return True

    def update(self):
        self.drop_time += self.clock.get_rawtime()
        if self.drop_time > 500:
            self.drop_puyo()
            self.drop_time = 0

    def drop_puyo(self):
        if self.is_valid_position(self.current_puyo.x, self.current_puyo.y + 1, self.current_puyo.rotation):
            self.current_puyo.y += 1
        else:
            self.board.place_puyo(self.current_puyo)
            self.score += self.board.clear_matches()
            self.board.apply_gravity()
            self.current_puyo = Puyo(self.board.grid_width // 2 - 1, 0)
            if not self.is_valid_position(self.current_puyo.x, self.current_puyo.y, self.current_puyo.rotation):
                self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)
        self.board.draw(self.screen)
        self.current_puyo.draw(self.screen)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()
