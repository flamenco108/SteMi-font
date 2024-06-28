#!/usr/bin/env python3

import fontforge
import sys


def move_glyphs_with_gaps(input_file, output_file, start_codepoint, end_codepoint):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    glyphs = []
    current_glyph = None

    for line in lines:
        if line.startswith('StartChar:'):
            if current_glyph:
                glyphs.append(current_glyph)
            current_glyph = [line]
        elif current_glyph is not None:
            current_glyph.append(line)

    if current_glyph:
        glyphs.append(current_glyph)

    glyphs_in_range = []
    for glyph in glyphs:
        encoding_line_index = next(i for i, line in enumerate(glyph) if line.startswith('Encoding:'))
        encoding_parts = glyph[encoding_line_index].split()
        codepoint = int(encoding_parts[1])

        if start_codepoint <= codepoint <= end_codepoint:
            glyphs_in_range.append((codepoint, glyph))

    glyphs_in_range.sort()

    new_glyphs = []
    last_codepoint = start_codepoint - 1

    for i, (codepoint, glyph) in enumerate(glyphs_in_range):
        if i == 0:
            # First glyph stays at its original position
            new_codepoint = codepoint
        else:
            # Move glyph only if there's a gap
            if codepoint > last_codepoint + 1:
                new_codepoint = last_codepoint + 1
            else:
                new_codepoint = codepoint

        encoding_line_index = next(i for i, line in enumerate(glyph) if line.startswith('Encoding:'))
        encoding_parts = glyph[encoding_line_index].split()
        encoding_parts[1] = str(new_codepoint)
        glyph[encoding_line_index] = ' '.join(encoding_parts) + '\n'

        new_glyphs.append(glyph)
        last_codepoint = new_codepoint

    remaining_glyphs = [glyph for codepoint, glyph in glyphs if not (start_codepoint <= codepoint <= end_codepoint)]
    new_glyphs.extend(remaining_glyphs)

    with open(output_file, 'w', encoding='utf-8') as file:
        for glyph in new_glyphs:
            for line in glyph:
                file.write(line)

# Example usage
# move_glyphs_with_gaps('Stemi-04.06-2024.sfd', 'Stemi-sciesnione.sfd', 57344, 63743)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <input_sfd> <output_sfd> <pua_start> <pua_end>")
        sys.exit(1)
    
    input_sfd = sys.argv[1]
    output_sfd = sys.argv[2]
    pua_start = int(sys.argv[3])
    pua_end = int(sys.argv[4])
    #option = sys.argv[5]
    
    #if option == '-n':
    #    use_encoding_line = True
    #elif option == '-u':
    #    use_encoding_line = False
    #else:
    #    print("Invalid option. Use -n for encoding line numbers or -u for Unicode values.")
    #    sys.exit(1)
    
    font = fontforge.open(input_sfd)
    
    move_glyphs_with_gaps(input_sfd, output_sfd, pua_start, pua_end)
    # move_glyphs_within_range(font, pua_start, pua_end, use_encoding_line)