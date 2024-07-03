import logging
logging.basicConfig(level=logging.DEBUG)

from everything import stylized_greeting, sort_list

# Print a greeting for Joe
print(stylized_greeting("Joe", "Angry"))

# Sort a list
print(sort_list([3, 2, 1, 0, -5, 2.5]))
