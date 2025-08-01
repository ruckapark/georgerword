class FinalArrowwordSolverV2:
    """
    A greedy solver for arrowword puzzles based on the user's instructions.
    This solver follows a deterministic algorithm:
    1. Sort words by length in descending order.
    2. Place the longest word on the board.
    3. Iterate through the remaining words, attempting to place each one.
    4. For each word, find all possible intersection points with words already on the board.
    5. For each potential placement, validate it against strict crossword rules (no parallel words touching, no letter conflicts).
    6. Use the first valid placement found and move to the next word.
    7. Words that cannot be placed are skipped and recorded.
    This is a greedy, non-backtracking approach.
    """

    def __init__(self, words, grid_size=15):
        # 1. Sort all the words by length, descending.
        self.words = sorted(words, key=len, reverse=True)
        self.grid_size = grid_size
        self.grid = [['' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.placed_words_info = []
        self.unplaced_words = []

    def solve(self):
        """
        Attempts to solve the arrowword puzzle using the greedy intersection-based approach.
        """
        if not self.words:
            return None, None

        # 2. Take the first word and place it on the board.
        # We place it horizontally near the center for a good starting point.
        first_word = self.words[0]
        r = self.grid_size // 2
        c = (self.grid_size - len(first_word)) // 2
        if c < 0: c = 0  # Handle words longer than the grid is wide.
        
        self._place_word_on_grid(first_word, r, c, 'H')
        self.placed_words_info.append({'word': first_word, 'row': r, 'col': c, 'direction': 'H'})

        words_to_place = self.words[1:]

        # 7. Continue this loop until all the words are either placed or unable to be placed.
        for word in words_to_place:
            # 3. Take the next word and try to place it.
            self._try_to_place_word(word)

        return self.grid, self.placed_words_info

    def _try_to_place_word(self, word):
        """
        Finds the first valid placement for a word and places it. If no placement is found,
        the word is added to the unplaced list.
        """
        # 4. Search through all the words that are already on the board for possible intersections.
        possible_placements = self._find_possible_placements(word)

        for placement in possible_placements:
            # 5. If there is a possible location, check if it interferes with other words.
            if self._is_valid_placement(word, placement['row'], placement['col'], placement['direction'], self.grid):
                # 6. If this word doesn't break the board, then place it there and go to the next word.
                self._place_word_on_grid(word, placement['row'], placement['col'], placement['direction'])
                self.placed_words_info.append(placement)
                return  # Word placed successfully, exit.

        # If the loop completes, no valid placement was found.
        self.unplaced_words.append(word)

    def _find_possible_placements(self, word_to_place):
        """
        Generates a list of potential placements by finding all common letters
        between the word to place and the words already on the grid.
        """
        placements = []
        for placed_info in self.placed_words_info:
            placed_word = placed_info['word']
            for i, char_to_place in enumerate(word_to_place):
                for j, placed_char in enumerate(placed_word):
                    if char_to_place == placed_char:
                        # Found a common letter, which is a potential intersection.
                        if placed_info['direction'] == 'H':
                            # The existing word is horizontal, so the new word must be vertical.
                            r = placed_info['row'] - i
                            c = placed_info['col'] + j
                            placements.append({'word': word_to_place, 'row': r, 'col': c, 'direction': 'V'})
                        else:  # The existing word is vertical.
                            # The new word must be horizontal.
                            r = placed_info['row'] + j
                            c = placed_info['col'] - i
                            placements.append({'word': word_to_place, 'row': r, 'col': c, 'direction': 'H'})
        return placements

    def _is_valid_placement(self, word, r, c, direction, grid):
        """
        Checks if a word can be placed at a given position and direction
        with strict crossword rules (no conflicts, no parallel neighbors).
        """
        if direction == 'H':
            if c < 0 or c + len(word) > self.grid_size: return False
            # Check word boundaries (must have empty cells or grid edge).
            if c > 0 and grid[r][c - 1] != '': return False
            if c + len(word) < self.grid_size and grid[r][c + len(word)] != '': return False

            for i in range(len(word)):
                char_on_grid = grid[r][c + i]
                if char_on_grid == word[i]:
                    continue  # This is the intersection point, which is allowed.
                elif char_on_grid != '':
                    return False  # Conflict with an existing letter.
                else:  # This is an empty cell, check for parallel words.
                    if r > 0 and grid[r - 1][c + i] != '': return False
                    if r < self.grid_size - 1 and grid[r + 1][c + i] != '': return False
        
        elif direction == 'V':
            if r < 0 or r + len(word) > self.grid_size: return False
            # Check word boundaries.
            if r > 0 and grid[r - 1][c] != '': return False
            if r + len(word) < self.grid_size and grid[r + len(word)][c] != '': return False

            for i in range(len(word)):
                char_on_grid = grid[r + i][c]
                if char_on_grid == word[i]:
                    continue  # Intersection point is allowed.
                elif char_on_grid != '':
                    return False  # Conflict.
                else:  # Empty cell, check for parallel words.
                    if c > 0 and grid[r + i][c - 1] != '': return False
                    if c < self.grid_size - 1 and grid[r + i][c + 1] != '': return False
        else:
            return False

        return True

    def _place_word_on_grid(self, word, r, c, direction):
        """Places a word's letters onto the main grid."""
        if direction == 'H':
            for i in range(len(word)):
                self.grid[r][c + i] = word[i]
        elif direction == 'V':
            for i in range(len(word)):
                self.grid[r + i][c] = word[i]

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
    
    # Using a larger grid as this greedy method might need more space to succeed.
    solver = FinalArrowwordSolverV2(word_list, grid_size=15)
    final_grid, placed_info = solver.solve()
    
    print("## Final Grid State (Greedy Intersection Solver) ##")
    print_grid(final_grid)
    
    if final_grid:
        print("\n## Placed Word Information ##")
        for info in sorted(placed_info, key=lambda x: (x['row'], x['col'])):
            print(f"- {info['word']}: ({info['row']}, {info['col']}), Direction: {info['direction']}")
        
        unplaced = solver.unplaced_words
        if unplaced:
            print("\n## Words that could not be placed ##")
            print(sorted(unplaced))
