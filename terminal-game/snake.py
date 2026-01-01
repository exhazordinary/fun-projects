#!/usr/bin/env python3
"""Terminal Snake Game - using curses"""

import curses
import random
import time

# Game settings
INITIAL_SPEED = 0.1
SPEED_INCREMENT = 0.005
MIN_SPEED = 0.03


def main(stdscr):
    # Setup curses
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100)

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Food
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Score
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Border

    # Get screen dimensions
    sh, sw = stdscr.getmaxyx()
    play_height = sh - 4
    play_width = sw - 2

    # Initial snake position (center of screen)
    snake = [
        (play_height // 2, play_width // 2),
        (play_height // 2, play_width // 2 - 1),
        (play_height // 2, play_width // 2 - 2),
    ]

    # Initial direction (right)
    direction = (0, 1)

    # Place first food
    food = place_food(snake, play_height, play_width)

    # Game state
    score = 0
    speed = INITIAL_SPEED
    game_over = False

    while not game_over:
        # Draw border
        stdscr.clear()
        stdscr.attron(curses.color_pair(4))
        stdscr.border()
        stdscr.attroff(curses.color_pair(4))

        # Draw score
        score_text = f" Score: {score} | Speed: {int((INITIAL_SPEED - speed + MIN_SPEED) / SPEED_INCREMENT)} "
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(0, 2, score_text)
        stdscr.attroff(curses.color_pair(3))

        # Draw food
        stdscr.attron(curses.color_pair(2))
        stdscr.addch(food[0] + 1, food[1] + 1, '*')
        stdscr.attroff(curses.color_pair(2))

        # Draw snake
        stdscr.attron(curses.color_pair(1))
        for i, (y, x) in enumerate(snake):
            char = '@' if i == 0 else 'o'
            try:
                stdscr.addch(y + 1, x + 1, char)
            except curses.error:
                pass
        stdscr.attroff(curses.color_pair(1))

        # Draw controls hint
        hint = " [Arrow keys] Move | [Q] Quit "
        stdscr.addstr(sh - 1, 2, hint)

        stdscr.refresh()

        # Get input
        key = stdscr.getch()

        # Handle input
        if key == ord('q') or key == ord('Q'):
            break
        elif key == curses.KEY_UP and direction != (1, 0):
            direction = (-1, 0)
        elif key == curses.KEY_DOWN and direction != (-1, 0):
            direction = (1, 0)
        elif key == curses.KEY_LEFT and direction != (0, 1):
            direction = (0, -1)
        elif key == curses.KEY_RIGHT and direction != (0, -1):
            direction = (0, 1)

        # Calculate new head position
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= play_height or
            new_head[1] < 0 or new_head[1] >= play_width):
            game_over = True
            continue

        # Check self collision
        if new_head in snake:
            game_over = True
            continue

        # Move snake
        snake.insert(0, new_head)

        # Check food collision
        if new_head == food:
            score += 10
            food = place_food(snake, play_height, play_width)
            # Speed up
            speed = max(MIN_SPEED, speed - SPEED_INCREMENT)
        else:
            snake.pop()

        time.sleep(speed)

    # Game over screen
    show_game_over(stdscr, score)


def place_food(snake, height, width):
    """Place food in a random empty position."""
    while True:
        food = (random.randint(0, height - 1), random.randint(0, width - 1))
        if food not in snake:
            return food


def show_game_over(stdscr, score):
    """Display game over screen."""
    sh, sw = stdscr.getmaxyx()

    stdscr.clear()

    messages = [
        "  GAME OVER  ",
        "",
        f"  Final Score: {score}  ",
        "",
        "  Press any key to exit  ",
    ]

    start_y = sh // 2 - len(messages) // 2

    for i, msg in enumerate(messages):
        x = sw // 2 - len(msg) // 2
        if i == 0:
            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
        elif i == 2:
            stdscr.attron(curses.color_pair(3))
        stdscr.addstr(start_y + i, x, msg)
        stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
        stdscr.attroff(curses.color_pair(3))

    stdscr.refresh()
    stdscr.nodelay(0)
    stdscr.getch()


if __name__ == "__main__":
    print("Starting Snake...")
    print("Use arrow keys to move, Q to quit")
    time.sleep(1)
    curses.wrapper(main)
    print("Thanks for playing!")
