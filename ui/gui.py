"""
Graphical User Interface for the Minesweeper game using Tkinter.
"""

import tkinter as tk
from tkinter import messagebox
from models.board import Board

class MinesweeperGUI:
    """
    Tkinter-based GUI for playing Minesweeper.
    """
    def __init__(self, game_manager, network_manager=None):
        """
        Initialize the GUI with the provided game manager and optional network manager.
        """
        self.game_manager = game_manager
        self.board = game_manager.board
        self.network_manager = network_manager
        self.is_host = network_manager.is_host if network_manager else True

        
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        
        self.buttons = []
        self.create_menu()
        
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=5)
        
        undo_btn = tk.Button(self.top_frame, text="Undo", command=self.undo_action)
        undo_btn.pack(side=tk.LEFT, padx=5)
        
        hint_btn = tk.Button(self.top_frame, text="Hint", command=self.hint_action)
        hint_btn.pack(side=tk.LEFT, padx=5)
        
        auto_btn = tk.Button(self.top_frame, text="Auto Solve", command=self.start_auto_solve)
        auto_btn.pack(side=tk.LEFT, padx=5)
        
        self.timer_seconds = 0
        self.timer_running = False
        self.timer_id = None
        
        self.timer_label = tk.Label(self.top_frame, text="Time: 000", font=("Arial", 12, "bold"))
        self.timer_label.pack(side=tk.RIGHT, padx=10)
        
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(padx=10, pady=10)
        
        self.create_grid_widgets()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        if self.network_manager:
            self.root.after(100, self.process_network_events)
            if self.is_host:
                self.root.title("Minesweeper (Host)")
            else:
                self.root.title("Minesweeper (Client)")

        
    def create_menu(self):
        """
        Create the application menu bar including game difficulty options.
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game (Easy)", command=lambda: self.new_game(9, 9, 10))
        game_menu.add_command(label="New Game (Medium)", command=lambda: self.new_game(16, 16, 40))
        game_menu.add_command(label="New Game (Hard)", command=lambda: self.new_game(16, 30, 99))
        game_menu.add_command(label="Custom...", command=self.show_custom_dialog)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)

    def create_grid_widgets(self):
        """
        Create and layout the board buttons.
        """
        for r in range(self.board.rows):
            row_buttons = []
            for c in range(self.board.cols):
                btn = tk.Button(self.grid_frame, width=3, height=1, font=('Arial', 10, 'bold'))
                btn.bind("<Button-1>", lambda e, x=r, y=c: self.on_left_click(x, y))
                btn.bind("<Button-3>", lambda e, x=r, y=c: self.on_right_click(x, y))
                btn.grid(row=r, column=c)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
            
    def new_game(self, rows, cols, num_mines, seed=None):
        """
        Start a new game with the specified board dimensions and mine count.
        """
        if self.network_manager:
            if not self.is_host:
                messagebox.showinfo("Info", "Only the host can start a new game.")
                return
            import random
            seed = random.randint(0, 1000000)
            # Pick a random starting cell for both players
            start_x = random.randint(0, rows - 1)
            start_y = random.randint(0, cols - 1)
            self.network_manager.send_message({'type': 'INIT_GAME', 'rows': rows, 'cols': cols, 'mines': num_mines, 'seed': seed, 'start_x': start_x, 'start_y': start_y})
            
        self._start_game(rows, cols, num_mines, seed, start_x if self.network_manager else None, start_y if self.network_manager else None)

    def _start_game(self, rows, cols, num_mines, seed=None, start_x=None, start_y=None):
        """
        Internal method to handle the actual starting of a game.
        """
        if seed is not None:
            import random
            random.seed(seed)
            
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_seconds = 0
        self.timer_label.config(text="Time: 000")
        
        self.board = Board(rows, cols, num_mines)
        self.game_manager.reset_game(self.board)
        
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        self.buttons = []
        self.create_grid_widgets()
        
        if start_x is not None and start_y is not None:
            # Automatically reveal the starting cell for identical boards
            self.game_manager.handle_left_click(start_x, start_y)
            
        self.update_gui()

    def show_custom_dialog(self):
        """
        Show a dialog allowing the user to enter custom board dimensions and mine count.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("Custom Game")
        
        tk.Label(dialog, text="Rows:").grid(row=0, column=0, padx=5, pady=5)
        rows_entry = tk.Entry(dialog)
        rows_entry.insert(0, str(self.board.rows))
        rows_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Columns:").grid(row=1, column=0, padx=5, pady=5)
        cols_entry = tk.Entry(dialog)
        cols_entry.insert(0, str(self.board.cols))
        cols_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Mines:").grid(row=2, column=0, padx=5, pady=5)
        mines_entry = tk.Entry(dialog)
        mines_entry.insert(0, str(self.board.num_mines))
        mines_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def on_ok():
            try:
                r = int(rows_entry.get())
                c = int(cols_entry.get())
                m = int(mines_entry.get())
                if r < 1 or c < 1 or m < 1 or m >= r * c:
                    messagebox.showerror("Error", "Invalid inputs. Ensure mines < rows * cols.", parent=dialog)
                    return
                self.new_game(r, c, m)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid integers.", parent=dialog)
                
        tk.Button(dialog, text="OK", command=on_ok).grid(row=3, column=0, columnspan=2, pady=10)

    def hint_action(self):
        """
        Provide a hint for the next best move by highlighting a cell.
        Safe cells are highlighted green, mines are red, and best guesses are yellow.
        """
        if self.game_manager.game_over or self.game_manager.game_won:
            return
            
        if not self.board.mines_placed:
            messagebox.showinfo("Hint", "Start by clicking any cell to generate the board.")
            return

        analysis = self.game_manager.get_analysis()
        if not analysis:
            messagebox.showinfo("Hint", "Unable to determine a sure move right now.")
            return
            
        for x, y in analysis['certain_safe']:
            cell = self.board.grid[x][y]
            if not cell.is_flagged and not cell.is_revealed:
                self.buttons[x][y].config(bg="lightgreen")
                return
                
        for x, y in analysis['certain_mines']:
            cell = self.board.grid[x][y]
            if not cell.is_flagged and not cell.is_revealed:
                self.buttons[x][y].config(bg="lightcoral")
                return
                
        if analysis['others']:
            x, y = analysis['others'][0]
            self.buttons[x][y].config(bg="lightyellow")
            messagebox.showinfo("Hint", f"No certain moves. The safest guess is cell ({x}, {y}).")
            
    def check_timer_state(self):
        """
        Check the current game state and start or stop the timer accordingly.
        """
        if self.board.mines_placed and not self.game_manager.game_over and not self.game_manager.game_won:
            if not self.timer_running:
                self.timer_running = True
                self.update_timer()
        else:
            if self.timer_running:
                self.timer_running = False
                if self.timer_id:
                    self.root.after_cancel(self.timer_id)
                    self.timer_id = None

    def update_timer(self):
        """
        Update the timer label with the elapsed seconds.
        """
        if self.timer_running:
            self.timer_seconds += 1
            self.timer_label.config(text=f"Time: {self.timer_seconds:03d}")
            self.timer_id = self.root.after(1000, self.update_timer)

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
                    if btn.cget("bg") not in ["lightgreen", "lightcoral", "lightyellow"]:
                        btn.config(state=tk.NORMAL, relief=tk.RAISED, bg="SystemButtonFace")
                    else:
                        btn.config(state=tk.NORMAL, relief=tk.RAISED)
                        
                    if cell.is_flagged:
                        btn.config(text="F", fg="red")
                    else:
                        btn.config(text="")
                        
        self.check_timer_state()
                        
        if self.game_manager.game_over:
            if self.network_manager:
                self.network_manager.send_message({'type': 'OPPONENT_LOST'})
            messagebox.showinfo("Game Over", "You hit a mine!\nPress Undo to try again.")
        elif self.game_manager.game_won:
            if self.network_manager:
                self.network_manager.send_message({'type': 'OPPONENT_WON'})
            messagebox.showinfo("Congratulations", f"You won in {self.timer_seconds} seconds!")
            
    def on_left_click(self, x, y):
        """
        Event handler for left-clicking a cell.
        """
        if self.buttons[x][y].cget("bg") in ["lightgreen", "lightcoral", "lightyellow"]:
            self.buttons[x][y].config(bg="SystemButtonFace")
            
        self.game_manager.handle_left_click(x, y)
        self.update_gui()
        
    def on_right_click(self, x, y):
        """
        Event handler for right-clicking a cell.
        """
        if self.buttons[x][y].cget("bg") in ["lightgreen", "lightcoral", "lightyellow"]:
            self.buttons[x][y].config(bg="SystemButtonFace")
            
        self.game_manager.handle_right_click(x, y)
        self.update_gui()
        
    def undo_action(self):
        """
        Event handler for the undo button.
        """
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if self.buttons[r][c].cget("bg") in ["lightgreen", "lightcoral", "lightyellow"]:
                    self.buttons[r][c].config(bg="SystemButtonFace")
                    
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
            
    def process_network_events(self):
        """
        Poll and process events from the network manager.
        """
        if not self.network_manager:
            return
            
        while not self.network_manager.event_queue.empty():
            event = self.network_manager.event_queue.get()
            event_type = event.get('type')
            
            if event_type == 'INIT_GAME':
                self._start_game(event['rows'], event['cols'], event['mines'], event['seed'], event.get('start_x'), event.get('start_y'))
            elif event_type == 'OPPONENT_WON':
                messagebox.showinfo("Network", "The other player has won the game! Try to beat their time.")
            elif event_type == 'OPPONENT_LOST':
                messagebox.showinfo("Network", "The other player hit a mine! You can take your time to win.")
            elif event_type == 'ERROR':
                messagebox.showerror("Network Error", event.get('msg'))
            elif event_type == 'CONNECTED':
                if self.is_host:
                    import random
                    seed = random.randint(0, 1000000)
                    start_x = random.randint(0, self.board.rows - 1)
                    start_y = random.randint(0, self.board.cols - 1)
                    self.network_manager.send_message({'type': 'INIT_GAME', 'rows': self.board.rows, 'cols': self.board.cols, 'mines': self.board.num_mines, 'seed': seed, 'start_x': start_x, 'start_y': start_y})
                    self._start_game(self.board.rows, self.board.cols, self.board.num_mines, seed, start_x, start_y)
                else:
                    messagebox.showinfo("Network", "Connected to host. Waiting for game start...")
            elif event_type == 'DISCONNECTED':
                messagebox.showwarning("Network", "Disconnected from peer.")
                
        self.root.after(100, self.process_network_events)

    def on_close(self):
        """
        Handle window close event.
        """
        if self.network_manager:
            self.network_manager.stop()
        self.root.destroy()
            
    def run(self):
        """
        Start the Tkinter main loop.
        """
        self.update_gui()
        self.root.mainloop()
