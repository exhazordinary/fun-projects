#!/usr/bin/env python3
"""
Terminal Tamagotchi
A pet that lives in your terminal. Feed it, play with it, watch it grow (or die).

Usage:
    python tamagotchi.py          # Interactive mode
    python tamagotchi.py status   # Check on your pet
    python tamagotchi.py feed     # Feed your pet
    python tamagotchi.py play     # Play with your pet
    python tamagotchi.py sleep    # Put your pet to sleep
    python tamagotchi.py reset    # Start over with a new pet
"""

import json
import os
import sys
import time
import random
from datetime import datetime
from pathlib import Path

# Save file location
SAVE_FILE = Path.home() / ".tamagotchi.json"

# Time decay rates (per hour)
HUNGER_RATE = 5      # Hunger increases by 5 per hour
HAPPINESS_RATE = 3   # Happiness decreases by 3 per hour
ENERGY_RATE = 2      # Energy decreases by 2 per hour

# ASCII Art
SPRITES = {
    "happy": r"""
    /\_/\
   ( ^.^ )
   (")_(")
""",
    "normal": r"""
    /\_/\
   ( o.o )
   (")_(")
""",
    "hungry": r"""
    /\_/\
   ( o.O )
   (")~(")
""",
    "sad": r"""
    /\_/\
   ( T_T )
   (")_(")
""",
    "sleeping": r"""
    /\_/\
   ( -.- ) zzZ
   (")_(")
""",
    "dead": r"""
    /\_/\
   ( x.x )
   (")_(") RIP
""",
    "excited": r"""
    /\_/\
   ( ^o^ ) !
   (")~(")
""",
}

# Status bar characters
BAR_FULL = "█"
BAR_EMPTY = "░"


def create_pet(name: str = None) -> dict:
    """Create a new pet."""
    if name is None:
        names = ["Pixel", "Byte", "Chip", "Bit", "Widget", "Nano", "Gizmo", "Spark"]
        name = random.choice(names)

    return {
        "name": name,
        "hunger": 50,
        "happiness": 50,
        "energy": 50,
        "age": 0,
        "is_sleeping": False,
        "is_alive": True,
        "created_at": datetime.now().isoformat(),
        "last_seen": datetime.now().isoformat(),
    }


def load_pet() -> dict:
    """Load pet from file, applying time decay."""
    if not SAVE_FILE.exists():
        return None

    with open(SAVE_FILE, "r") as f:
        pet = json.load(f)

    if not pet["is_alive"]:
        return pet

    # Calculate time since last interaction
    last_seen = datetime.fromisoformat(pet["last_seen"])
    now = datetime.now()
    hours_passed = (now - last_seen).total_seconds() / 3600

    # Apply time decay
    if hours_passed > 0.1:  # At least 6 minutes
        pet["hunger"] = min(100, pet["hunger"] + int(hours_passed * HUNGER_RATE))

        if not pet["is_sleeping"]:
            pet["happiness"] = max(0, pet["happiness"] - int(hours_passed * HAPPINESS_RATE))
            pet["energy"] = max(0, pet["energy"] - int(hours_passed * ENERGY_RATE))
        else:
            # Sleeping restores energy slowly
            pet["energy"] = min(100, pet["energy"] + int(hours_passed * 10))
            pet["is_sleeping"] = pet["energy"] < 100

        # Age increases
        pet["age"] += hours_passed / 24  # Age in days

        # Check for death
        if pet["hunger"] >= 100 or pet["happiness"] <= 0:
            pet["is_alive"] = False

    pet["last_seen"] = now.isoformat()
    save_pet(pet)
    return pet


def save_pet(pet: dict):
    """Save pet to file."""
    pet["last_seen"] = datetime.now().isoformat()
    with open(SAVE_FILE, "w") as f:
        json.dump(pet, f, indent=2)


def get_sprite(pet: dict) -> str:
    """Get the appropriate sprite for current pet state."""
    if not pet["is_alive"]:
        return SPRITES["dead"]
    if pet["is_sleeping"]:
        return SPRITES["sleeping"]
    if pet["hunger"] > 70:
        return SPRITES["hungry"]
    if pet["happiness"] < 30:
        return SPRITES["sad"]
    if pet["happiness"] > 80:
        return SPRITES["happy"]
    if pet["happiness"] > 60:
        return SPRITES["excited"]
    return SPRITES["normal"]


def get_mood(pet: dict) -> str:
    """Get mood description."""
    if not pet["is_alive"]:
        return "Dead... 💀"
    if pet["is_sleeping"]:
        return "Sleeping peacefully 💤"
    if pet["hunger"] > 80:
        return "Starving! 😫"
    if pet["hunger"] > 60:
        return "Very hungry 😣"
    if pet["happiness"] < 20:
        return "Miserable 😢"
    if pet["happiness"] < 40:
        return "Sad 😔"
    if pet["energy"] < 20:
        return "Exhausted 😴"
    if pet["happiness"] > 80 and pet["hunger"] < 30:
        return "Ecstatic! 🎉"
    if pet["happiness"] > 60:
        return "Happy 😊"
    return "Content 🙂"


def stat_bar(value: int, width: int = 10) -> str:
    """Create a visual stat bar."""
    filled = int(value / 100 * width)
    return BAR_FULL * filled + BAR_EMPTY * (width - filled)


