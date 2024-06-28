#!/usr/bin/env python3

import sys
import re

def print_next_line(pattern, file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if re.search(pattern, line):
                if i < len(lines) - 1:
                    print(lines[i + 1].strip())

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <pattern> <file_path>")
        sys.exit(1)

    pattern = sys.argv[1]
    file_path = sys.argv[2]

    print_next_line(pattern, file_path)