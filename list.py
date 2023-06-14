def flatten(list):
    return [item for sublist in list for item in sublist]


def flatMap(f, xs):
    return flatten(map(f, xs))


def lfilter(f, xs):
    return list(filter(f, xs))


def lmap(f, xs):
    return list(map(f, xs))


def find(predicate, xs):
    return next((x for x in xs if predicate(x)), None)
