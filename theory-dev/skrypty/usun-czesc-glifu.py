#!/usr/bin/env python3

import fontforge
import sys

def remove_glyph_part(input_file, glyph_name, part_index, output_file):
    """
    Usuwa określoną część glifu z glifu o podanej nazwie w pliku sfd.
    Zapisuje zmiany do pliku sfd o podanej nazwie.
    """
    try:
        # Otwórz plik sfd
        font = fontforge.open(input_file)

        # Pobierz glif
        glyph = font[glyph_name]

        # Sprawdź, czy indeks części jest prawidłowy
        if part_index < len(glyph.layers):
            # Usuń określoną część glifu
            glyph.layers[part_index].removeOverlap()

            # Zapisz zmiany do nowego pliku sfd
            font.save(output_file)
            font.close()
            print(f"Usunięto część {part_index} z glifu {glyph_name}. Zapisano do {output_file}.")
        else:
            print("Nieprawidłowy indeks części glifu.")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

# Sprawdź, czy podano poprawną liczbę argumentów
if len(sys.argv) != 5:
    print("Użycie: python script.py input_file.sfd glyph_name part_index output_file.sfd")
else:
    input_file = sys.argv[1]
    glyph_name = sys.argv[2]
    part_index = int(sys.argv[3])
    output_file = sys.argv[4]

    remove_glyph_part(input_file, glyph_name, part_index, output_file)
