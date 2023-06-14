from list import lfilter


def get_words(filename):
    dict_file = open(filename, "r")
    words = dict_file.read().split("\n")
    return lfilter(lambda w: len(w) > 0 and w[0] != "#", words)
