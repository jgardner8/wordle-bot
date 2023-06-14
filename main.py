from game import game_loop
from words import get_words


def main():
    words = get_words()
    game_loop(words)


if __name__ == "__main__":
    main()
