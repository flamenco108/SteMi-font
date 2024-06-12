#!/usr/bin/env python3

import sys

def find_string_with_context(word_list_file, search_string, preceding_letters, following_letters):
    try:
        with open(word_list_file, 'r') as file:
            for word in file:
                word = word.strip()
                start_index = word.find(search_string)
                if start_index != -1:
                    start_index += 1
                    end_index = start_index + len(search_string) + following_letters
                    if start_index <= preceding_letters + 1:
                        prefix = ">>" + word[:start_index - 1]
                        start_index = 1
                    else:
                        prefix = word[start_index - preceding_letters - 1:start_index - 1]
                    if end_index > len(word):
                        suffix = "<<"
                        end_index = len(word)
                    else:
                        suffix = ""
                    result = f"{prefix}{word[start_index - 1:end_index]}{suffix}"
                    print(result)
    except FileNotFoundError:
        print(f"Error: File {word_list_file} not found.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <word_list_file> <search_string> <no_preceding_letters> <no_following_letters>")
    else:
        word_list_file = sys.argv[1]
        search_string = sys.argv[2]
        preceding_letters = int(sys.argv[3])
        following_letters = int(sys.argv[4])
        find_string_with_context(word_list_file, search_string, preceding_letters, following_letters)
