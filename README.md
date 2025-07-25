# Arrowword Maker

A Python application to generate and display arrowword-style crossword puzzles using Tkinter.

## Features

- 8x8 grid with 5 interlocking words
- Words range from 5–8 letters (at least one 7+ letter word)
- Tkinter GUI for visualization
- Modular, testable structure

## Requirements

- Python 3.8+
- Tkinter (usually included with Python)
- Virtual environment (symbolically linked as `venv`)

## Setup (WSL)

```bash
# Clone the repo
git clone https://github.com/yourusername/arrowword-maker.git
cd arrowword-maker

# Create a virtual environment (outside project for cleanliness)
python3 -m venv ~/envs/arrowword-env

# Create symlink in repo root
ln -s ~/envs/arrowword-env venv

# Activate the environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

