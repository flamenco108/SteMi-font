#!/usr/bin/env python3

import sys

def find_string_with_context(word_list_file, search_string, num_preceding_chars, num_following_chars, show_boundaries):
    try:
        with open(word_list_file, 'r') as file:
            for word in file:
                word = word.strip()
                start_index = word.find(search_string)
                if start_index != -1:
                    start_index += 1
                    preceding_chars = word[max(start_index - num_preceding_chars - 1, 0):start_index - 1]
                    if show_boundaries:
                        if len(preceding_chars) == num_preceding_chars:
                            preceding_chars = ">" + preceding_chars
                        elif len(preceding_chars) < num_preceding_chars:
                            preceding_chars = ">>" + preceding_chars
                    end_index = start_index + len(search_string) + num_following_chars - 1
                    following_chars = word[start_index + len(search_string):end_index]
                    if show_boundaries and end_index >= len(word):
                        if end_index == len(word):
                            following_chars += "<"
                        else:
                            following_chars += "<<"
                    result = f"{preceding_chars}{word[start_index - 1:start_index + len(search_string)]}{following_chars}"
                    print(result)
    except FileNotFoundError:
        print(f"Error: File {word_list_file} not found.")

if __name__ == "__main__":
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print("""Usage: python script.py <word_list_file> <search_string> <no_preceding_chars> <no_following_chars> [-b]
        where '-b' makes script show if there are word boundary(><) or more characters(>><<)""")
    else:
        word_list_file = sys.argv[1]
        search_string = sys.argv[2]
        num_preceding_chars = int(sys.argv[3])
        num_following_chars = int(sys.argv[4])
        show_boundaries = False
        if len(sys.argv) == 6 and sys.argv[5] == "-b":
            show_boundaries = True
        find_string_with_context(word_list_file, search_string, num_preceding_chars, num_following_chars, show_boundaries)
