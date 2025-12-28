# Falling Sand Simulator

## What
Particles fall, pile up, interact. Like Noita but simpler. Weirdly therapeutic.

## Particle Types
- **Sand**: Falls, piles up diagonally
- **Water**: Flows sideways, fills containers
- **Stone**: Static, blocks everything
- **Fire**: Rises, burns stuff (optional)

## Logic
```
For each particle (bottom to top):
  - Sand: if below empty, fall. else slide diagonally
  - Water: fall, or spread sideways
  - Stone: do nothing
```

## Tech Options
- **Pygame**: Best for this, easy pixel manipulation
- **HTML Canvas**: Also works well
- **Terminal**: Possible but limited

## Structure
```
1. Create 2D grid
2. Mouse click = place particles
3. Each frame:
   - Iterate bottom-to-top, left-to-right
   - Apply physics rules
   - Render
```

## Starter
```python
import pygame
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 4
grid = [[None for _ in range(WIDTH//CELL_SIZE)] for _ in range(HEIGHT//CELL_SIZE)]
```

## Complexity
~100-150 lines for basic version
