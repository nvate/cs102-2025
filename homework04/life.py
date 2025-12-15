import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:

        if randomize:
            return [[random.randint(0, 1) for _ in range(self.rows)] for _ in range(self.cols)]
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:

        y, x = cell
        neighbours = []

        for offset_y in (-1, 0, 1):
            for offset_x in (-1, 0, 1):
                if offset_y == 0 and offset_x == 0:
                    continue
                new_y = y + offset_y
                new_x = x + offset_x

                if 0 <= new_y < self.rows and 0 <= new_x < self.cols:
                    neighbours.append(self.curr_generation[new_y][new_x])

        return neighbours

    def get_next_generation(self) -> Grid:

        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for y in range(self.rows):
            for x in range(self.cols):
                neighbours = self.get_neighbours((y, x))
                alive_neighbours = sum(neighbours)

                if self.curr_generation[y][x] == 1:
                    if 2 <= alive_neighbours <= 3:
                        new_grid[y][x] = 1
                else:
                    if alive_neighbours == 3:
                        new_grid[y][x] = 1

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False

        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """

        with open(filename, "r") as file:
            lines = file.readlines()
            k = 0
            new_grid = []

        while True:
            try:
                s = lines[k].strip().split()
                new_grid.append(list(map(int, s)))
                k += 1
            except IndexError:
                break

        rows = len(new_grid)
        cols = len(new_grid[0])
        grid = GameOfLife(size=(rows, cols), randomize=False)
        grid.curr_generation = new_grid
        grid.prev_generation = grid.create_grid()

        return grid

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as file:
            for rows in self.curr_generation:
                for element in rows:
                    file.write(str(element))
                file.write("\n")
