def is_valid_grid(grid, word_list):
    """
    Checks if an 8x8 grid is a valid arrowword solution.

    Args:
        grid (list[list[str]]): The 8x8 grid to check.
        word_list (list[str]): The list of valid words.

    Returns:
        bool: True if the grid is valid, False otherwise.
    """
    if len(grid) != 8 or any(len(row) != 8 for row in grid):
        print("Error: Grid must be 8x8.")
        return False

    word_set = set(word_list)
    found_words = set()

    # Check horizontal words
    for r in range(8):
        row_str = "".join(grid[r])
        words_in_row = [word for word in row_str.split('.') if len(word) > 1]
        for word in words_in_row:
            if word not in word_set:
                print(f"Error: Invalid horizontal word '{word}' at row {r}.")
                return False
            found_words.add(word)

    # Check vertical words
    for c in range(8):
        col_str = "".join(grid[r][c] for r in range(8))
        words_in_col = [word for word in col_str.split('.') if len(word) > 1]
        for word in words_in_col:
            if word not in word_set:
                print(f"Error: Invalid vertical word '{word}' at column {c}.")
                return False
            found_words.add(word)

    # Check if all words from the list are in the grid
    if found_words != word_set:
        missing_words = word_set - found_words
        print(f"Error: Missing words from the word list: {missing_words}")
        return False

    return True

if __name__ == '__main__':
    # Example usage with the provided solution
    solution = [
        list('HAPPILY.'),
        list('O.O..O..'),
        list('LIT.EVIL'),
        list('I....E.E'),
        list('DONUT..G'),
        list('A.I..EYE'),
        list('YELLOW.N'),
        list('..E..END')
    ]
    word_list = ['HAPPILY', 'HOLIDAY', 'YELLOW', 'LEGEND', 'LOVE', 'EWE', 'DONUT', 'LIT', 'POT', 'EVIL', 'EYE', 'END', 'NILE']

    # A corrected word list based on the provided solution grid
    corrected_word_list = ['HAPPILY', 'HOLIDAY', 'YELLOW', 'DONUT', 'LIT', 'EVIL', 'EYE', 'END', 'LEGEND', 'NILE']

    print("Checking the provided solution with the original word list:")
    is_valid = is_valid_grid(solution, word_list)
    print(f"Is the grid valid? {is_valid}\n")

    print("Checking the provided solution with a corrected word list:")
    is_valid = is_valid_grid(solution, corrected_word_list)
    print(f"Is the grid valid? {is_valid}")
