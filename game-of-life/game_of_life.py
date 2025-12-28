"""
Conway's Game of Life
Simple rules, emergent complexity.

Rules:
    1. Live cell with 2-3 neighbors survives
    2. Dead cell with exactly 3 neighbors becomes alive
    3. All other cells die or stay dead

Controls:
    - Left Click: Toggle cell / Draw cells
    - Right Click: Erase cells
    - Space: Pause/Resume
    - R: Randomize grid
    - C: Clear grid
    - +/-: Speed up/down
    - 1-5: Load preset patterns
    - ESC: Quit
"""

import pygame
import numpy as np
import random

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 8
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
UI_HEIGHT = 40
FPS = 60

# Colors
BACKGROUND = (15, 15, 25)
GRID_COLOR = (30, 30, 40)
CELL_COLOR = (0, 255, 136)
CELL_FADE = (0, 180, 100)
UI_BG = (25, 25, 35)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)


# Preset patterns (relative coordinates)
PATTERNS = {
    "glider": [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
    "lwss": [(0, 1), (0, 4), (1, 0), (2, 0), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3)],  # Lightweight spaceship
    "pulsar": [
        # Top-left quadrant pattern (will be mirrored)
        (0, 2), (0, 3), (0, 4), (2, 0), (3, 0), (4, 0),
        (2, 5), (3, 5), (4, 5), (5, 2), (5, 3), (5, 4),
    ],
    "glider_gun": [
        (0, 24), (1, 22), (1, 24), (2, 12), (2, 13), (2, 20), (2, 21), (2, 34), (2, 35),
        (3, 11), (3, 15), (3, 20), (3, 21), (3, 34), (3, 35), (4, 0), (4, 1), (4, 10),
        (4, 16), (4, 20), (4, 21), (5, 0), (5, 1), (5, 10), (5, 14), (5, 16), (5, 17),
        (5, 22), (5, 24), (6, 10), (6, 16), (6, 24), (7, 11), (7, 15), (8, 12), (8, 13),
    ],
    "block": [(0, 0), (0, 1), (1, 0), (1, 1)],  # Still life
}


