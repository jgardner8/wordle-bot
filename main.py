#!/usr/bin/env python3

# from automatic_game import play  # Uncomment to collect performance stats
from interactive_game import play  # Uncomment to play interactively
from words import read_words


def main():
    words = read_words("five_letter_words.txt")
    play(words)


if __name__ == "__main__":
    main()
