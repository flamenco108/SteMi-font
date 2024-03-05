#!/bin/bash

# Sprawdź, czy podano poprawną liczbę argumentów
if [ "$#" -ne 3 ]; then
    echo "Użycie: $0 input_file.sfd line_to_remove output_file.sfd"
    exit 1
fi

# Przypisz argumenty do zmiennych
input_file="$1"
line_to_remove="$2"
output_file="$3"

# Usuń podaną linijkę z pliku i zapisz do nowego pliku
grep -vF "$line_to_remove" "$input_file" > "$output_file"

echo "Linia '$line_to_remove' została usunięta z pliku '$input_file' i zapisana do '$output_file'."
