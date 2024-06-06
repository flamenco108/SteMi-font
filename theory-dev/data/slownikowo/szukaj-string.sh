#!/bin/bash

# Check if the required arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <word_list_file> <search_string> <no_preceding_letters> <no_following_letters>"
    exit 1
fi

word_list_file="$1"
search_string="$2"
preceding_letters="$3"
following_letters="$4"

# Check if the word list file exists
if [ ! -f "$word_list_file" ]; then
    echo "Error: File $word_list_file not found."
    exit 1
fi

# Grep through the word list and print the results with the specified context
grep -E -o "(.{$preceding_letters})($search_string)(.{$following_letters})" "$word_list_file"
