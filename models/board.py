"""
Board model representing the Minesweeper game board.
"""

import random
from .cell import Cell

class Board:
    """
    Represents the Minesweeper board, managing cells and mine placement.
    """
    def __init__(self, rows, cols, num_mines):
        """
        Initialize the board with given dimensions and number of mines.
        """
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.mines_placed = False

    def place_mines(self, first_x, first_y):
        """
        Place mines randomly on the board, avoiding the first clicked cell and its immediate neighbors.
        """
        mines_to_place = self.num_mines
        not_to_place = []
        for i in range(first_x - 1, first_x + 2):
            for j in range(first_y - 1, first_y + 2):
                if 0 <= i < self.rows and 0 <= j < self.cols:
                    not_to_place.append((i, j))
        while mines_to_place > 0:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            
            if not self.grid[r][c].is_mine and (r, c) not in not_to_place:
                self.grid[r][c].is_mine = True
                mines_to_place -= 1
        
        self.calculate_numbers()
        self.mines_placed = True

    def calculate_numbers(self):
        """
        Calculate the number of adjacent mines for each cell on the board.
        """
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
                      
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].is_mine:
                    continue
                
                count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.grid[nr][nc].is_mine:
                            count += 1
                self.grid[r][c].adjacent_mines = count
