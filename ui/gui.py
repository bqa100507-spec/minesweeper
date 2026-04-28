"""
Graphical User Interface for the Minesweeper game using Tkinter.
"""

import tkinter as tk
from tkinter import messagebox

class MinesweeperGUI:
    """
    Tkinter-based GUI for playing Minesweeper.
    """
    def __init__(self, game_manager):
        """
        Initialize the GUI with the provided game manager.
        """
        self.game_manager = game_manager
        self.board = game_manager.board
        
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        
        self.buttons = []
        self.create_widgets()
        
    def create_widgets(self):
        """
        Create and layout the GUI widgets, including the board buttons and undo button.
        """
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5)
        
        undo_btn = tk.Button(top_frame, text="Undo", command=self.undo_action)
        undo_btn.pack(side=tk.LEFT, padx=5)
        
        auto_btn = tk.Button(top_frame, text="Auto Solve", command=self.start_auto_solve)
        auto_btn.pack(side=tk.LEFT, padx=5)
        
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(padx=10, pady=10)
        
        for r in range(self.board.rows):
            row_buttons = []
            for c in range(self.board.cols):
                btn = tk.Button(self.grid_frame, width=3, height=1, font=('Arial', 10, 'bold'))
                btn.bind("<Button-1>", lambda e, x=r, y=c: self.on_left_click(x, y))
                btn.bind("<Button-3>", lambda e, x=r, y=c: self.on_right_click(x, y))
                btn.grid(row=r, column=c)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
            
    def update_gui(self):
        """
        Update the visual state of all buttons on the board to reflect the current game state.
        """
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                btn = self.buttons[r][c]
                
                if cell.is_revealed:
                    btn.config(relief=tk.SUNKEN, state=tk.DISABLED, bg="#d3d3d3")
                    if cell.is_mine:
                        btn.config(text="*", disabledforeground="red")
                    elif cell.adjacent_mines > 0:
                        colors = ["", "blue", "green", "red", "purple", "maroon", "turquoise", "black", "gray"]
                        color = colors[cell.adjacent_mines] if cell.adjacent_mines < len(colors) else "black"
                        btn.config(text=str(cell.adjacent_mines), disabledforeground=color)
                    else:
                        btn.config(text="")
                else:
                    btn.config(state=tk.NORMAL, relief=tk.RAISED, bg="SystemButtonFace")
                    if cell.is_flagged:
                        btn.config(text="F", fg="red")
                    else:
                        btn.config(text="")
                        
        if self.game_manager.game_over:
            messagebox.showinfo("Game Over", "You hit a mine!\nPress Undo to try again.")
        elif self.game_manager.game_won:
            messagebox.showinfo("Congratulations", "You won!")
            
    def on_left_click(self, x, y):
        """
        Event handler for left-clicking a cell.
        """
        self.game_manager.handle_left_click(x, y)
        self.update_gui()
        
    def on_right_click(self, x, y):
        """
        Event handler for right-clicking a cell.
        """
        self.game_manager.handle_right_click(x, y)
        self.update_gui()
        
    def undo_action(self):
        """
        Event handler for the undo button.
        """
        self.game_manager.undo()
        self.update_gui()
        
    def start_auto_solve(self):
        """
        Starts the auto-solve loop.
        """
        if not self.game_manager.game_over and not self.game_manager.game_won:
            self.auto_solve_loop()

    def auto_solve_loop(self):
        """
        Executes one auto-solve step, then reschedules itself after 600ms for a slower animation effect.
        """
        if self.game_manager.game_over or self.game_manager.game_won:
            return
            
        action_taken = self.game_manager.auto_solve_step()
        self.update_gui()
        
        if action_taken and not self.game_manager.game_over and not self.game_manager.game_won:
            self.root.after(600, self.auto_solve_loop)
            
    def run(self):
        """
        Start the Tkinter main loop.
        """
        self.update_gui()
        self.root.mainloop()
