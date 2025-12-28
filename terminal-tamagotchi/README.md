# Terminal Tamagotchi

A virtual pet that lives in your terminal. Feed it, play with it, watch it grow (or die).

## Features

- Persistent state saved to `~/.tamagotchi.json`
- Time decay - hunger increases while you're away!
- ASCII art expressions
- Interactive REPL or one-shot commands

## Usage

```bash
# Interactive mode
python tamagotchi.py

# One-shot commands
python tamagotchi.py status
python tamagotchi.py feed
python tamagotchi.py play
python tamagotchi.py sleep

# Start over
python tamagotchi.py reset
python tamagotchi.py reset "Fluffy"  # Custom name
```

## Stats

| Stat | Description |
|------|-------------|
| Fullness | Decreases over time, feed to restore |
| Happiness | Decreases when neglected, play to restore |
| Energy | Spent when playing, sleep to restore |

## What Happens When You're Away

- Hunger increases (~5% per hour)
- Happiness decreases (~3% per hour)
- Energy decreases (~2% per hour)
- If sleeping, energy slowly restores instead

## Death

Your pet dies if:
- Hunger reaches 100%
- Happiness reaches 0%

Take care of your pet!
