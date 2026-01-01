# Generative Art - Flow Field

Mesmerizing visual patterns using p5.js. Particles flow through a Perlin noise field.

## Run

Just open `index.html` in a browser. No build step needed.

```bash
open index.html
# or
python3 -m http.server 8000  # then visit localhost:8000
```

## Controls

| Key | Action |
|-----|--------|
| Space | Reset canvas |
| 1 | Rainbow mode (position-based) |
| 2 | Ocean blues |
| 3 | Fire colors |
| 4 | Monochrome |
| + | Add 100 particles |
| - | Remove 100 particles |

## How It Works

1. A grid of vectors is created using Perlin noise
2. The noise evolves slowly over time (z-offset)
3. Particles follow these vectors, drawing trails
4. Colors are based on position or noise values
5. Low opacity creates layered, organic patterns

## Customization

In `sketch.js`:
- `PARTICLE_COUNT`: Initial number of particles
- `scale`: Grid resolution (smaller = more detailed)
- `zoff += 0.003`: Speed of flow field evolution
- `this.maxSpeed`: Particle velocity limit
