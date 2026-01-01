# Bad Robot Poetry Generator

Markov chains making weird poetry. Not LLMs - embrace the beautiful jank.

## How It Works

1. Reads a corpus mixing Shakespeare, Edgar Allan Poe, and cooking recipes
2. Builds a Markov chain tracking word sequences (order-2)
3. Generates poetry by randomly picking next words based on probabilities
4. Results in beautiful nonsense like:

> "the moon doth softly bake at 350 degrees
> until golden brown wherefore art thou crispy"

## Usage

```bash
python3 poetry_generator.py
```

Press Enter for more poetry, 'q' to quit.

## Sample Output

```
========================================
  Ode to a Preheated Void
========================================

  or to take arms against a sea of troubles
  gently rapping at my chamber door tis some
  simmer the ancient sorrows on low heat until
  fold gently into the void season with tears

========================================
```

## Customization

Edit the `CORPUS` variable to add your own text sources. Mix different genres for maximum chaos.
