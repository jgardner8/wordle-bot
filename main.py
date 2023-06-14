#!/usr/bin/env python3

# from interactive_game import play # Uncomment to play interactively
from automatic_game import play  # Uncomment to make the computer play itself
from words import get_words


def main():
    words = get_words("words.txt")
    play(words)


if __name__ == "__main__":
    main()
