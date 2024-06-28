#!/usr/bin/env python3

import fontforge
import sys

def find_glyphs_in_range(font, pua_start, pua_end, use_encoding_line):
    glyphs_in_range = []
    for glyph in font.glyphs():
        if use_encoding_line:
            if pua_start <= glyph.encoding <= pua_end:
                glyphs_in_range.append(glyph)
        else:
            if pua_start <= glyph.unicode <= pua_end:
                glyphs_in_range.append(glyph)
    return glyphs_in_range

def copy_glyph_properties(src_glyph, dest_glyph):
    dest_glyph.width = src_glyph.width
    dest_glyph.vwidth = src_glyph.vwidth
    dest_glyph.foreground = src_glyph.foreground
    dest_glyph.background = src_glyph.background
    dest_glyph.glyphname = src_glyph.glyphname

def move_glyphs_within_range(font, pua_start, pua_end, use_encoding_line):
    glyphs_in_range = find_glyphs_in_range(font, pua_start, pua_end, use_encoding_line)
    if not glyphs_in_range:
        print("No glyphs found in the specified range.")
        return
    
    # Sort glyphs by encoding or Unicode in ascending order
    glyphs_in_range.sort(key=lambda glyph: glyph.encoding if use_encoding_line else glyph.unicode)
    
    # Track the next available code point
    next_code_point = pua_start
    
    for glyph in glyphs_in_range:
        if use_encoding_line:
            original_code_point = glyph.encoding
        else:
            original_code_point = glyph.unicode
        
        # Skip if the original code point is not in the expected range
        if original_code_point < pua_start or original_code_point > pua_end:
            continue
        
        # Skip if glyph is already in the right position
        if original_code_point == next_code_point:
            print(f"Skipping glyph {glyph.glyphname} already at codepoint {original_code_point}")
            next_code_point += 1
            continue
        
        # Create a new glyph at the next available code point
        new_glyph = font.createChar(next_code_point)
        copy_glyph_properties(glyph, new_glyph)
        print(f"Moving glyph {glyph.glyphname} from {original_code_point} to {next_code_point}")
        
        # Remove the original glyph
        font.removeGlyph(glyph)
        
        # Increment next_code_point
        next_code_point += 1
        
        # Find the next available empty code point
        while next_code_point <= pua_end and (next_code_point in font and font[next_code_point].isWorthOutputting()):
            next_code_point += 1
        
        if next_code_point > pua_end:
            print(f"No more available code points in range {pua_start} to {pua_end}.")
            return
    
    # Save the modified font
    font.save(output_sfd)
    print(f"...Squeezed glyphs written to {output_sfd}")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python combine_glyphs.py <input_sfd> <output_sfd> <pua_start> <pua_end> <-n or -u>")
        sys.exit(1)
    
    input_sfd = sys.argv[1]
    output_sfd = sys.argv[2]
    pua_start = int(sys.argv[3])  # PUA start or encoding line number
    pua_end = int(sys.argv[4])    # PUA end or encoding line number
    option = sys.argv[5]  # -n or -u
    
    if option == '-n':
        use_encoding_line = True
    elif option == '-u':
        use_encoding_line = False
    else:
        print("Invalid option. Use -n for encoding line numbers or -u for Unicode values.")
        sys.exit(1)
    
    # Open the input SFD font file
    font = fontforge.open(input_sfd)
    
    # Move glyphs within the specified range towards smaller codepoints
    move_glyphs_within_range(font, pua_start, pua_end, use_encoding_line)
