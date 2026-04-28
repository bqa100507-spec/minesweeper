def solve_entropy_logic(n_unselected, constraints, max_iter=100, tol=1e-5):
    """
    Solves for the probability of each unselected cell containing a mine using an entropy-based
    iterative proportional fitting algorithm.
    
    Args:
        n_unselected: Number of hidden/unselected cells.
        constraints: A list of tuples (indices, c_j), where `indices` is a list/set of cell indices,
                     and `c_j` is the number of mines in those cells.
        max_iter: Maximum number of iterations for the algorithm.
        tol: Tolerance for convergence.
        
    Returns:
        A list of probabilities for each cell.
    """
    if n_unselected == 0:
        return []

    p = [1.0] * n_unselected
    q = [1.0] * n_unselected
    
    for _ in range(max_iter):
        p_old = list(p)
        
        for indices, c_j in constraints:
            sum_p = sum(p[i] for i in indices)
            sum_q = sum(q[i] for i in indices)
            
            if sum_p > 0 and c_j > 0:
                factor_p = c_j / sum_p
                for i in indices:
                    p[i] *= factor_p
            elif c_j == 0:
                for i in indices:
                    p[i] = 0.0
                    
            safe_count = len(indices) - c_j
            if sum_q > 0 and safe_count > 0:
                factor_q = safe_count / sum_q
                for i in indices:
                    q[i] *= factor_q
            elif safe_count == 0:
                for i in indices:
                    q[i] = 0.0

        for i in range(n_unselected):
            total = p[i] + q[i]
            if total > 0:
                p[i] /= total
                q[i] /= total
            else:
                p[i] = 0.0
                q[i] = 1.0
                
        if all(abs(p[i] - p_old[i]) < tol for i in range(n_unselected)):
            break
            
    return p
