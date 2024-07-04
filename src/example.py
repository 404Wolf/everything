module_name = "everything"

mod = __import__(module_name)
all_attrs = {name: getattr(mod, name) for name in dir(mod) if not name.startswith("_")}

# Optionally update globals with these attributes
globals().update(all_attrs)

from everything import sort_list, stylized_greeting

# Print a greeting for Joe
print(stylized_greeting("Joe", "Angry"))

# Sort a list
print(sort_list([3, 2, 1, 0, -5, 2.5]))
