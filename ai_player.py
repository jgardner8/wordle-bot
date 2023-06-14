from dataclasses import dataclass
from typing import List
from game import Match
from list import find, flatMap, flatten, lfilter, lmap


@dataclass(eq=True, frozen=True)
class _Knowledge:
    non_matches: str
    incorrect_index_matches: List[Match]
    known_structure: List[str]


def _generate_known_structure(matches):
    index_matches = lfilter(lambda m: m.index_matched, matches)
    matches_by_char = map(
        lambda i: find(lambda m: m.index == i, index_matches), range(0, 5)
    )
    return lmap(lambda m: getattr(m, "char", None), matches_by_char)


def _collate_knowledge(guesses):
    guessed_chars = flatMap(lambda g: g.word, guesses)
    matches = set(flatMap(lambda g: g.matches, guesses))
    non_matches = lfilter(
        lambda c: c not in lmap(lambda m: m.char, matches), guessed_chars
    )

    incorrect_index_matches = lfilter(lambda m: not m.index_matched, matches)

    index_matches = lfilter(lambda m: m.index_matched, matches)
    known_structure = _generate_known_structure(index_matches)

    return _Knowledge(non_matches, incorrect_index_matches, known_structure)


def _find_eligible_words(words, knowledge):
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
    # Yellow boxes
    words_without_incorrect_index_matches = lfilter(
        lambda w: all(
            [
                w[m.index] != m.char and m.char in w
                for m in knowledge.incorrect_index_matches
            ]
        ),
        words_with_index_matches,
    )
    return words_without_incorrect_index_matches


def _print_reasoning(knowledge, occurrences, sorted_scores):
    print("Reasoning:")
    print("\tLetters not present (grey):", ", ".join(knowledge.non_matches))
    print(
        "\tLetters in known positions (green):",
        " ".join([c if c else "_" for c in knowledge.known_structure]),
    )

    print("\tLetters present, but not in positions (yellow):")
    incorrect_index_match_info = {
        m.char: lmap(
            lambda m2: str(m2.index + 1),
            filter(lambda m2: m2.char == m.char, knowledge.incorrect_index_matches),
        )
        for m in knowledge.incorrect_index_matches
    }
    incorrect_index_match_strs = [
        f"{char} not in positions: {', '.join(sorted(incorrect_index_match_info[char]))}"
        for char in sorted(incorrect_index_match_info.keys())
    ]
    for s in incorrect_index_match_strs:
        print(f"\t\t{s}")

    print(
        "\tLetter occurrences in eligible words:",
        sorted(occurrences.items(), key=lambda kvp: kvp[1], reverse=True),
    )
    print("\tTop 5 guesses:", sorted_scores[:5])
    print("")


def next_guess(words, guesses, silent_mode=True):
    if len(guesses) == 0:
        return "alert"  # optimisation: this is what it would calculate every time with no knowledge

    knowledge = _collate_knowledge(guesses)
    eligible_words = _find_eligible_words(words, knowledge)
    chars = flatten(eligible_words)
    occurrences = {char: len(lfilter(lambda c: c == char, chars)) for char in chars}
    scores = {
        word: sum([occurrences[char] for char in set(word)]) for word in eligible_words
    }
    sorted_scores = sorted(scores.items(), key=lambda kvp: kvp[1], reverse=True)

    if not silent_mode:
        _print_reasoning(knowledge, occurrences, sorted_scores)

    if len(sorted_scores) == 0:
        return None
    else:
        return sorted_scores[0][0]
