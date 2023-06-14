#!/usr/bin/env python3

import automatic_game
import interactive_game
import sys
from words import read_words


def main(args):
    if len(args) <= 1 or args[1] not in ("interactive", "automatic"):
        print("Usage: ./main.py (interactive|automatic)")
        return

    words = read_words("five_letter_words.txt")

    if args[1] == "interactive":
        interactive_game.play(words)
    else:
        automatic_game.play(words)


if __name__ == "__main__":
    main(sys.argv)
