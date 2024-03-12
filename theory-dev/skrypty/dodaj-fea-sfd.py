#!/usr/bin/env python3

import fontforge
import sys

def add_fea_to_sfd(input_sfd, input_fea, output_sfd):
    try:
        font = fontforge.open(input_sfd)
        font.mergeFeature(input_fea)
        font.save(output_sfd)
        font.close()
        print(f"Plik .fea został pomyślnie dodany do pliku {input_sfd} i zapisany jako {output_sfd}.")
    except Exception as e:
        print(f"Wystąpił błąd podczas dodawania pliku .fea do pliku .sfd: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Użycie:", sys.argv[0], "[input_sfd] [input_fea] [output_sfd]")
        sys.exit(1)
    
    input_sfd = sys.argv[1]
    input_fea = sys.argv[2]
    output_sfd = sys.argv[3]
    
    add_fea_to_sfd(input_sfd, input_fea, output_sfd)
