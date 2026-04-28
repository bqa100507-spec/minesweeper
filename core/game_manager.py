"""
Game manager logic for Minesweeper.
"""

import copy
from data_structures_algorithms.stack import Stack
from data_structures_algorithms.bfs import flood_fill_bfs
from core.solver import MinesweeperSolver

class GameManager:
    """
    Manages the core game state and logic, including interactions.
    """
    def __init__(self, board):
        """
        Initialize the game manager with a specific board state.
        """
        self.board = board
        self.history = Stack()
        self.game_over = False
        self.game_won = False
        self.solver = MinesweeperSolver()

    def save_state(self):
        """
        Save the current board state to the history stack for undo functionality.
        """
        state = copy.deepcopy(self.board.grid)
        self.history.push(state)

    def undo(self):
        """
        Revert the board to its previous state.
        """
        if not self.history.is_empty():
            previous_state = self.history.pop()
            self.board.grid = previous_state
            self.game_over = False
            self.game_won = False
            
    def handle_left_click(self, x, y):
        """
        Handle a left-click event (reveal a cell).
        """
        if self.game_over or self.game_won:
            return
            
        cell = self.board.grid[x][y]
        
        if cell.is_flagged or cell.is_revealed:
            return
            
        self.save_state()
            
        if not self.board.mines_placed:
            self.board.place_mines(x, y)
            
        if cell.is_mine:
            cell.is_revealed = True
            self.game_over = True
            self.reveal_all_mines()
        else:
            if cell.adjacent_mines == 0:
                flood_fill_bfs(self.board.grid, x, y)
            else:
                cell.is_revealed = True
                
        self.check_win()

    def handle_right_click(self, x, y):
        """
        Handle a right-click event (toggle flag).
        """
        if self.game_over or self.game_won:
            return
            
        cell = self.board.grid[x][y]
        if not cell.is_revealed:
            self.save_state()
            cell.is_flagged = not cell.is_flagged

    def reveal_all_mines(self):
        """
        Reveal all mines on the board (typically after game over).
        """
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if self.board.grid[r][c].is_mine:
                    self.board.grid[r][c].is_revealed = True

    def check_win(self):
        """
        Check if the player has won the game by revealing all safe cells.
        """
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                if not cell.is_mine and not cell.is_revealed:
                    return False
        self.game_won = True

    def get_analysis(self):
        """
        Activates MinesweeperSolver to analyze the current board.
        Returns a dictionary categorizing the cells:
        - certain_mines: List of coordinates that are definitely mines.
        - certain_safe: List of coordinates that are definitely safe.
        - others: List of other cell coordinates sorted from lowest to highest mine probability.
        """
        if self.game_over or self.game_won:
            return None
            
        probabilities = self.solver.execute_solve(self.board)
        
        certain_mines = []
        certain_safe = []
        others = []
        
        for (x, y), prob in probabilities.items():
            if prob >= 0.999:
                certain_mines.append((x, y))
            elif prob <= 0.001:
                certain_safe.append((x, y))
            else:
                others.append(((x, y), prob))
                
        others.sort(key=lambda item: item[1])
        
        return {
            'certain_mines': certain_mines,
            'certain_safe': certain_safe,
            'others': [item[0] for item in others]
        }

    def auto_solve_step(self):
        """
        Executes a single step of the auto-solver (performing only one action to simulate a player).
        Returns True if an action was taken, False otherwise.
        """
        analysis = self.get_analysis()
        if not analysis:
            return False
            
        for x, y in analysis['certain_mines']:
            cell = self.board.grid[x][y]
            if not cell.is_flagged and not cell.is_revealed:
                self.handle_right_click(x, y)
                return True
                
        for x, y in analysis['certain_safe']:
            cell = self.board.grid[x][y]
            if not cell.is_flagged and not cell.is_revealed:
                self.handle_left_click(x, y)
                return True
                
        if analysis['others']:
            x, y = analysis['others'][0]
            self.handle_left_click(x, y)
            action_taken = True
            
        return False
