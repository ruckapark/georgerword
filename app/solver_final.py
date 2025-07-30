import collections

class FinalArrowwordSolver:
    """
    A robust backtracking solver for arrowword puzzles.
    """

    def __init__(self, words, grid_size=8):
        self.words = sorted(words, key=len, reverse=True)
        self.grid_size = grid_size

    def solve(self):
        """
        Attempts to solve the arrowword puzzle using backtracking.
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
        is_first_word = not placed_words_info

        # Iterate through all possible placements
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                for direction in ['H', 'V']:
                    if self._is_valid_placement(word_to_place, r, c, direction, grid, is_first_word):
                        new_grid = self._place_word(grid, word_to_place, r, c, direction)
                        new_placed_info = placed_words_info + [{'word': word_to_place, 'row': r, 'col': c, 'direction': direction}]
                        
                        solution_grid, solution_info = self._solve_recursive(remaining_words, new_grid, new_placed_info)
                        if solution_grid:
                            return solution_grid, solution_info
        
        return None, None

    def _is_valid_placement(self, word, r, c, direction, grid, is_first_word=False):
        """Checks if a word can be placed at a given position and direction with strict crossword rules."""
        has_intersection = False
        # print(f'Checking {word} at ({r}, {c}) {direction}') # Debug
        
        if direction == 'H':
            if c < 0 or c + len(word) > self.grid_size: return False
            # Check word boundaries (must have empty cells or grid edge)
            if c > 0 and grid[r][c - 1] != '': return False
            if c + len(word) < self.grid_size and grid[r][c + len(word)] != '': return False

            for i in range(len(word)):
                char_on_grid = grid[r][c + i]
                if char_on_grid == word[i]:
                    has_intersection = True
                elif char_on_grid != '':
                    # print(f'  Conflict at ({r}, {c+i}): grid has {char_on_grid}, word has {word[i]}') # Debug
                    return False # Conflict with existing letter
                else: # Empty cell, check adjacent cells
                    if r > 0 and grid[r - 1][c + i] != '': return False
                    if r < self.grid_size - 1 and grid[r + 1][c + i] != '': return False
        
        elif direction == 'V':
            if r < 0 or r + len(word) > self.grid_size: return False
            # Check word boundaries
            if r > 0 and grid[r - 1][c] != '': return False
            if r + len(word) < self.grid_size and grid[r + len(word)][c] != '': return False

            for i in range(len(word)):
                char_on_grid = grid[r + i][c]
                if char_on_grid == word[i]:
                    has_intersection = True
                elif char_on_grid != '':
                    # print(f'  Conflict at ({r+i}, {c}): grid has {char_on_grid}, word has {word[i]}') # Debug
                    return False # Conflict
                else: # Empty cell, check adjacent cells
                    if c > 0 and grid[r + i][c - 1] != '': return False
                    if c < self.grid_size - 1 and grid[r + i][c + 1] != '': return False
        else:
            return False

        return is_first_word or has_intersection

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

def verify_solution(grid, word_list):
    """Extracts all words from the grid and verifies them against the word list."""
    if not grid:
        return False
    
    found_words = set()
    # Check horizontal words
    for r in range(len(grid)):
        row_str = "".join(grid[r]).replace('', ' ')
        words_in_row = [word for word in row_str.split(' ') if len(word) > 1]
        for word in words_in_row:
            found_words.add(word)

    # Check vertical words
    for c in range(len(grid[0])):
        col_str = "".join(grid[r][c] for r in range(len(grid))).replace('', ' ')
        words_in_col = [word for word in col_str.split(' ') if len(word) > 1]
        for word in words_in_col:
            found_words.add(word)
    
    input_word_set = set(word_list)
    
    print("\n--- Verification ---")
    print(f"Words in grid:  {sorted(list(found_words))}")
    print(f"Words in input: {sorted(list(input_word_set))}")

    if found_words == input_word_set:
        print("\nSuccess: The grid is a valid solution.")
        return True
    else:
        print("\nError: The grid is not a valid solution.")
        print(f"Missing from grid: {sorted(list(input_word_set - found_words))}")
        print(f"Extra in grid: {sorted(list(found_words - input_word_set))}")
        return False

# --- Main Execution ---
if __name__ == "__main__":
    word_list = ['HAPPILY', 'HOLIDAY', 'YELLOW', 'LEGEND', 'LOVE', 'EWE', 'DONUT', 'LIT', 'POT', 'EVIL', 'EYE', 'END', 'NILE']
    
    solver = FinalArrowwordSolver(word_list, grid_size=8)
    final_grid, placed_info = solver.solve()
    
    print("## Final Grid State (Final Solver) ##")
    print_grid(final_grid)
    
    if final_grid:
        print("\n## Placed Word Information ##")
        for info in sorted(placed_info, key=lambda x: (x['row'], x['col'])):
            print(f"- {info['word']}: ({info['row']}, {info['col']}), Direction: {info['direction']}")
        verify_solution(final_grid, word_list)