def display_status(pet: dict):
    """Display pet status."""
    print("\n" + "=" * 35)
    print(f"  {pet['name']}")
    print("=" * 35)
    print(get_sprite(pet))

    print(f"  Mood: {get_mood(pet)}")
    print(f"  Age:  {pet['age']:.1f} days")
    print()

    # Invert hunger for display (low hunger = good)
    fullness = 100 - pet["hunger"]
    print(f"  Fullness:   [{stat_bar(fullness)}] {fullness}%")
    print(f"  Happiness:  [{stat_bar(pet['happiness'])}] {pet['happiness']}%")
    print(f"  Energy:     [{stat_bar(pet['energy'])}] {pet['energy']}%")
    print("=" * 35)


def feed(pet: dict) -> str:
    """Feed the pet."""
    if not pet["is_alive"]:
        return "Your pet is no longer with us... 😢"
    if pet["is_sleeping"]:
        return f"{pet['name']} is sleeping. Let them rest!"
    if pet["hunger"] <= 10:
        return f"{pet['name']} isn't hungry right now."

    pet["hunger"] = max(0, pet["hunger"] - 30)
    pet["happiness"] = min(100, pet["happiness"] + 5)
    save_pet(pet)
    return f"*munch munch* {pet['name']} enjoyed the food! 🍖"


def play(pet: dict) -> str:
    """Play with the pet."""
    if not pet["is_alive"]:
        return "Your pet is no longer with us... 😢"
    if pet["is_sleeping"]:
        return f"{pet['name']} is sleeping. Let them rest!"
    if pet["energy"] < 20:
        return f"{pet['name']} is too tired to play. Try letting them sleep!"
    if pet["hunger"] > 80:
        return f"{pet['name']} is too hungry to play. Feed them first!"

    pet["happiness"] = min(100, pet["happiness"] + 20)
    pet["energy"] = max(0, pet["energy"] - 15)
    pet["hunger"] = min(100, pet["hunger"] + 5)
    save_pet(pet)

    actions = [
        f"{pet['name']} chased their tail! 🌀",
        f"You played fetch with {pet['name']}! 🎾",
        f"{pet['name']} did a happy dance! 💃",
        f"You gave {pet['name']} belly rubs! ✨",
    ]
    return random.choice(actions)


def sleep(pet: dict) -> str:
    """Put the pet to sleep."""
    if not pet["is_alive"]:
        return "Your pet is no longer with us... 😢"
    if pet["is_sleeping"]:
        return f"{pet['name']} is already sleeping! 💤"
    if pet["energy"] > 80:
        return f"{pet['name']} isn't tired yet!"

    pet["is_sleeping"] = True
    save_pet(pet)
    return f"{pet['name']} curled up and went to sleep... 💤"


def wake(pet: dict) -> str:
    """Wake the pet up."""
    if not pet["is_alive"]:
        return "Your pet is no longer with us... 😢"
    if not pet["is_sleeping"]:
        return f"{pet['name']} is already awake!"

    pet["is_sleeping"] = False
    save_pet(pet)
    return f"{pet['name']} woke up and stretched! 🌅"


def interactive_mode(pet: dict):
    """Run interactive REPL mode."""
    print("\n🐾 Welcome to Terminal Tamagotchi!")
    print("Commands: feed, play, sleep, wake, status, help, quit\n")

    display_status(pet)

    while True:
        try:
            cmd = input("\n> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye! Take care of your pet! 👋")
            break

        if cmd in ["quit", "exit", "q"]:
            print("Goodbye! Take care of your pet! 👋")
            break
        elif cmd == "feed":
            print(feed(pet))
        elif cmd == "play":
            print(play(pet))
        elif cmd == "sleep":
            print(sleep(pet))
        elif cmd == "wake":
            print(wake(pet))
        elif cmd in ["status", "s", ""]:
            pet = load_pet()  # Reload to apply time decay
            display_status(pet)
        elif cmd == "help":
            print("""
Commands:
  feed   - Feed your pet (reduces hunger)
  play   - Play with your pet (increases happiness, costs energy)
  sleep  - Put your pet to sleep (restores energy over time)
  wake   - Wake your pet up
  status - Show current status
  quit   - Exit (your pet will persist!)
            """)
        else:
            print(f"Unknown command: {cmd}. Type 'help' for commands.")


def main():
    args = sys.argv[1:]

    # Handle reset
    if args and args[0] == "reset":
        name = args[1] if len(args) > 1 else None
        pet = create_pet(name)
        save_pet(pet)
        print(f"🐣 A new pet named {pet['name']} has been born!")
        display_status(pet)
        return

    # Load or create pet
    pet = load_pet()
    if pet is None:
        print("🐣 No pet found! Creating a new one...")
        pet = create_pet()
        save_pet(pet)
        display_status(pet)
        print("\nTip: Run with no arguments for interactive mode!")
        return

    # Handle commands
    if not args:
        interactive_mode(pet)
    elif args[0] == "status":
        display_status(pet)
    elif args[0] == "feed":
        print(feed(pet))
        display_status(pet)
    elif args[0] == "play":
        print(play(pet))
        display_status(pet)
    elif args[0] == "sleep":
        print(sleep(pet))
        display_status(pet)
    elif args[0] == "wake":
        print(wake(pet))
        display_status(pet)
    else:
        print(f"Unknown command: {args[0]}")
        print("Commands: status, feed, play, sleep, wake, reset")


if __name__ == "__main__":
    main()
