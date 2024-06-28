#!/usr/bin/env python3

import re
import sys

def replace_string(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        pattern = r'StartChar: ([a-z]+).brh.([0-9]+).([0-9]+)'
        replacement = r'StartChar: brh.\1.\2.\3'
        new_content = re.sub(pattern, replacement, content)

        with open(file_path, 'w') as file:
            file.write(new_content)

        print(f"String replacement completed successfully in {file_path}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    replace_string(file_path)
