from data_structures_algorithms.solver_algo import solve_entropy_logic

class MinesweeperSolver:
    """
    Intermediary class that connects the Board data with the pure mathematical algorithm.
    """
    def __init__(self):
        pass

    def prepare_data(self, board):
        """
        Iterates through the Board matrix, creates a list of all unrevealed cells and indexes them.
        Then, finds revealed numbered cells to generate a list of constraints.
        
        Returns:
            n_unselected: Number of unrevealed cells.
            constraints: List of constraints as (indices, remaining_mines).
            unrevealed_cells: List of coordinates (x, y) of unrevealed cells in index order.
        """
        unrevealed_cells = []
        cell_to_index = {}
        
        for r in range(board.rows):
            for c in range(board.cols):
                cell = board.grid[r][c]
                if not cell.is_revealed and not cell.is_flagged:
                    cell_to_index[(r, c)] = len(unrevealed_cells)
                    unrevealed_cells.append((r, c))
                    
        n_unselected = len(unrevealed_cells)
        constraints = []
        
        for r in range(board.rows):
            for c in range(board.cols):
                cell = board.grid[r][c]
                if cell.is_revealed and cell.adjacent_mines > 0:
                    neighbors = []
                    flagged_count = 0
                    
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                                
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < board.rows and 0 <= nc < board.cols:
                                neighbor_cell = board.grid[nr][nc]
                                if neighbor_cell.is_flagged:
                                    flagged_count += 1
                                elif not neighbor_cell.is_revealed:
                                    if (nr, nc) in cell_to_index:
                                        neighbors.append(cell_to_index[(nr, nc)])
                    
                    if neighbors:
                        remaining_mines = cell.adjacent_mines - flagged_count
                        remaining_mines = max(0, remaining_mines)
                        constraints.append((neighbors, remaining_mines))
                        
        return n_unselected, constraints, unrevealed_cells

    def execute_solve(self, board):
        """
        Calls prepare_data to get mathematical sets, passes them to solve_entropy_logic.
        Maps the resulting probabilities back to (x, y) coordinates.
        
        Returns:
            Dictionary containing coordinates and corresponding probabilities: {(x, y): probability}
        """
        n_unselected, constraints, unrevealed_cells = self.prepare_data(board)
        
        if n_unselected == 0:
            return {}
            
        probabilities_array = solve_entropy_logic(n_unselected, constraints)
        
        result = {}
        for i in range(len(unrevealed_cells)):
            coord = unrevealed_cells[i]
            if i < len(probabilities_array):
                result[coord] = probabilities_array[i]
            
        return result
