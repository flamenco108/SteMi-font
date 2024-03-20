#!/usr/bin/env python3
import sys
from fontTools.ttLib import TTFont

def get_glyphs_and_codepoints(otf_file):
    font = TTFont(otf_file)
    cmap = font['cmap'].getcmap(3, 1)  # Windows Unicode BMP (UCS-2)
    
    glyphs_codepoints = []
    if cmap:
        for codepoint, glyph_name in cmap.cmap.items():
            glyphs_codepoints.append((glyph_name, f"U+{codepoint:04X}"))
    
    return glyphs_codepoints

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the OTF file as an argument.")
    else:
        otf_file = sys.argv[1]
        result = get_glyphs_and_codepoints(otf_file)
        for glyph, codepoint in result:
            #print(f"Glyph: {glyph}, Codepoint: {codepoint}")
            print(f"g{glyph} = {codepoint}")

