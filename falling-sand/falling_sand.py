"""
Falling Sand Simulator
A relaxing particle simulation with sand, water, stone, and fire.

Controls:
    - Left Click: Place particles
    - Right Click: Erase particles
    - 1: Select Sand
    - 2: Select Water
    - 3: Select Stone
    - 4: Select Fire
    - Mouse Wheel: Change brush size
    - C: Clear screen
    - Space: Pause/Resume
    - ESC: Quit
"""

import pygame
import random
from enum import Enum
from dataclasses import dataclass

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 4
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
FPS = 60

# Colors
BACKGROUND = (20, 20, 30)
UI_BG = (40, 40, 50)
WHITE = (255, 255, 255)


class ParticleType(Enum):
    EMPTY = 0
    SAND = 1
    WATER = 2
    STONE = 3
    FIRE = 4
    SMOKE = 5


@dataclass
class Particle:
    type: ParticleType
    color: tuple
    updated: bool = False
    lifetime: int = -1  # -1 means infinite


def get_particle_color(ptype: ParticleType) -> tuple:
    """Get a slightly randomized color for each particle type."""
    if ptype == ParticleType.SAND:
        base = (194, 178, 128)
        variation = random.randint(-20, 20)
        return (base[0] + variation, base[1] + variation, base[2])
    elif ptype == ParticleType.WATER:
        base = (30, 144, 255)
        variation = random.randint(-20, 20)
        return (base[0], base[1] + variation, min(255, base[2] + variation))
    elif ptype == ParticleType.STONE:
        base = (128, 128, 128)
        variation = random.randint(-30, 30)
        return (base[0] + variation, base[1] + variation, base[2] + variation)
    elif ptype == ParticleType.FIRE:
        return (255, random.randint(100, 200), 0)
    elif ptype == ParticleType.SMOKE:
        gray = random.randint(80, 120)
        return (gray, gray, gray)
    return BACKGROUND


def create_particle(ptype: ParticleType) -> Particle:
    """Create a new particle of the given type."""
    lifetime = -1
    if ptype == ParticleType.FIRE:
        lifetime = random.randint(30, 90)
    elif ptype == ParticleType.SMOKE:
        lifetime = random.randint(60, 120)
    return Particle(
        type=ptype,
        color=get_particle_color(ptype),
        updated=False,
        lifetime=lifetime
    )


