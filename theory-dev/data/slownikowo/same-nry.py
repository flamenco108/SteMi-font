#!/usr/bin/env python3
import sys

def extract_numbers_from_file(input_filename, output_filename):
    with open(input_filename, 'r') as input_file:
        numbers = [line.split('=')[1].strip() for line in input_file]

    with open(output_filename, 'w') as output_file:
        for number in numbers:
            output_file.write(f"{number}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_filename>")
    else:
        input_filename = sys.argv[1]
        output_filename = f"{input_filename}-only"
        extract_numbers_from_file(input_filename, output_filename)