#!/usr/bin/env python3

import sys

def find_string_with_context(word_list_file, search_string, num_preceding_chars, num_following_chars, show_boundaries, show_word):
    try:
        with open(word_list_file, 'r') as file:
            words_with_string = [word.strip() for word in file if search_string in word]

            for word in words_with_string:
                start_index = word.find(search_string)
                preceding_chars = word[max(start_index - num_preceding_chars, 0):start_index] if num_preceding_chars > 0 else ""
                if show_boundaries and num_preceding_chars > 0:
                    if len(preceding_chars) == num_preceding_chars:
                        preceding_chars = ">" + preceding_chars
                    elif len(preceding_chars) < num_preceding_chars:
                        preceding_chars = ">>" + preceding_chars
                end_index = start_index + len(search_string) + num_following_chars
                following_chars = word[start_index + len(search_string):end_index] if end_index <= len(word) else word[start_index + len(search_string):]
                if num_following_chars == 1:
                    following_chars = following_chars[:1]
                if show_boundaries and num_following_chars > 0:
                    if len(following_chars) == num_following_chars:
                        following_chars += "<"
                    else:
                        following_chars += "<<"
                result = f"{preceding_chars}{search_string}{following_chars}"
                if num_preceding_chars == 0 and num_following_chars == 0:
                    result = search_string
                if show_word:
                    print(f"{word}\t{result}")
                else:
                    print(result)
    except FileNotFoundError:
        print(f"Error: File {word_list_file} not found.")

if __name__ == "__main__":
    if len(sys.argv) < 5 or len(sys.argv) > 7:
        print("Usage: python script.py <word_list_file> <search_string> <no_preceding_chars> <no_following_chars> [-b] [-w]")
    else:
        word_list_file = sys.argv[1]
        search_string = sys.argv[2]
        num_preceding_chars = int(sys.argv[3])
        num_following_chars = int(sys.argv[4])
        show_boundaries = False
        show_word = False
        for arg in sys.argv[5:]:
            if arg == "-b":
                show_boundaries = True
            elif arg == "-w":
                show_word = True
        find_string_with_context(word_list_file, search_string, num_preceding_chars, num_following_chars, show_boundaries, show_word)
