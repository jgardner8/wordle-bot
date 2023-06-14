from dataclasses import dataclass
from typing import List


@dataclass
class Match:
    letter: str
    position: int
    positionMatched: bool  # if true, position is correct index of letter, otherwise it's known incorrect position


@dataclass
class Guess:
    word: str
    matches: List[Match]


def get_words():
    dict_file = open("dictionary.txt", "r")
    words = dict_file.read().split("\n")
    return list(filter(lambda w: len(w) > 0 and w[0] != "#", words))


def main():
    words = get_words()
    guesses = [Guess("louse", [Match("e", 4, True)])]


if __name__ == "__main__":
    main()
