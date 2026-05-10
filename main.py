"""
Main application entry point for the Minesweeper game.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import socket

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.board import Board
from core.game_manager import GameManager
from ui.gui import MinesweeperGUI
from core.network import NetworkManager

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
        
        tk.Label(self.root, text="Minesweeper", font=("Arial", 20, "bold")).pack(pady=10)
        
        self.info_label = tk.Label(self.root, text="", fg="blue")
        self.info_label.pack(pady=5)
        
        tk.Button(self.root, text="Easy (9x9, 10 mines)", width=25, height=2, command=lambda: self.start_game(9, 9, 10)).pack(pady=5)
        tk.Button(self.root, text="Medium (16x16, 40 mines)", width=25, height=2, command=lambda: self.start_game(16, 16, 40)).pack(pady=5)
        tk.Button(self.root, text="Hard (16x30, 99 mines)", width=25, height=2, command=lambda: self.start_game(16, 30, 99)).pack(pady=5)
        tk.Button(self.root, text="Custom...", width=25, height=2, command=self.show_custom_dialog).pack(pady=5)
        
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        self.host_btn = tk.Button(frame, text="Host Game", width=11, height=2, command=self.show_host_dialog)
        self.host_btn.pack(side=tk.LEFT, padx=5)
        self.join_btn = tk.Button(frame, text="Join Game", width=11, height=2, command=self.show_join_dialog)
        self.join_btn.pack(side=tk.LEFT, padx=5)

        self.network_manager = None

    def start_game(self, rows, cols, num_mines):
        """
        Launch the main Minesweeper game with the specified parameters and close the startup window.
        """
        self.root.destroy()
        board = Board(rows, cols, num_mines)
        game_manager = GameManager(board)
        gui = MinesweeperGUI(game_manager, self.network_manager)
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

    def show_host_dialog(self):
        """
        Show dialog to host a multiplayer game.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("Host Game")
        
        tk.Label(dialog, text="Port:").grid(row=0, column=0, padx=5, pady=5)
        port_entry = tk.Entry(dialog)
        port_entry.insert(0, "5555")
        port_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def on_host():
            try:
                port = int(port_entry.get())
                self.network_manager = NetworkManager(is_host=True, port=port)
                self.network_manager.start()
                
                # Get local IP
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    s.connect(('10.255.255.255', 1))
                    ip = s.getsockname()[0]
                except Exception:
                    ip = '127.0.0.1'
                finally:
                    s.close()
                    
                self.info_label.config(text=f"Hosting on IP: {ip}:{port}\nNow select difficulty to start.")
                self.host_btn.config(state=tk.DISABLED)
                self.join_btn.config(state=tk.DISABLED)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid port.", parent=dialog)
                
        tk.Button(dialog, text="Host", width=10, command=on_host).grid(row=1, column=0, columnspan=2, pady=10)

    def show_join_dialog(self):
        """
        Show dialog to join a multiplayer game.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("Join Game")
        
        tk.Label(dialog, text="IP Address:").grid(row=0, column=0, padx=5, pady=5)
        ip_entry = tk.Entry(dialog)
        ip_entry.insert(0, "127.0.0.1")
        ip_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Port:").grid(row=1, column=0, padx=5, pady=5)
        port_entry = tk.Entry(dialog)
        port_entry.insert(0, "5555")
        port_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def on_join():
            try:
                ip = ip_entry.get()
                port = int(port_entry.get())
                self.network_manager = NetworkManager(is_host=False, host_ip=ip, port=port)
                self.network_manager.start()
                
                self.info_label.config(text=f"Connecting to {ip}:{port}...\nGame will start automatically.")
                self.host_btn.config(state=tk.DISABLED)
                self.join_btn.config(state=tk.DISABLED)
                dialog.destroy()
                
                # Start an arbitrary empty board, it will be synced by INIT_GAME
                self.start_game(9, 9, 10)
            except ValueError:
                messagebox.showerror("Error", "Invalid port.", parent=dialog)
                
        tk.Button(dialog, text="Join", width=10, command=on_join).grid(row=2, column=0, columnspan=2, pady=10)

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
