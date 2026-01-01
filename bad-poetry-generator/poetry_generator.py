#!/usr/bin/env python3
"""Bad Robot Poetry Generator - Markov chains making weird poetry."""

from collections import defaultdict
import random
import textwrap

# Sample corpus mixing Shakespeare, Poe, and cooking recipes for maximum chaos
CORPUS = """
To be or not to be that is the question whether tis nobler in the mind
to suffer the slings and arrows of outrageous fortune or to take arms
against a sea of troubles and by opposing end them to die to sleep
no more and by a sleep to say we end the heartache and the thousand
natural shocks that flesh is heir to tis a consummation devoutly to be wished

Once upon a midnight dreary while I pondered weak and weary over many
a quaint and curious volume of forgotten lore while I nodded nearly
napping suddenly there came a tapping as of someone gently rapping
rapping at my chamber door tis some visitor I muttered tapping at my
chamber door only this and nothing more

Preheat the oven to three hundred fifty degrees and mix the flour
with butter until golden brown wherefore art thou crispy tender
flaky perfection let cool before serving with a garnish of despair
bake until the soul reaches an internal temperature of existential dread
fold gently into the void season with tears of forgotten dreams

Shall I compare thee to a summers day thou art more lovely and more
temperate rough winds do shake the darling buds of may and summers
lease hath all too short a date sometime too hot the eye of heaven shines

Quoth the raven nevermore and deep into that darkness peering long I
stood there wondering fearing doubting dreaming dreams no mortal ever
dared to dream before the silence was unbroken and the stillness gave
no token and the only word there spoken was the whispered word

Simmer the ancient sorrows on low heat until reduced by half
add a pinch of moonlight and a dash of forgotten memories stir
clockwise under the pale light of a waning crescent serve cold
with a side of eternal longing garnish with crushed hopes

The moon doth softly illuminate the kitchen where shadows dance
between the mixing bowls and measuring cups of fate whisking
the batter of destiny into peaks stiff with determination
"""


def build_chain(text, order=2):
    """Build a Markov chain from text with given order."""
    words = text.lower().split()
    chain = defaultdict(list)
    for i in range(len(words) - order):
        key = tuple(words[i:i + order])
        chain[key].append(words[i + order])
    return chain


def generate_line(chain, max_words=12):
    """Generate a single line of poetry."""
    if not chain:
        return ""
    key = random.choice(list(chain.keys()))
    output = list(key)
    for _ in range(max_words - len(key)):
        if key in chain:
            next_word = random.choice(chain[key])
            output.append(next_word)
            key = tuple(output[-len(key):])
        else:
            break
    return ' '.join(output)


def generate_poem(chain, lines=4, words_per_line=10):
    """Generate a complete poem."""
    poem_lines = []
    for _ in range(lines):
        line = generate_line(chain, words_per_line)
        poem_lines.append(line)
    return '\n'.join(poem_lines)


def format_poem(poem, title=None):
    """Format poem with title and wrapping."""
    if title is None:
        title = f"Untitled #{random.randint(1, 999)}"

    formatted = f"\n{'=' * 40}\n"
    formatted += f"  {title}\n"
    formatted += f"{'=' * 40}\n\n"

    for line in poem.split('\n'):
        wrapped = textwrap.fill(line, width=38, initial_indent='  ', subsequent_indent='    ')
        formatted += wrapped + '\n'

    formatted += f"\n{'=' * 40}\n"
    return formatted


def main():
    """Generate and display bad poetry."""
    print("\n🤖 BAD ROBOT POETRY GENERATOR 🤖")
    print("Markov chains + mixed corpus = art(?)\n")

    chain = build_chain(CORPUS, order=2)

    titles = [
        "Ode to a Preheated Void",
        "The Raven's Recipe",
        "Sonnet for a Mixing Bowl",
        "Dreams at 350 Degrees",
        "Nevermore (Serves 4)",
        "To Bake or Not to Bake",
        "Midnight in the Kitchen",
        "The Buttered Soul",
    ]

    while True:
        title = random.choice(titles)
        poem = generate_poem(chain, lines=4, words_per_line=10)
        print(format_poem(poem, title))

        choice = input("\n[Enter] for more poetry, [q] to quit: ").strip().lower()
        if choice == 'q':
            print("\n\"Quoth the oven, 'bake no more.'\"\n")
            break


if __name__ == "__main__":
    main()
