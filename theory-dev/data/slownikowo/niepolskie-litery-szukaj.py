#!/usr/bin/env python3

import sys

# List of letters to exclude
letter_list = 'aąbcćdeęfghijklłmnńoóprsśtuwzżźy-xv'

# Check if the file argument is provided
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <word_list_file>")
    sys.exit(1)

word_list_file = sys.argv[1]

try:
    # Open the word list file
    with open(word_list_file, 'r', encoding='utf-8') as file:
        # Read all lines from the file
        lines = file.readlines()

    # Iterate over each line (word)
    for line in lines:
        word = line.strip()  # Remove leading/trailing whitespace
        other_letters = [letter for letter in word if letter not in letter_list]

        # If the word contains letters other than those in the list, print it with those letters
        if other_letters:
            print(f"{word}: {', '.join(other_letters)}")

except FileNotFoundError:
    print(f"Error: File {word_list_file} not found.")
    sys.exit(1)

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
