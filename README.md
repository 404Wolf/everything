# Literally everything!
## The ultimate abstraction.

### from everything import anything!

Real example:
```py
from everything import sort_list, stylized_greeting

# Print a greeting for Joe
print(stylized_greeting("Wolf", "Angry"))

# Sort a list
print(sort_list([3, 2, 1, 0, -5, 2.5]))
```

```cmd
>> OPENAI_API_TOKEN=...
>> python example.py
WHAT DO YOU WANT, WOLF?!
[-5, 0, 1, 2, 2.5, 3]
```

### How's it work?

Using [OpenAI's](https://openai.com)'s state-of-the-art AI technology, we can literally import anything from everything! Any function you can imagine, dynamically generated at runtime, acceptable with a simple import. 

When you `import <anything> from everything`, `dothething` will use Python's [AST](https://docs.python.org/3/library/ast.html) library to scan your source code, and find all usages of `<anything>`. It then will merge a few lines of context on both sides of every function call, along with the call itself. Then, it will use OpenAI's `gpt-4o` model to generate a Python function, which you can then use in your code.

### How to use

First, set the `OPENAI_API_TOKEN` to a valid API token. Then install the package with `pip install dothething`. Finally, import anything from everything!

### Words of caution

You **probably** don't want to use this in production. `dothething` provides no guarantees! This is my escape hatch after of 6 weeks of learning `nix`.

