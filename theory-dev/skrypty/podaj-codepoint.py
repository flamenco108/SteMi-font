#!/usr/bin/env python3

import sys
import fontforge

def get_glyph_codepoint(sfd_file_path, glyph_name):
    try:
        font = fontforge.open(sfd_file_path)
        glyph = font[glyph_name]

        if glyph:
            codepoint = glyph.encoding
            unicode_codepoint = glyph.unicode

            print(f"Chosen glyph: {glyph_name}")
            if codepoint != -1:
                print(f"Numerical codepoint: {codepoint}")
            else:
                print("Glyph has no numerical codepoint assigned.")

            if unicode_codepoint != -1:
                print(f"Unicode codepoint: U+{unicode_codepoint:04X}")
            else:
                print("Glyph has no Unicode codepoint assigned.")
        else:
            print(f"Glyph '{glyph_name}' not found in the font.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <sfd_file_path> <glyph_name>")
        sys.exit(1)

    sfd_file_path = sys.argv[1]
    glyph_name = sys.argv[2]

    get_glyph_codepoint(sfd_file_path, glyph_name)