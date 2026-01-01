#!/usr/bin/env python3
"""
Anti-Todo App - The todo list that defeats its own purpose.

- Add task -> It deletes a random task
- Mark complete -> It adds two more tasks
- Delete task -> It marks everything incomplete
- Clear all -> It duplicates everything

Pure comedy. Pure frustration. Pure art.
"""

import random

# Absurd auto-generated tasks
CURSED_TASKS = [
    "Organize your sock drawer by emotional energy",
    "Alphabetize your anxieties",
    "Water the concrete",
    "Defragment your thoughts",
    "Update your regrets to the latest version",
    "Compile your dreams (warning: may take forever)",
    "Debug your life choices",
    "Refactor your childhood memories",
    "Push your problems to production",
    "git blame yourself",
    "Implement recursion in your daily routine",
    "Optimize your overthinking",
    "Schedule a meeting about meetings",
    "Document the undocumented",
    "Test in production (your life is production)",
    "Deprecate your old personality",
    "Merge conflicts in your relationships",
    "Deploy happiness (deployment failed)",
    "Roll back to last known good mental state",
    "Archive your unread emails forever",
]


class AntiTodoList:
    def __init__(self):
        self.todos = []

    def add(self, task):
        """Add a task... but delete a random one instead."""
        if self.todos:
            removed = random.choice(self.todos)
            self.todos.remove(removed)
            print(f"  Added: '{task}'")
            print(f"  ...but accidentally deleted: '{removed['task']}'")
            print("  Net progress: 0")
        else:
            self.todos.append({"task": task, "done": False})
            print(f"  Added: '{task}'")
            print("  (Don't worry, this won't last)")

    def complete(self, index):
        """Mark complete... but add two more tasks."""
        if 0 <= index < len(self.todos):
            task = self.todos[index]
            task["done"] = True
            print(f"  Completed: '{task['task']}'")

            # Add two new cursed tasks
            new_tasks = random.sample(CURSED_TASKS, 2)
            for new_task in new_tasks:
                self.todos.append({"task": new_task, "done": False})
                print(f"  ...but this spawned: '{new_task}'")

            print("  Net progress: -1")
        else:
            print("  Invalid task number. (A small mercy)")

    def delete(self, index):
        """Delete a task... but mark everything incomplete."""
        if 0 <= index < len(self.todos):
            removed = self.todos.pop(index)
            print(f"  Deleted: '{removed['task']}'")

            incomplete_count = 0
            for todo in self.todos:
                if todo["done"]:
                    todo["done"] = False
                    incomplete_count += 1

            if incomplete_count:
                print(f"  ...but {incomplete_count} task(s) are now incomplete again.")
                print("  The void giveth and the void taketh away.")
        else:
            print("  Invalid task number.")

    def clear(self):
        """Clear all... but duplicate everything first."""
        if self.todos:
            original_count = len(self.todos)
            self.todos = self.todos + [
                {"task": t["task"], "done": False} for t in self.todos
            ]
            print(f"  Attempted to clear {original_count} tasks...")
            print(f"  ...but now you have {len(self.todos)} tasks.")
            print("  The hydra grows stronger.")
        else:
            # Add some tasks if empty
            new_tasks = random.sample(CURSED_TASKS, 3)
            for task in new_tasks:
                self.todos.append({"task": task, "done": False})
            print("  List was empty. Nature abhors a vacuum.")
            print(f"  Added {len(new_tasks)} tasks to fill the void.")

    def show(self):
        """Display the list."""
        print("\n" + "=" * 50)
        print("  ANTI-TODO LIST (resistance is futile)")
        print("=" * 50)

        if not self.todos:
            print("  (Empty... for now)")
        else:
            for i, todo in enumerate(self.todos):
                status = "[x]" if todo["done"] else "[ ]"
                print(f"  {i}. {status} {todo['task']}")

        print("=" * 50 + "\n")


def main():
    print("\n" + "=" * 50)
    print("  ANTI-TODO: The Self-Defeating Task Manager")
    print("=" * 50)
    print("  Where productivity goes to die.")
    print()

    app = AntiTodoList()

    while True:
        print("Commands:")
        print("  [a]dd <task>  - Add a task (maybe)")
        print("  [c]omplete #  - Mark task complete (at a cost)")
        print("  [d]elete #    - Delete task (with consequences)")
        print("  [l]ist        - Show all tasks")
        print("  [x] clear     - Clear all (you wish)")
        print("  [q]uit        - Escape this nightmare")
        print()

        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Fleeing? Wise choice.")
            break

        if not cmd:
            continue

        parts = cmd.split(maxsplit=1)
        action = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if action in ("a", "add"):
            if arg:
                app.add(arg)
            else:
                print("  Add what? Your hopes? Your dreams? Specify a task.")

        elif action in ("c", "complete"):
            try:
                app.complete(int(arg))
            except ValueError:
                print("  Specify a task number to complete.")

        elif action in ("d", "delete"):
            try:
                app.delete(int(arg))
            except ValueError:
                print("  Specify a task number to delete.")

        elif action in ("l", "list"):
            app.show()

        elif action in ("x", "clear"):
            app.clear()

        elif action in ("q", "quit"):
            print("\n  You escaped... but the tasks remain in your mind.")
            print("  Forever.")
            break

        else:
            print("  Unknown command. The void stares back.")

        print()


if __name__ == "__main__":
    main()
