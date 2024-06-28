#!/usr/bin/env python3

import fontforge
import sys
import shutil

def gather_codepoints(font, start_number, end_number):
    codepoints = {}
    for codepoint in range(start_number, end_number + 1):
        glyph = font.createMappedChar(codepoint)
        if glyph.glyphname == ".notdef":
            codepoints[codepoint] = 0  # Empty codepoint
            print(f"empty = {glyph.glyphname}")
        else:
            codepoints[codepoint] = 1  # Occupied codepoint
            print(f"full = {glyph.glyphname}")
    return codepoints

def move_glyphs(font, codepoints):
    sorted_codepoints = sorted(codepoints.items())
    empty_codepoints = [cp for cp, status in sorted_codepoints if status == 0]
    occupied_codepoints = [cp for cp, status in sorted_codepoints if status == 1]
    
    for old_cp in occupied_codepoints:
        if not empty_codepoints:
            break
        new_cp = empty_codepoints.pop(0)
        glyph = font.createMappedChar(old_cp)
        print(f"Moving glyph {glyph.glyphname} from {old_cp} to {new_cp}")
        
        glyph.unicode = new_cp
        glyph.changed()
        
        for layer_name in glyph.layerOrder:
            layer = glyph.layers[layer_name]
            if layer is not None:
                for ref in layer.references:
                    ref_glyph = font[ref.glyph]
                    if ref_glyph.unicode == old_cp:
                        ref_glyph.unicode = new_cp

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
