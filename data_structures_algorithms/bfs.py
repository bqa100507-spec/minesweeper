"""
Breadth-First Search (BFS) algorithm implementation for Minesweeper.
"""

from .queue import Queue

def flood_fill_bfs(board_matrix, start_x, start_y):
    """
    Perform a Breadth-First Search to reveal empty adjacent cells.
    Stops exploring further when encountering a cell with adjacent mines.
    """
    rows = len(board_matrix)
    cols = len(board_matrix[0]) if rows > 0 else 0
    
    q = Queue()
    q.enqueue((start_x, start_y))
    
    if not board_matrix[start_x][start_y].is_revealed:
        board_matrix[start_x][start_y].is_revealed = True
    
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
                  
    while not q.is_empty():
        x, y = q.dequeue()
        
        if board_matrix[x][y].adjacent_mines > 0:
            continue
            
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < rows and 0 <= ny < cols:
                neighbor = board_matrix[nx][ny]
                
                if not neighbor.is_revealed and not neighbor.is_flagged and not neighbor.is_mine:
                    neighbor.is_revealed = True
                    
                    if neighbor.adjacent_mines == 0:
                        q.enqueue((nx, ny))
