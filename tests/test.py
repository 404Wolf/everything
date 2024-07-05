import everything
from everything import sort_list

print(everything.sort_list_discending([12, 5, 6, 3, 22]))
print(sort_list([12, 5, 6, 3, 22]))


def adder(a, b):
    return a + b


# Makes a function that changes a function to do a factorial afterwards
new_func = everything.factorialize_after(adder)
print(new_func(3, 4))

print(everything.greet_people_with_different_tones(["bob", "joe", "sally"]))
