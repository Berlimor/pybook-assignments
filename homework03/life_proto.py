import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        self.grid = self.create_grid(True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:  # type: ignore
                    running = False
            self.draw_lines()
            self.grid = self.get_next_generation()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return[
                    [round(random.random()) for _ in range(self.cell_width)] 
                    for _ in range(self.cell_height)
                ]
        else: 
            return[[0 for _ in range(self.cell_width)] 
                    for _ in range(self.cell_height)
                ]


    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                if self.grid[row][col] == 0:
                    pygame.draw.rect(
                        self.screen, 
                        pygame.Color('white'), 
                        (
                            row * self.cell_size + 1, 
                            col * self.cell_size + 1, 
                            self.cell_size - 1, 
                            self.cell_size - 1
                        ))
                else:
                     pygame.draw.rect(
                        self.screen, 
                        pygame.Color('green'), 
                        (
                            row * self.cell_size + 1, 
                            col * self.cell_size + 1, 
                            self.cell_size - 1, 
                            self.cell_size - 1
                        ))


    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        """
        neighbours = []
        pos_row, pos_col = cell
        rows = len(self.grid)
        cols = len(self.grid[0]) if rows else 0
        for row in range(max(0, pos_row - 1), min(rows, pos_row + 2)):
            for col in range(max(0, pos_col - 1), min(cols, pos_col + 2)):
                if (row, col) != cell: 
                    neighbours.append(self.grid[row][col]) 
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        """
        counter = self.create_grid()
        for pos_row, row in enumerate(self.grid):
            for pos_col, col in enumerate(row):
                cell = (pos_row, pos_col)
                alive_neighbours = sum(self.get_neighbours(cell))
                if col:
                    if alive_neighbours != 2 and alive_neighbours != 3:
                        counter[pos_row][pos_col] = 0
                    else: 
                        counter[pos_row][pos_col] = 1
                else: 
                    if alive_neighbours == 3:
                        counter[pos_row][pos_col] = 1
        return counter

game = GameOfLife()
game.run()