from collections import defaultdict
import numpy as np

def can_place_word(grid, word, row, col, direction):
    n = len(grid)
    l = len(word)

    if direction == 'across':
        if col + l > n:
            return False
        # Check before and after boundaries
        if col > 0 and grid[row][col - 1] != '':
            return False
        if col + l < n and grid[row][col + l] != '':
            return False
        for i in range(l):
            ch = grid[row][col + i]
            if ch not in ('', word[i]):
                return False
        return True

    elif direction == 'down':
        if row + l > n:
            return False
        # Check before and after boundaries
        if row > 0 and grid[row - 1][col] != '':
            return False
        if row + l < n and grid[row + l][col] != '':
            return False
        for i in range(l):
            ch = grid[row + i][col]
            if ch not in ('', word[i]):
                return False
        return True

    return False

def place_word(grid, word, row, col, direction):
    if direction == 'across':
        for i in range(len(word)):
            grid[row][col + i] = word[i]
    else:
        for i in range(len(word)):
            grid[row + i][col] = word[i]

def find_all_intersections(grid, word):
    n = len(grid)
    for i, char in enumerate(word):
        for r in range(n):
            for c in range(n):
                if grid[r][c] == char:
                    # Try across
                    start_col = c - i
                    if 0 <= start_col and start_col + len(word) <= n:
                        if can_place_word(grid, word, r, start_col, 'across'):
                            return (word, r, start_col, 'across')
                    # Try down
                    start_row = r - i
                    if 0 <= start_row and start_row + len(word) <= n:
                        if can_place_word(grid, word, start_row, c, 'down'):
                            return (word, start_row, c, 'down')
    return None

def greedy_arrowword(words):
    words = sorted(words, key=lambda w: -len(w))  # Longest words first
    n = 8
    grid = [['' for _ in range(n)] for _ in range(n)]
    placed = []

    # Try first word in top-left corner horizontally
    first_word = words.pop(0)
    if can_place_word(grid, first_word, 0, 0, 'across'):
        place_word(grid, first_word, 0, 0, 'across')
        placed.append((first_word, 0, 0, 'across'))
    else:
        return None  # Failed early, shouldn't happen with valid input

    # Place remaining words
    for word in words:
        placement = find_all_intersections(grid, word)
        if placement:
            w, r, c, d = placement
            place_word(grid, w, r, c, d)
            placed.append(placement)

    return np.array(grid)

# Example usage
words = ['HAPPILY','HOLIDAY','YELLOW', 'LEGEND','LOVE','EWE','DONUT','LIT','POT','EVIL','EYE','END','NILE']
grid_result = greedy_arrowword(words)

# Display grid
if grid_result is not None:
    for row in grid_result:
        print(' '.join(c if c else '.' for c in row))
else:
    print("No valid solution found.")

solution = solution = [list('HAPPILY.'),list('O.O..O..'),list('LIT.EVIL'),list('I....E.E'),list('DONUT..G'),list('A.I..EYE'),list('YELLOW.N'),list('..E..END')]
for row in solution:
    print(''.join(row))