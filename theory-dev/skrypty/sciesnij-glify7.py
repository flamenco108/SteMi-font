#!/usr/bin/env python3

def move_glyphs(font, codepoints):
    sorted_codepoints = sorted(codepoints.items())
    empty_codepoints = [cp for cp, status in sorted_codepoints if status == 0]
    occupied_codepoints = [cp for cp, status in sorted_codepoints if status == 1]
    
    for old_cp in occupied_codepoints:
        if not empty_codepoints:
            break
        
        new_cp = empty_codepoints.pop(0)
        glyph = font[old_cp]
        
        # Check if the glyph is already at its correct position
        if glyph.unicode == new_cp:
            print(f"Glyph {glyph.glyphname} is already at correct position {new_cp}. Skipping...")
            continue
        
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
