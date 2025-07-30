import itertools
from grid_check import is_valid_grid

class BruteForceArrowwordSolver:
    """
    A brute-force solver that tries all permutations of words.
    """

    def __init__(self, words, grid_size=8):
        self.words = words
        self.grid_size = grid_size
        self.iterations = 0

    def solve(self):
        """
        Attempts to solve the arrowword puzzle by trying all permutations of words.
        """
        for word_permutation in itertools.permutations(self.words):
            if self.iterations >= 10000:
                print("Brute-force solver reached 10,000 iterations without finding a solution.")
                break
            self.iterations += 1
            grid = [['' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
            placed_info = []
            solution = self._solve_recursive(list(word_permutation), grid, placed_info)
            if solution:
                final_grid, final_placed_info = solution
                if is_valid_grid(final_grid, self.words):
                    return final_grid, final_placed_info
        return None, None

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
                        solution = self._solve_recursive(remaining_words, new_grid, new_placed_info)
                        if solution:
                            return solution
        return None

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
    
    solver = BruteForceArrowwordSolver(word_list, grid_size=8)
    final_grid, placed_info = solver.solve()
    
    print("## Final Grid State (Brute-Force Solver) ##")
    print_grid(final_grid)
    
    if final_grid:
        print("\n## Placed Word Information ##")
        for info in sorted(placed_info, key=lambda x: (x['row'], x['col'])):
            print(f"- {info['word']}: ({info['row']}, {info['col']}), Direction: {info['direction']}")
