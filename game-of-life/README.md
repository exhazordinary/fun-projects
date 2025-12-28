# Conway's Game of Life

Cellular automaton where simple rules create emergent complexity. Watch patterns evolve, oscillate, and travel across the grid.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green)

## Rules

1. Live cell with 2-3 neighbors **survives**
2. Dead cell with exactly 3 neighbors **becomes alive**
3. All other cells **die** or stay dead

## Controls

| Key | Action |
|-----|--------|
| Left Click | Draw cells |
| Right Click | Erase cells |
| Space | Pause/Resume |
| R | Randomize grid |
| C | Clear grid |
| G | Toggle grid lines |
| +/- | Speed up/down |
| 1 | Load Glider |
| 2 | Load Lightweight Spaceship |
| 3 | Load Pulsar |
| 4 | Load Gosper Glider Gun |
| 5 | Load Block (still life) |
| ESC | Quit |

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python game_of_life.py
```

## Patterns

- **Glider** - Moves diagonally forever
- **Lightweight Spaceship (LWSS)** - Moves horizontally
- **Pulsar** - Period-3 oscillator
- **Gosper Glider Gun** - Emits gliders infinitely
- **Block** - 2x2 still life, never changes
