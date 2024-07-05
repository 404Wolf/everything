from everything import sort_list, stylized_greeting, is_sandwitch

# Print a greeting for Joe
print(stylized_greeting("Joe", "Angry"))

# Sort a list
print(sort_list([3, 2, 1, 0, -5, 2.5]))

# Determine if a hotdog is a sandwitch
print(
    is_sandwitch(
        name="hotdog", is_spicy=True, diameter_inches=3, is_delicious=True
    )
)

