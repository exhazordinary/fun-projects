# Ray Marching

Render 3D scenes with just math. No meshes, no models - pure signed distance functions.

## Scenes

| Key | Scene |
|-----|-------|
| 1 | Floating spheres with soft shadows |
| 2 | Infinite repeating boxes + spheres |
| 3 | Morphing shape (sphere → box → octahedron → torus) |
| 4 | Wormhole tunnel |
| 5 | Fractal Menger sponge |

## Controls

| Input | Action |
|-------|--------|
| Mouse | Look around |
| 1-5 | Switch scenes |
| Space | Pause time |

## Run

Just open `index.html` in your browser.

```bash
open index.html
```

## How It Works

1. Cast a ray from camera through each pixel
2. "March" along the ray in steps
3. At each step, evaluate distance to nearest surface (SDF)
4. Step forward by that distance
5. Repeat until hit or max distance
6. Calculate lighting and color

## Signed Distance Functions

```glsl
// Sphere
float sdSphere(vec3 p, float r) {
    return length(p) - r;
}

// Box
float sdBox(vec3 p, vec3 b) {
    vec3 d = abs(p) - b;
    return length(max(d, 0.0));
}

// Combine shapes
min(a, b)  // Union
max(a, b)  // Intersection
max(a, -b) // Subtraction
```

## Cool Techniques Used

- Smooth minimum for organic blending
- Infinite repetition with `mod()`
- Soft shadows
- Fresnel effect
- Domain rotation for animation