class GameOfLife:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + UI_HEIGHT))
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        # Grid
        self.grid = np.zeros((ROWS, COLS), dtype=np.uint8)
        self.prev_grid = np.zeros((ROWS, COLS), dtype=np.uint8)

        # State
        self.running = True
        self.paused = True  # Start paused so user can set up
        self.generation = 0
        self.speed = 10  # Updates per second
        self.update_timer = 0
        self.show_grid_lines = True

    def count_neighbors(self, row: int, col: int) -> int:
        """Count live neighbors for a cell using wrapping edges."""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r = (row + dr) % ROWS
                c = (col + dc) % COLS
                count += self.grid[r, c]
        return count

    def update(self):
        """Apply Game of Life rules."""
        if self.paused:
            return

        self.update_timer += self.clock.get_time()
        update_interval = 1000 / self.speed

        if self.update_timer < update_interval:
            return

        self.update_timer = 0
        self.prev_grid = self.grid.copy()

        new_grid = np.zeros((ROWS, COLS), dtype=np.uint8)

        for row in range(ROWS):
            for col in range(COLS):
                neighbors = self.count_neighbors(row, col)
                cell = self.grid[row, col]

                if cell == 1:
                    # Live cell survives with 2-3 neighbors
                    if neighbors in [2, 3]:
                        new_grid[row, col] = 1
                else:
                    # Dead cell becomes alive with exactly 3 neighbors
                    if neighbors == 3:
                        new_grid[row, col] = 1

        self.grid = new_grid
        self.generation += 1

    def randomize(self, density: float = 0.15):
        """Randomly populate the grid."""
        self.grid = np.random.choice([0, 1], size=(ROWS, COLS), p=[1 - density, density]).astype(np.uint8)
        self.generation = 0

    def clear(self):
        """Clear all cells."""
        self.grid = np.zeros((ROWS, COLS), dtype=np.uint8)
        self.generation = 0

    def place_pattern(self, pattern_name: str, center_row: int = None, center_col: int = None):
        """Place a preset pattern on the grid."""
        if pattern_name not in PATTERNS:
            return

        pattern = PATTERNS[pattern_name]

        # Default to center of grid
        if center_row is None:
            center_row = ROWS // 2
        if center_col is None:
            center_col = COLS // 2

        # Special handling for pulsar (needs 4-way symmetry)
        if pattern_name == "pulsar":
            for dr, dc in pattern:
                for r_mult in [-1, 1]:
                    for c_mult in [-1, 1]:
                        r = (center_row + dr * r_mult) % ROWS
                        c = (center_col + dc * c_mult) % COLS
                        self.grid[r, c] = 1
        else:
            for dr, dc in pattern:
                r = (center_row + dr) % ROWS
                c = (center_col + dc) % COLS
                self.grid[r, c] = 1

    def toggle_cell(self, mouse_pos: tuple, value: int = None):
        """Toggle or set a cell at mouse position."""
        mx, my = mouse_pos
        if my >= HEIGHT:
            return

        col = mx // CELL_SIZE
        row = my // CELL_SIZE

        if 0 <= row < ROWS and 0 <= col < COLS:
            if value is not None:
                self.grid[row, col] = value
            else:
                self.grid[row, col] = 1 - self.grid[row, col]

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.randomize()
                elif event.key == pygame.K_c:
                    self.clear()
                elif event.key == pygame.K_g:
                    self.show_grid_lines = not self.show_grid_lines
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    self.speed = min(60, self.speed + 2)
                elif event.key == pygame.K_MINUS:
                    self.speed = max(1, self.speed - 2)
                elif event.key == pygame.K_1:
                    self.clear()
                    self.place_pattern("glider")
                elif event.key == pygame.K_2:
                    self.clear()
                    self.place_pattern("lwss")
                elif event.key == pygame.K_3:
                    self.clear()
                    self.place_pattern("pulsar")
                elif event.key == pygame.K_4:
                    self.clear()
                    self.place_pattern("glider_gun")
                elif event.key == pygame.K_5:
                    self.clear()
                    self.place_pattern("block")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.toggle_cell(event.pos)

        # Handle continuous mouse drawing
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] or mouse_buttons[2]:
            mouse_pos = pygame.mouse.get_pos()
            value = 1 if mouse_buttons[0] else 0
            self.toggle_cell(mouse_pos, value)

    def render(self):
        """Render the simulation."""
        self.screen.fill(BACKGROUND)

        # Draw grid lines
        if self.show_grid_lines:
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y))

        # Draw cells
        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row, col]:
                    rect = pygame.Rect(
                        col * CELL_SIZE + 1,
                        row * CELL_SIZE + 1,
                        CELL_SIZE - 1,
                        CELL_SIZE - 1
                    )
                    pygame.draw.rect(self.screen, CELL_COLOR, rect)

        # Draw UI bar
        pygame.draw.rect(self.screen, UI_BG, (0, HEIGHT, WIDTH, UI_HEIGHT))

        # Status text
        status = "PAUSED - Click to draw, Space to start" if self.paused else "RUNNING"
        status_color = (255, 200, 100) if self.paused else CELL_COLOR
        status_text = self.font.render(status, True, status_color)
        self.screen.blit(status_text, (10, HEIGHT + 12))

        # Generation counter
        gen_text = self.font.render(f"Gen: {self.generation}", True, WHITE)
        self.screen.blit(gen_text, (WIDTH // 2 - 40, HEIGHT + 12))

        # Speed indicator
        speed_text = self.font.render(f"Speed: {self.speed}", True, GRAY)
        self.screen.blit(speed_text, (WIDTH // 2 + 50, HEIGHT + 12))

        # Population count
        pop = np.sum(self.grid)
        pop_text = self.font.render(f"Pop: {pop}", True, GRAY)
        self.screen.blit(pop_text, (WIDTH - 100, HEIGHT + 12))

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        print("Conway's Game of Life")
        print("=" * 30)
        print("Controls:")
        print("  Left Click  - Draw cells")
        print("  Right Click - Erase cells")
        print("  Space       - Pause/Resume")
        print("  R           - Randomize")
        print("  C           - Clear")
        print("  +/-         - Speed up/down")
        print("  G           - Toggle grid lines")
        print("  1-5         - Load patterns:")
        print("    1: Glider")
        print("    2: Lightweight Spaceship")
        print("    3: Pulsar")
        print("    4: Gosper Glider Gun")
        print("    5: Block (still life)")
        print("  ESC         - Quit")
        print("=" * 30)

        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife()
    game.run()
