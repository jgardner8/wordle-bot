import time
import ai_player
from game_data import Guess, Match
from list import find


def _is_game_won(guesses):
    return (
        len(guesses) > 0
        and len(guesses[-1].matches) == 5
        and all([m.index_matched for m in guesses[-1].matches])
    )


def _ask_user_for_matches(guess_str):
    print("Guess:", guess_str)

    matches = []
    i = 0
    while i < 5:
        print("Letter", i + 1, "matched? (g=green, y=yellow, n=grey) ", end="")
        feedback = input()
        if feedback not in ["g", "y", "n"]:
            continue
        elif feedback in ["g", "y"]:
            matches.append(Match(guess_str[i], i, index_matched=feedback == "g"))
        i += 1

    return matches


def _print_guess_grid(guesses):
    def print_char(c):
        print(c, end="", flush="True")
        time.sleep(0.1)

    for guess_idx in range(0, len(guesses)):
        print_char(guess_idx + 1)
        print_char(":")
        print_char(" ")

        for char_idx in range(0, 5):
            match = find(lambda m: m.index == char_idx, guesses[guess_idx].matches)
            if match:
                if match.index_matched:
                    print_char("g")
                else:
                    print_char("y")
            else:
                print_char(" ")

        print("")

    print("")


def game_loop(words):
    guesses = []
    for turn_number in range(1, 7):
        if _is_game_won(guesses):
            print("Winner winner, chicken dinner!")
            _print_guess_grid(guesses)
            break

        print("Turn", turn_number)
        print("------------")

        guess_str = ai_player.next_guess(words, guesses)
        if guess_str == None:
            print("Oops, the word is not in words.txt :(")
            _print_guess_grid(guesses)
            break
        else:
            matches = _ask_user_for_matches(guess_str)
            guesses.append(Guess(guess_str, matches))
            print("")
