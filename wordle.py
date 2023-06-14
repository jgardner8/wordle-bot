from dataclasses import dataclass
from typing import List
from list import find, flatMap, flatten, lfilter, lmap


@dataclass
class Match:
    char: str
    index: int
    index_matched: bool  # if true, index is correct index of char (green), otherwise it's known incorrect index (orange)


@dataclass
class Guess:
    word: str
    matches: List[Match]


@dataclass
class Knowledge:
    non_matches: str
    incorrect_index_matches: List[Match]
    known_structure: List[str]


def get_words():
    dict_file = open("dictionary.txt", "r")
    words = dict_file.read().split("\n")
    return lfilter(lambda w: len(w) > 0 and w[0] != "#", words)


def generate_known_structure(matches):
    index_matches = lfilter(lambda m: m.index_matched, matches)
    matches_by_char = map(
        lambda i: find(lambda m: m.index == i, index_matches), range(0, 5)
    )
    return lmap(lambda m: getattr(m, "char", None), matches_by_char)


def collate_knowledge(guesses):
    guessed_chars = flatMap(lambda g: g.word, guesses)
    matches = flatMap(lambda g: g.matches, guesses)
    non_matches = lfilter(
        lambda c: c not in lmap(lambda m: m.char, matches), guessed_chars
    )

    incorrect_index_matches = lfilter(lambda m: not m.index_matched, matches)

    index_matches = lfilter(lambda m: m.index_matched, matches)
    known_structure = generate_known_structure(index_matches)

    return Knowledge(non_matches, incorrect_index_matches, known_structure)


def find_eligible_words(words, knowledge):
    # Grey boxes
    words_without_non_matches = lfilter(
        lambda w: not any([char in w for char in knowledge.non_matches]), words
    )
    # Green boxes
    words_with_index_matches = lfilter(
        lambda w: all(
            [c == None or w[i] == c for i, c in enumerate(knowledge.known_structure)]
        ),
        words_without_non_matches,
    )
    # Orange boxes
    words_with_incorrect_index_matches = lfilter(
        lambda w: all(
            [w[m.index] != m.char for m in knowledge.incorrect_index_matches]
        ),
        words_with_index_matches,
    )
    return words_with_incorrect_index_matches


def next_guess(eligible_words):
    chars = flatten(eligible_words)
    occurrences = {char: len(lfilter(lambda c: c == char, chars)) for char in chars}
    scores = {
        word: sum([occurrences[char] for char in set(word)]) for word in eligible_words
    }
    sorted_scores = sorted(scores.items(), key=lambda kvp: kvp[1], reverse=True)
    return sorted_scores[0][0]


def main():
    words = get_words()
    guesses = [Guess("louse", [Match("e", 4, True)])]
    knowledge = collate_knowledge(guesses)
    eligible_words = find_eligible_words(words, knowledge)
    print(next_guess(eligible_words))


if __name__ == "__main__":
    main()
