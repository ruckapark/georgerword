import collections

class GraphArrowwordSolver:
    """
    A graph-based backtracking solver for arrowword puzzles.
    """

    def __init__(self, words, grid_size=8):
        self.words = sorted(words, key=len, reverse=True)
        self.grid_size = grid_size
        self.graph = self._create_graph()

    def _create_graph(self):
        """Creates a graph representation of the grid."""
        graph = collections.defaultdict(list)
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                        graph[(r, c)].append((nr, nc))
        return graph

    def solve(self):
        """
        Attempts to solve the arrowword puzzle using a graph-based approach.
        """
        initial_grid = [['' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        return self._solve_recursive(self.words, initial_grid, [])

    def _solve_recursive(self, words_to_place, grid, placed_words_info):
        """
        The main recursive function that tries to place words.
        """
        if not words_to_place:
            return grid, placed_words_info

        word_to_place = words_to_place[0]
        remaining_words = words_to_place[1:]

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                for direction in ['H', 'V']:
                    if self._is_valid_placement(word_to_place, r, c, direction, grid):
                        new_grid = self._place_word(grid, word_to_place, r, c, direction)
                        new_placed_info = placed_words_info + [{'word': word_to_place, 'row': r, 'col': c, 'direction': direction}]
                        
                        solution_grid, solution_info = self._solve_recursive(remaining_words, new_grid, new_placed_info)
                        if solution_grid:
                            return solution_grid, solution_info
        
        return None, None

    def _is_valid_placement(self, word, r, c, direction, grid):
        """Checks if a word can be placed at a given position and direction."""
        if direction == 'H':
            if c + len(word) > self.grid_size: return False
            for i in range(len(word)):
                if grid[r][c + i] not in ('', word[i]): return False
        elif direction == 'V':
            if r + len(word) > self.grid_size: return False
            for i in range(len(word)):
                if grid[r + i][c] not in ('', word[i]): return False
        return True

    def _place_word(self, grid, word, r, c, direction):
        """Places a word on a copy of the grid and returns the new grid."""
        new_grid = [row[:] for row in grid]
        if direction == 'H':
            for i in range(len(word)):
                new_grid[r][c + i] = word[i]
        elif direction == 'V':
            for i in range(len(word)):
                new_grid[r + i][c] = word[i]
        return new_grid

def print_grid(grid):
    """Utility function to print the grid nicely."""
    if not grid:
        print("No solution found.")
        return
    for row in grid:
        print(" ".join(char if char else '.' for char in row))

# --- Main Execution ---
if __name__ == "__main__":
    word_list = ['HAPPILY', 'HOLIDAY', 'YELLOW', 'LEGEND', 'LOVE', 'EWE', 'DONUT', 'LIT', 'POT', 'EVIL', 'EYE', 'END', 'NILE']
    
    solver = GraphArrowwordSolver(word_list, grid_size=8)
    final_grid, placed_info = solver.solve()
    
    print("## Final Grid State (Graph Solver) ##")
    print_grid(final_grid)
    
    print("\n## Placed Word Information ##")
    if placed_info:
        for info in sorted(placed_info, key=lambda x: x['word']):
            print(f"- {info['word']}: ({info['row']}, {info['col']}), Direction: {info['direction']}")
