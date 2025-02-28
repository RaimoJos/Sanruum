# Jokes, Quotes & Fun Facts
from __future__ import annotations

import random

FACTS = [
    'Honey never spoils.',
    'Octopuses have three hearts.',
    "Bananas are berries, but strawberries aren't."
    'A day in venus is longer than its year.',
]


def tell_joke() -> None:
    """Tells a random joke."""
    pass


def get_famous_quote() -> None:
    """Returns a random famous quote."""
    pass


def get_motivational_quote() -> None:
    """Returns a motivational quote to inspire the user."""
    pass


def get_riddle() -> None:
    """Provides a random riddle and its answer."""
    pass


def get_trivia_question() -> None:
    """Provides a random trivia question and possible answers."""
    pass


def get_random_fact() -> str:
    """Returns a random interesting fact."""
    return random.choice(FACTS)


def get_lucky_number() -> int:
    """Generates a random lucky number between 1 and 100."""
    return random.randint(1, 100)
