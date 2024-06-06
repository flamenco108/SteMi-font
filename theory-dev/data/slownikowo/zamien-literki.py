#!/usr/bin/env python3

import sys

# Check if the required arguments are provided
if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <file> <chars_to_replace> <replacement_chars>")
    sys.exit(1)

file_path = sys.argv[1]
chars_to_replace = list(sys.argv[2])
replacement_chars = list(sys.argv[3])

try:
    # Read the contents of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace the specified characters with the replacement characters
    translation_table = str.maketrans(''.join(chars_to_replace), ''.join(replacement_chars))
    new_content = content.translate(translation_table)

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

    print(f"The characters '{', '.join(chars_to_replace)}' have been replaced with '{', '.join(replacement_chars)}' in {file_path}.")

except FileNotFoundError:
    print(f"Error: File {file_path} not found.")
    sys.exit(1)

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
