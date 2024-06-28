#!/usr/bin/env python3

import fontforge
import sys

def move_glyphs_with_gaps(input_file, output_file, start_codepoint, end_codepoint):
    # Open the font using FontForge
    font = fontforge.open(input_file)

    # Collect glyphs within the specified PUA range
    glyphs_in_range = []
    for glyph in font.glyphs():
        if glyph.unicode is not None and start_codepoint <= glyph.unicode <= end_codepoint:
            glyphs_in_range.append(glyph)

    # Sort glyphs by their original codepoints
    glyphs_in_range.sort(key=lambda x: x.unicode)

    # Track the last used codepoint to fill gaps
    last_codepoint = start_codepoint - 1

    # Move glyphs to fill gaps
    for glyph in glyphs_in_range:
        print(f" = = = \nglyph = {glyph}")

        # Move glyph only if there's a gap
        if glyph.unicode > last_codepoint + 1:
            new_codepoint = last_codepoint + 1
            print(f" * * * \nglyph = {glyph}")

            # Update glyph's unicode and name to avoid duplicates
            glyph.unicode = new_codepoint
            glyph.glyphname = f"uni{new_codepoint:04X}"
            print(f"codepoint = {glyph.unicode}")
            print(f"new_codepoint = {new_codepoint}")
            print(f"glyph.unicode = {glyph.unicode}")
            print(f"glyph.glyphname = {glyph.glyphname}")

        # Update last_codepoint
        last_codepoint = glyph.unicode
        print(f"last_codepoint = {last_codepoint}")

    # Save the modified font
    font.save(output_file)

# Main script logic
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <input_sfd> <output_sfd> <pua_start> <pua_end>")
        sys.exit(1)
    
    input_sfd = sys.argv[1]
    output_sfd = sys.argv[2]
    pua_start = int(sys.argv[3])
    pua_end = int(sys.argv[4])

    move_glyphs_with_gaps(input_sfd, output_sfd, pua_start, pua_end)
