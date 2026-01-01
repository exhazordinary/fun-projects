# Useless Machine - Anti-Todo App

A todo list that defeats its own purpose. Pure comedy.

## Run

```bash
python3 anti_todo.py
```

## How It Works

Every action backfires:

| Action | Expected | Reality |
|--------|----------|---------|
| Add task | Task is added | A random existing task is deleted |
| Complete task | Task marked done | Two new absurd tasks appear |
| Delete task | Task removed | All tasks marked incomplete |
| Clear all | List emptied | Everything duplicates |

## Sample Session

```
> add Buy groceries
  Added: 'Buy groceries'
  (Don't worry, this won't last)

> add Walk the dog
  Added: 'Walk the dog'
  ...but accidentally deleted: 'Buy groceries'
  Net progress: 0

> complete 0
  Completed: 'Walk the dog'
  ...but this spawned: 'Alphabetize your anxieties'
  ...but this spawned: 'Debug your life choices'
  Net progress: -1
```

## The Philosophy

This is a meditation on futility, wrapped in a CLI. Every attempt to organize creates more chaos. The only winning move is not to play.

Or maybe it's just funny. You decide.
