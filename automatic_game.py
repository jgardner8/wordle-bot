import ai_player
import statistics
from game import Guess, Match
from list import find, lfilter, lmap
from words import get_words


def _calculate_matches(word_to_guess, guess_str):
    matches = []
    for i, c in enumerate(guess_str):
        if c in word_to_guess:
            matches.append(
                Match(guess_str[i], i, index_matched=word_to_guess[i] == guess_str[i])
            )

    return matches


def play_game(words, word_to_guess):
    guesses = []
    for turn_number in range(1, 100):
        guess_str = ai_player.next_guess(words, guesses)
        if guess_str == word_to_guess:
            return turn_number
        elif guess_str == None:
            raise AssertionError(f"{word_to_guess} is not in words.txt")
        else:
            matches = _calculate_matches(word_to_guess, guess_str)
            guesses.append(Guess(guess_str, matches))

    raise AssertionError(f"Couldn't guess {word_to_guess} within iteration limit")


def play(words):
    past_answers = get_words("past_answers.txt")

    stats = []
    for word_to_guess in past_answers:
        turns_taken = play_game(words, word_to_guess)
        stats.append((word_to_guess, turns_taken))

    turns_taken_data = lmap(lambda s: s[1], stats)
    print("Games played:", len(turns_taken_data))
    print("Games won:", len(lfilter(lambda n: n <= 6, turns_taken_data)))
    print("Games lost:", len(lfilter(lambda n: n > 6, turns_taken_data)))
    print("Min turns:", min(turns_taken_data))
    print("Max turns:", max(turns_taken_data))
    print("Mean turns:", statistics.mean(turns_taken_data))
    print("Median turns:", statistics.median(turns_taken_data))

    games_lost = lfilter(lambda x: x[1] > 6, stats)
    games_lost_str = [f"{x[0]} took {x[1]} turns" for x in games_lost]
    print("Words lost on:")
    for s in games_lost_str:
        print(f"\t{s}")
