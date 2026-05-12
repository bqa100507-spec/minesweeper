# Minesweeper - Final Project

**Course**: Data Structures and Algorithms (IT004)
**University**: University of Information Technology VNU-HCM

## 1. Project Overview

This project implements the classic **Minesweeper** game using **Object-Oriented Programming (OOP)** and advanced algorithms. The core logic is separated from the graphical interface, allowing for easy maintenance and testing.

## 2. Architecture

The project follows a 3-layer architecture:

### 2.1. Data Structures & Algorithms Layer (`data_structures_algorithms/`)

- **`solver_algo.py`**: Implements the core logic for analyzing the board using **Minesweeper Entropy Logic**.
- **`entropy_calculator.py`**: Calculates probabilities and identifies cells that are definitely safe or mines.
- **Key Algorithms**:
    - **Minesweeper Entropy Logic**: Uses mathematical formulas to calculate the probability of each unrevealed cell containing a mine.
    - **Backtracking (Backtracking Solver)**: Used for solving complex patterns on the board.

### 2.2. Core Logic Layer (`core/`)

- **`board.py`**: Manages the game state (board layout, mine positions, cell states).
  - **Data Structure**: Uses a **2D List** to represent the board grid.
- **`solver.py`**: The bridge between the game logic and the mathematical algorithms.
  - **Responsibilities**: Analyzes board state, identifies patterns, and executes solving algorithms.
- **`game_manager.py`**: Orchestrates the game flow.
  - **Features**: Win/Loss detection, Mine counting, Step tracking.
- **`network.py`**: Handles local multiplayer connections.
  - **Features**: TCP socket server/client, asynchronous message queuing, deterministic board synchronization.

### 2.3. User Interface Layer (`ui/`)

- **`gui.py`**: Implements the **Graphical User Interface** using **Tkinter**.
  - **Features**:
    - **Visual Theme**: System-native UI elements with color-coded hints and numbers.
    - **Auto-Solve Animation**: Visualizes the AI solving the board step-by-step.
    - **Difficulty Selection**: Easy (9x9), Medium (16x16), Hard (16x30), and Custom (user-defined dimensions and mines).

## 3. Features

### Player Features
- **4 Difficulty Levels**: Easy (10 mines), Medium (40 mines), Hard (99 mines), and Custom.
- **Left-Click**: Reveal cell.
- **Right-Click**: Flag cell.
- **Middle-Click / Double-Click (Chording)**: Instantly reveals all surrounding unflagged cells if the adjacent flagged count matches the cell's number.
- **Timer & Flag Counter**: Tracks elapsed time and remaining mines to flag.
- **Leaderboard**: Automatically saves best completion times locally for Easy, Medium, and Hard modes (`leaderboard.json`).
- **Dark Mode**: Toggleable dark theme for a modern visual experience.
- **Sound Effects**: Immersive audio feedback for interactions and game events (uses Windows `winsound`).
- **Hint**: Suggests the safest next move by color-coding cells (Green = Safe, Red = Mine, Yellow = Best Guess).
- **Undo**: Reverts the board to the previous state using a custom Stack data structure.
- **Multiplayer (Competitive Race)**: 
  - Play against friends on identical boards over a Local Area Network (LAN).
  - Built-in TCP socket communication (Host/Join) with synchronized seeds.
  - **Live Opponent Progress**: Shows real-time percentage of safe cells revealed by the opponent.
  - **Rematch System**: Instantly request and accept rematches without disconnecting.

### AI (Solver) Features
- **Pattern Recognition**: Identifies logical patterns to deduce cell states.
- **Probability Calculation**: Calculates the exact probability of each cell containing a mine.
- **Auto-Solve Mode**: Automatically solves the board using the mathematical algorithm.
- **Visualization**: Shows the AI's thought process (revealing cells one by one).

## 4. How to Run

### Prerequisites
- **Python 3.x**
- **Tkinter**: Usually built-in with standard Python installations.

### Execution
```bash
python main.py
```

## 5. Documentation

The project includes automatically generated API documentation using `pdoc`.
To view the docstrings and understand the project's codebase:
1. Navigate to the `docs/` folder in the repository.
2. Open the `index.html` or `minesweeper.html` file in any web browser (Chrome, Edge, Firefox, etc.).
3. Browse the documented classes, methods, and modules.

## 6. Technical Highlights

- **Data Structures**:
  - **Stack**: Used for the `Undo` functionality.
  - **Queue**: Optimized `O(1)` dequeue operations using a head-pointer approach for BFS algorithms.
  - **Graph**: 2D Grid representing the game board.
- **Algorithms**:
  - **Breadth-First Search (BFS)**: Efficient flood-fill algorithm for revealing empty safe zones.
  - **Entropy & Backtracking**: Core AI logic solver.
- **Time Complexity**:
  - **Setup**: O(M*N)
  - **Reveal (Normal)**: O(1)
  - **Reveal (Flood Fill)**: O(M*N)
  - **Chording**: O(1) (checks 8 adjacent cells)
- **Space Complexity**: O(M*N) for storing the board state.
- **Modularity**: The solver algorithms can be tested independently of the GUI by mocking the `Board` object.
