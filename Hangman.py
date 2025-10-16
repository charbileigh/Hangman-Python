# hangman.py
import random
import string
import sys
from pathlib import Path

HANGMANPICS = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """
]

# -------- word loading --------
def load_words(filename: str = "words.txt"):
    """
    Load words from a text file. Accepts words separated by spaces, commas, or newlines.
    Keeps only alphabetic tokens and lowercases them. Removes duplicates.
    Falls back to a small built-in list if the file doesn't exist or yields no words.
    """
    fallback = [
        "python", "testing", "function", "variable", "agile",
        "project", "refactor", "engineer", "compile", "interface"
    ]

    path = Path(filename)
    if not path.exists():
        print(f"⚠️  File '{filename}' not found. Using default list.")
        return fallback

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"⚠️  Couldn't read '{filename}' ({e}). Using default list.")
        return fallback

    # allow commas/newlines/spaces as separators
    tokens = content.replace(",", " ").split()
    words = sorted({t.strip().lower() for t in tokens if t.isalpha()})

    if not words:
        print(f"⚠️  No valid words found in '{filename}'. Using default list.")
        return fallback

    print(f"📚 Loaded {len(words)} words from '{filename}'.")
    return words

def choose_word(words):
    return random.choice(words)

# -------- game helpers --------
def masked_word(secret, guessed):
    return " ".join([ch if ch in guessed else "_" for ch in secret])

def get_guess(already):
    while True:
        g = input("Guess a letter: ").strip().lower()
        if len(g) != 1:
            print("Please enter exactly one character.")
            continue
        if g not in string.ascii_lowercase:
            print("Letters only (a-z).")
            continue
        if g in already:
            print(f"You already guessed '{g}'. Try a different letter.")
            continue
        return g

def play_one_round(secret):
    lives = len(HANGMANPICS) - 1
    guessed = set()
    wrong = set()

    print("\nLet's play Hangman!")
    while True:
        print(HANGMANPICS[len(wrong)])
        print("Word:   ", masked_word(secret, guessed))
        if wrong:
            print("Wrong:  ", " ".join(sorted(wrong)))
        print(f"Lives:   {lives - len(wrong)}")

        # win?
        if all(ch in guessed for ch in secret):
            print(f"\n🎉 You guessed it! The word was: {secret}")
            return True

        # lose?
        if len(wrong) >= lives:
            print(f"\n💀 Out of lives! The word was: {secret}")
            return False

        g = get_guess(guessed | wrong)
        if g in secret:
            guessed.add(g)
            print(f"Nice! '{g}' is in the word.\n")
        else:
            wrong.add(g)
            print(f"Oops! '{g}' is not in the word.\n")

# -------- entry point --------
def main():
    print("=== Hangman (Python CLI) ===")
    # Usage: python hangman.py my_words.txt
    words_file = sys.argv[1] if len(sys.argv) > 1 else "words.txt"
    words = load_words(words_file)

    while True:
        secret = choose_word(words)
        play_one_round(secret)

        again = input("\nPlay again? (y/n): ").strip().lower()
        if not again or again[0] != "y":
            print("Thanks for playing! 👋")
            break

if __name__ == "__main__":
    main()
