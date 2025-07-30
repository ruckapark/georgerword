import collections
import itertools

class ArrowwordSolver:
    """
    A backtracking algorithm to fill an arrowword grid with a given set of words.
    This version finds the best possible solution, even if it means omitting some words.
    """

    def __init__(self, words, grid_size=8):
        self.words = sorted(words, key=len, reverse=True) # Sort for better heuristic
        self.grid_size = grid_size

    def solve(self):
        """
        Attempts to solve the arrowword puzzle by finding the best possible solution,
        even if it means omitting some words.
        """
        initial_grid = [['' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        for i in range(len(self.words), 0, -1):
            for word_subset in itertools.combinations(self.words, i):
                grid, placed_info = self._solve_recursive(list(word_subset), initial_grid, [])
                if grid:
                    return grid, placed_info
        return None, None

    def _get_next_word_and_placements(self, unplaced_words, grid, is_first_word):
        """
        Determines the best word to place next based on the number of valid placements (minimum first).
        """
        if is_first_word:
            first_word = unplaced_words[0]
            # Place the first word at (0,0) horizontally
            if self._is_valid_placement(first_word, 0, 0, 'H', grid, True):
                return first_word, [(0, 0, 'H')]
            else:
                return None, []


        candidate_words = []
        for word in unplaced_words:
            placements = self._find_all_valid_placements(word, grid)
            valid_placements = [p for p in placements if self._is_valid_placement(word, p[0], p[1], p[2], grid, False)]
            
            if not valid_placements:
                # If any word has zero valid placements, this path is invalid.
                return None, []
                
            candidate_words.append((word, valid_placements))

        if not candidate_words:
            return None, []

        # Sort by the number of valid placements, ascending
        candidate_words.sort(key=lambda x: len(x[1]))
        
        return candidate_words[0]


    def _solve_recursive(self, unplaced_words, grid, placed_words_info):
        """
        The main recursive function that tries to place words using a heuristic.
        """
        if not unplaced_words:
            return grid, placed_words_info

        is_first_word = not placed_words_info
        
        # Find the best word to place next
        word_to_place, placements = self._get_next_word_and_placements(unplaced_words, grid, is_first_word)
        
        if not word_to_place:
            return None, None

        new_unplaced_words = [w for w in unplaced_words if w != word_to_place]

        for r, c, direction in placements:
            new_grid = self._place_word(grid, word_to_place, r, c, direction)
            new_placed_info = placed_words_info + [{'word': word_to_place, 'row': r, 'col': c, 'direction': direction}]
            
            solution_grid, solution_info = self._solve_recursive(new_unplaced_words, new_grid, new_placed_info)
            if solution_grid:
                return solution_grid, solution_info
        
        return None, None

    def _find_all_valid_placements(self, word, grid):
        """Finds all geometrically possible placements for a word based on intersections."""
        placements = []
        for r_intersect in range(self.grid_size):
            for c_intersect in range(self.grid_size):
                if grid[r_intersect][c_intersect] != '':
                    for i, char in enumerate(word):
                        if char == grid[r_intersect][c_intersect]:
                            # Try placing horizontally
                            placements.append((r_intersect, c_intersect - i, 'H'))
                            # Try placing vertically
                            placements.append((r_intersect - i, c_intersect, 'V'))
        return list(set(placements)) # Remove duplicates

    def _is_valid_placement(self, word, r, c, direction, grid, is_first_word=False):
        """Checks if a word can be placed at a given position and direction."""
        has_intersection = False
        
        if direction == 'H':
            if c < 0 or c + len(word) > self.grid_size: return False
            for i in range(len(word)):
                char_on_grid = grid[r][c + i]
                if char_on_grid != '' and char_on_grid != word[i]: return False
                if char_on_grid == word[i]: has_intersection = True
                if char_on_grid == '':
                    if r > 0 and grid[r - 1][c + i] != '': return False
                    if r < self.grid_size - 1 and grid[r + 1][c + i] != '': return False
            if c > 0 and grid[r][c - 1] != '': return False
            if c + len(word) < self.grid_size and grid[r][c + len(word)] != '': return False
        
        elif direction == 'V':
            if r < 0 or r + len(word) > self.grid_size: return False
            for i in range(len(word)):
                char_on_grid = grid[r + i][c]
                if char_on_grid != '' and char_on_grid != word[i]: return False
                if char_on_grid == word[i]: has_intersection = True
                if char_on_grid == '':
                    if c > 0 and grid[r + i][c - 1] != '': return False
                    if c < self.grid_size - 1 and grid[r + i][c + 1] != '': return False
            if r > 0 and grid[r - 1][c] != '': return False
            if r + len(word) < self.grid_size and grid[r + len(word)][c] != '': return False
        
        else: # Invalid direction
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

# --- Main Execution ---
if __name__ == "__main__":
    word_list = ['HAPPILY', 'HOLIDAY', 'YELLOW', 'LEGEND', 'LOVE', 'EWE', 'DONUT', 'LIT', 'POT', 'EVIL', 'EYE', 'END', 'NILE']
    
    solver = ArrowwordSolver(word_list, grid_size=8)
    final_grid, placed_info = solver.solve()
    
    print("## Final Grid State (Best Effort) ##")
    print_grid(final_grid)
    
    print("\n## Placed Word Information ##")
    if placed_info:
        placed_words = {info['word'] for info in placed_info}
        for info in sorted(placed_info, key=lambda x: x['word']):
            print(f"- {info['word']}: ({info['row']}, {info['col']}), Direction: {info['direction']}")
        
        unplaced_words = set(word_list) - placed_words
        if unplaced_words:
            print(f"\nWords not placed: {sorted(list(unplaced_words))}")

    print('The actual solution is ')
    solution = [list('HAPPILY.'),list('O.O..O..'),list('LIT.EVIL'),list('I....E.E'),list('DONUT..G'),list('A.I..EYE'),list('YELLOW.N'),list('..E..END')]
    for row in solution:
        print(''.join(row))