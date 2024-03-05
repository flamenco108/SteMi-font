#!/usr/bin/env python3

import fontforge
import sys


def open_sfd_file(input_file):
    """
    Otwiera wskazany plik FontForge SFD.
    """
    try:
        font = fontforge.open(input_file)
        return font
    except fontforge.fontforgeError as e:
        print("Błąd podczas otwierania pliku SFD:", e)
        return None


def remove_all_features(input_file, output_file):
    try:
        font = fontforge.open(input_file)
        if font.gsub_lookups or font.gpos_lookups:
            for lookup_type in font.gsub_lookups + font.gpos_lookups:
                for lookup in lookup_type:
                    font.removeLookup(lookup)
            font.generate(output_file)
            font.close()
            print(f"Usunięto wszystkie funkcje z pliku {input_file} i zapisano do {output_file}.")
        else:
            print(f"Brak funkcji do usunięcia w pliku {input_file}.")
    except Exception as e:
        print(f"Wystąpił błąd podczas przetwarzania pliku: {e}")

def remove_anchor_lines(font):
    lines_to_keep = []
    with open(font, 'r') as file:
        for line in file:
            if not line.strip().startswith('AnchorPoint:'):
                lines_to_keep.append(line)

    # Sprawdzenie czy coś zostało usunięte, jeśli nie, to nic nie rób
    if len(lines_to_keep) == 0:
        print("Brak linii z AnchorPoint w pliku.")
        return

    # Zapisanie linii z AnchorPoint
    with open(file_path, 'w') as file:
        for line in lines_to_keep:
            file.write(line)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Użycie:", sys.argv[0], " input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    remove_all_features(input_file, output_file)