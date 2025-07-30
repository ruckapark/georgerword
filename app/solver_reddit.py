from bisect import bisect_left

# Fill a NxN crossword using a dictionary of words of length N.
# Prints solution, and then waits until you hit Enter to try to find the next one.
def make_crosswords(N, word_list):
  for soln in fill(N, sorted([w for w in word_list if len(w) == N]), []):
    for row in soln:
      print(row)
    input()

def fill(N, words, crossword):
  for col in range(N):
    if not could_place_vertical_word(words, crossword, col):
      return # Dead end
  if len(crossword) == N: 
    # Full, do final validity check
    if len(set(get_col(crossword, i) for i in range(N))) < N: return # Invalid
    yield crossword # Valid!
  for w in words:
    if w in crossword: continue # already placed
    crossword.append(w)
    yield from fill(N, words, crossword)
    crossword.pop()

def get_col(crossword, col):
  return ''.join(w[col] for w in crossword)

def could_place_vertical_word(words, crossword, col):
  # The letters in this column so far
  prefix = get_col(crossword, col)
  # Just like you would in a dictionary, find the prefix and scan forward
  for i in range(bisect_left(words, prefix), len(words)):
    if words[i] in crossword: continue # already placed
    if not words[i].startswith(prefix): break # passed the section for this prefix
    return True
  return False