# Data definitions for game.py. Avoids circular import.

from dataclasses import dataclass
from typing import List


@dataclass(eq=True, frozen=True)
class Match:
    char: str
    index: int
    index_matched: bool  # if true, index is correct index of char (green), otherwise it's known incorrect index (yellow)


@dataclass(eq=True, frozen=True)
class Guess:
    word: str
    matches: List[Match]
