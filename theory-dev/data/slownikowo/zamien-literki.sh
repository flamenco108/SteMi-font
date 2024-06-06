#!/bin/bash

# Sprawdź, czy podano argument (nazwę pliku)
if [ -z "$1" ]; then
    echo "Użycie: $0 nazwa_pliku"
    exit 1
fi

# Przypisz nazwę pliku i rozszerzenie do zmiennych
nazwa_pliku=$(basename "$1" .txt)
rozszerzenie="${1##*.}"

# Utwórz nazwę pliku wynikowego
plik_wynikowy="${nazwa_pliku}-wyn.${rozszerzenie}"

# Przetwórz plik wejściowy i zapisz do pliku wynikowego
tr 'Ņ' 'ń' < "$1" > 01.slnp
tr 'Ą' 'ą' < 01.slnp > "$plik_wynikowy"
rm 01.slnp

echo "Plik wynikowy: $plik_wynikowy"
