#!/usr/bin/env python3

import fontforge
import sys
import shutil

def gather_codepoints(font, start_number, end_number):
    codepoints = {}
    for codepoint in range(start_number, end_number + 1):
        try:
            glyph = font[codepoint]
            if glyph is None or glyph.glyphname == ".notdef":
                codepoints[codepoint] = 0  # Empty codepoint
                print(f"empty = {codepoint}")
            else:
                codepoints[codepoint] = 1  # Occupied codepoint
                print(f"full = {glyph.glyphname} at {codepoint}")
        except TypeError:
            codepoints[codepoint] = 0  # Empty codepoint
            print(f"empty = {codepoint} (TypeError)")
    return codepoints

def move_glyphs(font, codepoints):
    sorted_codepoints = sorted(codepoints.items())
    empty_codepoints = [cp for cp, status in sorted_codepoints if status == 0]
    occupied_codepoints = [cp for cp, status in sorted_codepoints if status == 1]
    
    for old_cp in occupied_codepoints:
        if not empty_codepoints:
            break
        new_cp = empty_codepoints.pop(0)
        glyph = font[old_cp]
        print(f"Moving glyph {glyph.glyphname} from {old_cp} to {new_cp}")
        
        # Move the glyph to the new codepoint
        font.selection.select(old_cp)
        font.copy()
        font.selection.select(new_cp)
        font.paste()
        
        # Remove the old glyph
        font.removeGlyph(old_cp)

        # Update the glyph references
        glyph = font[new_cp]
        for layer in glyph.layers:
            if layer is not None:
                for ref in layer.references:
                    if ref[0].unicode == old_cp:
                        ref[0].unicode = new_cp

def main(input_file, output_file, start_number, end_number):
    shutil.copyfile(input_file, input_file + "-temp")
    
    font = fontforge.open(input_file + "-temp")
    codepoints = gather_codepoints(font, start_number, end_number)
    
    move_glyphs(font, codepoints)
    
    font.save(output_file)
    font.close()
    print(f"Glyphs have been moved and saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: script.py <input_file> <output_file> <start_number> <end_number>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    start_number = int(sys.argv[3])
    end_number = int(sys.argv[4])

    main(input_file, output_file, start_number, end_number)
