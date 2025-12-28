# Falling Sand Simulator

A relaxing particle physics simulation. Watch sand pile up, water flow, and fire rise. Weirdly therapeutic.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green)

## Particle Types

| Particle | Behavior |
|----------|----------|
| Sand | Falls, piles up diagonally, sinks through water |
| Water | Falls, spreads horizontally, fills containers |
| Stone | Static, blocks everything |
| Fire | Rises, flickers, turns to smoke |

## Controls

| Key | Action |
|-----|--------|
| Left Click | Place particles |
| Right Click | Erase particles |
| 1 | Select Sand |
| 2 | Select Water |
| 3 | Select Stone |
| 4 | Select Fire |
| Mouse Wheel | Change brush size |
| C | Clear screen |
| Space | Pause/Resume |
| ESC | Quit |

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python falling_sand.py
```

## How It Works

The simulation uses a 2D grid where each cell can hold a particle. Every frame:

1. Iterate through particles bottom-to-top
2. Apply physics rules based on particle type
3. Render the grid

Sand and water interact realistically - sand sinks through water, water fills around obstacles.
