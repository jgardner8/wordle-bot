import ai_player
from game_data import Guess, Match


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
        print("Letter", i + 1, "matched? (g=green, y=yellow, n=grey)")
        feedback = input()
        if feedback not in ["g", "y", "n"]:
            continue
        elif feedback in ["g", "y"]:
            matches.append(Match(guess_str[i], i, index_matched=feedback == "g"))
        i += 1

    return matches


def game_loop(words):
    guesses = []
    for turn_number in range(1, 7):
        if _is_game_won(guesses):
            print("Winner winner, chicken dinner!")
            break

        print("Turn", turn_number)
        print("------------")

        guess_str = ai_player.next_guess(words, guesses)
        if guess_str == None:
            print("Oops, the word is not in words.txt :(")
        else:
            matches = _ask_user_for_matches(guess_str)
            guesses.append(Guess(guess_str, matches))
            print("")
