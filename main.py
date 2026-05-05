"""
Main application entry point for the Minesweeper game.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.board import Board
from core.game_manager import GameManager
from ui.gui import MinesweeperGUI

class StartupWindow:
    """
    Provides a pre-game dialog to select the game difficulty or set custom parameters.
    """
    def __init__(self):
        """
        Initialize the startup window and display difficulty buttons.
        """
        self.root = tk.Tk()
        self.root.title("Minesweeper - Select Difficulty")
        
        window_width = 300
        window_height = 350
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        
        self.root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
        
        tk.Label(self.root, text="Minesweeper", font=("Arial", 20, "bold")).pack(pady=20)
        
        tk.Button(self.root, text="Easy (9x9, 10 mines)", width=25, height=2, command=lambda: self.start_game(9, 9, 10)).pack(pady=5)
        tk.Button(self.root, text="Medium (16x16, 40 mines)", width=25, height=2, command=lambda: self.start_game(16, 16, 40)).pack(pady=5)
        tk.Button(self.root, text="Hard (16x30, 99 mines)", width=25, height=2, command=lambda: self.start_game(16, 30, 99)).pack(pady=5)
        tk.Button(self.root, text="Custom...", width=25, height=2, command=self.show_custom_dialog).pack(pady=5)

    def start_game(self, rows, cols, num_mines):
        """
        Launch the main Minesweeper game with the specified parameters and close the startup window.
        """
        self.root.destroy()
        board = Board(rows, cols, num_mines)
        game_manager = GameManager(board)
        gui = MinesweeperGUI(game_manager)
        gui.run()

    def show_custom_dialog(self):
        """
        Show a dialog allowing the user to enter custom board dimensions and mine count.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("Custom Game")
        
        tk.Label(dialog, text="Rows:").grid(row=0, column=0, padx=5, pady=5)
        rows_entry = tk.Entry(dialog)
        rows_entry.insert(0, "16")
        rows_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Columns:").grid(row=1, column=0, padx=5, pady=5)
        cols_entry = tk.Entry(dialog)
        cols_entry.insert(0, "16")
        cols_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Mines:").grid(row=2, column=0, padx=5, pady=5)
        mines_entry = tk.Entry(dialog)
        mines_entry.insert(0, "40")
        mines_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def on_ok():
            try:
                r = int(rows_entry.get())
                c = int(cols_entry.get())
                m = int(mines_entry.get())
                if r < 1 or c < 1 or m < 1 or m >= r * c:
                    messagebox.showerror("Error", "Invalid inputs. Ensure mines < rows * cols.", parent=dialog)
                    return
                self.start_game(r, c, m)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid integers.", parent=dialog)
                
        tk.Button(dialog, text="OK", width=10, command=on_ok).grid(row=3, column=0, columnspan=2, pady=10)

    def run(self):
        """
        Start the Tkinter main loop for the startup window.
        """
        self.root.mainloop()

def main():
    """
    Show startup window to select difficulty and start the application.
    """
    startup = StartupWindow()
    startup.run()

if __name__ == "__main__":
    main()
