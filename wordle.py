def get_words():
    dict_file = open("dictionary.txt", "r")
    words = dict_file.read().split("\n")
    return list(filter(lambda w: len(w) > 0 and w[0] != "#", words))


def main():
    words = get_words()
    print(words)


if __name__ == "__main__":
    main()
