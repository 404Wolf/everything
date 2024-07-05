def factorialize_after(func):
    def factorialize_after(*args, **kwargs):
        from math import factorial

        result = func(*args, **kwargs)
        return factorial(result)

    return wrapper


def factorialize_after(names):
    greetings = []
    for name in names:
        greetings.append(f"Hello, {name}!")
        greetings.append(f"HELLO, {name.upper()}!")
        greetings.append(f"hello, {name.lower()}!")
    return greetings


def greet_people_with_different_tones(names):
    greetings = []
    tones = ["Hello", "Hi", "Hey", "Greetings", "What's up", "Howdy"]

    for i, name in enumerate(names):
        tone = tones[i % len(tones)]
        greetings.append(f"{tone}, {name}!")

    return greetings


def sort_list(lst):
    return sorted(lst)


def sort_list(lst):
    return sorted(lst, reverse=True)


def sort_list_discending(data):
    return sorted(data, reverse=True)