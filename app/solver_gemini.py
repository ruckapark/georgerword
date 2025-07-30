import collections

class ArrowwordSolver:
    """
    A greedy algorithm to fill an arrowword grid with a given set of words.
    """

    def __init__(self, words, grid_size=8):
        self.words = sorted(words, key=len, reverse=True)
        self.grid_size = grid_size
        self.grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
        self.placed_words = []
        self.unplaced_words = collections.deque(self.words)

    def solve(self):
        """
        Attempts to solve the arrowword puzzle.
        Returns:
            tuple: The completed grid and a list of placed word details, or None if it fails.
        """
        if not self._place_first_word():
            return None, None

        while self.unplaced_words:
            word_to_place = self.unplaced_words.popleft()
            
            found_placement = False
            # Find the first valid intersection point for the current word
            for r in range(self.grid_size):
                for c in range(self.grid_size):
                    if self.grid[r][c] != '':
                        # Try to find an intersection with the letter at (r,c)
                        for i, char in enumerate(word_to_place):
                            if char == self.grid[r][c]:
                                # Try placing horizontally
                                if self._is_valid_placement(word_to_place, r, c - i, 'H'):
                                    self._place_word(word_to_place, r, c - i, 'H')
                                    found_placement = True
                                    break
                                # Try placing vertically
                                if self._is_valid_placement(word_to_place, r - i, c, 'V'):
                                    self._place_word(word_to_place, r - i, c, 'V')
                                    found_placement = True
                                    break
                        if found_placement:
                            break
                if found_placement:
                    break
            
            if not found_placement:
                # If a word can't be placed, the solution fails. Add it back and stop.
                self.unplaced_words.appendleft(word_to_place)
                print(f"Error: Could not find a valid placement for '{word_to_place}'")
                return None, None
                
        return self.grid, self.placed_words

    def _place_first_word(self):
        """Places the longest word in the center of the grid."""
        if not self.unplaced_words:
            return False
        
        first_word = self.unplaced_words.popleft()
        start_row = self.grid_size // 2
        start_col = (self.grid_size - len(first_word)) // 2
        
        if self._is_valid_placement(first_word, start_row, start_col, 'H'):
            self._place_word(first_word, start_row, start_col, 'H')
            return True
        return False

    def _is_valid_placement(self, word, r, c, direction):
        """Checks if a word can be placed at a given position and direction."""
        if direction == 'H':
            # Check grid boundaries
            if c < 0 or c + len(word) > self.grid_size:
                return False
            
            # Check for conflicts with existing letters and adjacency rules
            for i in range(len(word)):
                char_on_grid = self.grid[r][c + i]
                # If the cell is not empty, it must match the word's character
                if char_on_grid != '' and char_on_grid != word[i]:
                    return False
                # If the cell is empty, check its vertical neighbors
                if char_on_grid == '':
                    if r > 0 and self.grid[r - 1][c + i] != '':
                        return False # Word above
                    if r < self.grid_size - 1 and self.grid[r + 1][c + i] != '':
                        return False # Word below

            # Check that the ends of the word are not attached to other words
            if c > 0 and self.grid[r][c - 1] != '':
                return False
            if c + len(word) < self.grid_size and self.grid[r][c + len(word)] != '':
                return False

        elif direction == 'V':
            # Check grid boundaries
            if r < 0 or r + len(word) > self.grid_size:
                return False
            
            # Check for conflicts with existing letters and adjacency rules
            for i in range(len(word)):
                char_on_grid = self.grid[r + i][c]
                if char_on_grid != '' and char_on_grid != word[i]:
                    return False
                if char_on_grid == '':
                    if c > 0 and self.grid[r + i][c - 1] != '':
                        return False # Word to the left
                    if c < self.grid_size - 1 and self.grid[r + i][c + 1] != '':
                        return False # Word to the right
            
            # Check that the ends of the word are not attached to other words
            if r > 0 and self.grid[r - 1][c] != '':
                return False
            if r + len(word) < self.grid_size and self.grid[r + len(word)][c] != '':
                return False
        
        return True

    def _place_word(self, word, r, c, direction):
        """Places a word on the grid and records its position."""
        if direction == 'H':
            for i in range(len(word)):
                self.grid[r][c + i] = word[i]
        elif direction == 'V':
            for i in range(len(word)):
                self.grid[r + i][c] = word[i]
        
        self.placed_words.append({
            'word': word,
            'row': r,
            'col': c,
            'direction': direction
        })

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
    
    print("## Final Grid State ##")
    print_grid(final_grid)
    
    print("\n## Placed Word Information ##")
    if placed_info:
        for info in placed_info:
            print(f"- {info['word']}: ({info['row']}, {info['col']}), Direction: {info['direction']}")

    print('The actual solution is \n')
    solution = solution = [list('HAPPILY.'),list('O.O..O..'),list('LIT.EVIL'),list('I....E.E'),list('DONUT..G'),list('A.I..EYE'),list('YELLOW.N'),list('..E..END')]
    for row in solution:
        print(''.join(row))