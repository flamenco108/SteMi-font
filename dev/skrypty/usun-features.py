#!/usr/bin/env python3

import fontforge
import sys

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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Sposób użycia: python script.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    remove_all_features(input_file, output_file)