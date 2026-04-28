"""
Main application entry point for the Minesweeper game.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.board import Board
from core.game_manager import GameManager
from ui.gui import MinesweeperGUI

def main():
    """
    Initialize the board, game manager, and GUI, and start the application.
    """
    board = Board(16, 16, 40)
    
    game_manager = GameManager(board)
    
    gui = MinesweeperGUI(game_manager)
    
    gui.run()

if __name__ == "__main__":
    main()