class FallingSand:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))
        pygame.display.set_caption("Falling Sand Simulator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        # Grid
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

        # State
        self.running = True
        self.paused = False
        self.selected_type = ParticleType.SAND
        self.brush_size = 3
        self.particle_count = 0

    def in_bounds(self, row: int, col: int) -> bool:
        """Check if coordinates are within grid bounds."""
        return 0 <= row < ROWS and 0 <= col < COLS

    def is_empty(self, row: int, col: int) -> bool:
        """Check if a cell is empty."""
        return self.in_bounds(row, col) and self.grid[row][col] is None

    def swap(self, r1: int, c1: int, r2: int, c2: int):
        """Swap two cells."""
        self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]

    def update_sand(self, row: int, col: int):
        """Update sand particle physics."""
        particle = self.grid[row][col]

        # Try to fall straight down
        if self.is_empty(row + 1, col):
            self.swap(row, col, row + 1, col)
            return

        # Try to fall into water below
        if self.in_bounds(row + 1, col):
            below = self.grid[row + 1][col]
            if below and below.type == ParticleType.WATER:
                self.swap(row, col, row + 1, col)
                return

        # Try diagonal movement (randomly choose left or right first)
        directions = [-1, 1]
        random.shuffle(directions)

        for dx in directions:
            new_col = col + dx
            if self.is_empty(row + 1, new_col):
                self.swap(row, col, row + 1, new_col)
                return
            # Slide through water diagonally
            if self.in_bounds(row + 1, new_col):
                diag = self.grid[row + 1][new_col]
                if diag and diag.type == ParticleType.WATER:
                    self.swap(row, col, row + 1, new_col)
                    return

    def update_water(self, row: int, col: int):
        """Update water particle physics."""
        particle = self.grid[row][col]

        # Try to fall straight down
        if self.is_empty(row + 1, col):
            self.swap(row, col, row + 1, col)
            return

        # Try diagonal down
        directions = [-1, 1]
        random.shuffle(directions)

        for dx in directions:
            if self.is_empty(row + 1, col + dx):
                self.swap(row, col, row + 1, col + dx)
                return

        # Spread horizontally
        spread_distance = random.randint(1, 3)
        for dx in directions:
            if self.is_empty(row, col + dx):
                self.swap(row, col, row, col + dx)
                return

    def update_fire(self, row: int, col: int):
        """Update fire particle physics."""
        particle = self.grid[row][col]

        # Decrease lifetime
        particle.lifetime -= 1
        if particle.lifetime <= 0:
            # Turn into smoke
            if random.random() < 0.5:
                self.grid[row][col] = create_particle(ParticleType.SMOKE)
            else:
                self.grid[row][col] = None
            return

        # Fire flickers and rises
        if random.random() < 0.3:
            particle.color = (255, random.randint(100, 200), random.randint(0, 50))

        # Rise upward
        if random.random() < 0.6:
            directions = [0, -1, 1]
            random.shuffle(directions)

            for dx in directions:
                if self.is_empty(row - 1, col + dx):
                    self.swap(row, col, row - 1, col + dx)
                    return

        # Spread fire to nearby flammable things (currently nothing is flammable)
        # Can be extended to burn other particle types

    def update_smoke(self, row: int, col: int):
        """Update smoke particle physics."""
        particle = self.grid[row][col]

        # Decrease lifetime
        particle.lifetime -= 1
        if particle.lifetime <= 0:
            self.grid[row][col] = None
            return

        # Fade color
        gray = max(40, particle.color[0] - 1)
        particle.color = (gray, gray, gray)

        # Rise and drift
        if random.random() < 0.4:
            directions = [0, -1, 1]
            random.shuffle(directions)

            for dx in directions:
                if self.is_empty(row - 1, col + dx):
                    self.swap(row, col, row - 1, col + dx)
                    return

    def update_particles(self):
        """Update all particles in the grid."""
        if self.paused:
            return

        # Reset update flags
        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col]:
                    self.grid[row][col].updated = False

        # Update bottom to top for falling particles
        for row in range(ROWS - 1, -1, -1):
            # Randomly iterate left-to-right or right-to-left for natural flow
            cols = list(range(COLS))
            if random.random() < 0.5:
                cols.reverse()

            for col in cols:
                particle = self.grid[row][col]
                if particle is None or particle.updated:
                    continue

                particle.updated = True

                if particle.type == ParticleType.SAND:
                    self.update_sand(row, col)
                elif particle.type == ParticleType.WATER:
                    self.update_water(row, col)
                elif particle.type == ParticleType.FIRE:
                    self.update_fire(row, col)
                elif particle.type == ParticleType.SMOKE:
                    self.update_smoke(row, col)
                # Stone doesn't move

    def place_particles(self, mouse_pos: tuple, erase: bool = False):
        """Place or erase particles at mouse position."""
        mx, my = mouse_pos

        # Only place in the grid area (not UI)
        if my >= HEIGHT:
            return

        col = mx // CELL_SIZE
        row = my // CELL_SIZE

        # Place in a brush-sized area
        for dr in range(-self.brush_size, self.brush_size + 1):
            for dc in range(-self.brush_size, self.brush_size + 1):
                # Circular brush
                if dr * dr + dc * dc <= self.brush_size * self.brush_size:
                    r, c = row + dr, col + dc
                    if self.in_bounds(r, c):
                        if erase:
                            self.grid[r][c] = None
                        elif self.grid[r][c] is None:
                            # Add some randomness to placement
                            if random.random() < 0.7:
                                self.grid[r][c] = create_particle(self.selected_type)

    def clear_grid(self):
        """Clear all particles from the grid."""
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

    def count_particles(self) -> int:
        """Count total particles in the grid."""
        count = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col]:
                    count += 1
        return count

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_1:
                    self.selected_type = ParticleType.SAND
                elif event.key == pygame.K_2:
                    self.selected_type = ParticleType.WATER
                elif event.key == pygame.K_3:
                    self.selected_type = ParticleType.STONE
                elif event.key == pygame.K_4:
                    self.selected_type = ParticleType.FIRE
                elif event.key == pygame.K_c:
                    self.clear_grid()
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused

            elif event.type == pygame.MOUSEWHEEL:
                self.brush_size = max(1, min(10, self.brush_size + event.y))

        # Handle continuous mouse input
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] or mouse_buttons[2]:
            mouse_pos = pygame.mouse.get_pos()
            self.place_particles(mouse_pos, erase=mouse_buttons[2])

    def render(self):
        """Render the simulation."""
        # Clear screen
        self.screen.fill(BACKGROUND)

        # Draw particles
        for row in range(ROWS):
            for col in range(COLS):
                particle = self.grid[row][col]
                if particle:
                    rect = pygame.Rect(
                        col * CELL_SIZE,
                        row * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                    pygame.draw.rect(self.screen, particle.color, rect)

        # Draw UI bar
        pygame.draw.rect(self.screen, UI_BG, (0, HEIGHT, WIDTH, 50))

        # Draw particle type buttons
        types = [
            (ParticleType.SAND, "1:Sand", (194, 178, 128)),
            (ParticleType.WATER, "2:Water", (30, 144, 255)),
            (ParticleType.STONE, "3:Stone", (128, 128, 128)),
            (ParticleType.FIRE, "4:Fire", (255, 150, 0)),
        ]

        x_offset = 10
        for ptype, label, color in types:
            # Highlight selected
            if self.selected_type == ptype:
                pygame.draw.rect(self.screen, WHITE, (x_offset - 2, HEIGHT + 8, 74, 34), 2)

            pygame.draw.rect(self.screen, color, (x_offset, HEIGHT + 10, 70, 30))
            text = self.font.render(label, True, WHITE if ptype != ParticleType.SAND else (40, 40, 40))
            self.screen.blit(text, (x_offset + 5, HEIGHT + 16))
            x_offset += 80

        # Draw brush size
        brush_text = self.font.render(f"Brush: {self.brush_size}", True, WHITE)
        self.screen.blit(brush_text, (x_offset + 20, HEIGHT + 16))

        # Draw particle count
        self.particle_count = self.count_particles()
        count_text = self.font.render(f"Particles: {self.particle_count}", True, WHITE)
        self.screen.blit(count_text, (x_offset + 120, HEIGHT + 16))

        # Draw pause indicator
        if self.paused:
            pause_text = self.font.render("PAUSED", True, (255, 100, 100))
            self.screen.blit(pause_text, (WIDTH - 80, HEIGHT + 16))

        # Draw FPS
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, WHITE)
        self.screen.blit(fps_text, (WIDTH - 80, HEIGHT + 32))

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        print("Falling Sand Simulator")
        print("=" * 30)
        print("Controls:")
        print("  Left Click  - Place particles")
        print("  Right Click - Erase particles")
        print("  1/2/3/4     - Select Sand/Water/Stone/Fire")
        print("  Mouse Wheel - Change brush size")
        print("  C           - Clear screen")
        print("  Space       - Pause/Resume")
        print("  ESC         - Quit")
        print("=" * 30)

        while self.running:
            self.handle_events()
            self.update_particles()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = FallingSand()
    game.run()
