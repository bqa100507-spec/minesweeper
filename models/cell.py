"""
Cell model representing a single square on the Minesweeper board.
"""

class Cell:
    """
    Represents a single cell with its coordinates and state.
    """
    def __init__(self, x, y):
        """
        Initialize a cell with given coordinates and default states.
        """
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
