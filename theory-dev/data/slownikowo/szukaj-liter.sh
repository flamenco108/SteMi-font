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
while read -r word; do
    start_index=$(expr index "$word" "$search_string")
    if [ "$start_index" -gt 0 ]; then
        start_index=$((start_index - 1))
        end_index=$((start_index + ${#search_string} + following_letters))
        if [ "$start_index" -le "$preceding_letters" ]; then
            prefix=">>"
            start_index=0
        else
            prefix="${word:$((start_index - preceding_letters)):$preceding_letters}"
        fi
        if [ "$end_index" -gt "${#word}" ]; then
            suffix=""
            end_index=${#word}
        else
            suffix="${word:$end_index:$following_letters}"
        fi
        result="${prefix}${word:$start_index:$((end_index - start_index))}${suffix}"
        echo "$result"
    fi
done < "$word_list_file"
