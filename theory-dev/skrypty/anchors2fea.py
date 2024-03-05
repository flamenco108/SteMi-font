#!/usr/bin/env python3

import sys
import fontforge
import re

#def export_anchors_to_fea(font_path, fea_output_path):
#    font = fontforge.open(font_path)
#    fea_output = []

#    fea_output.append("languagesystem DFLT dflt;\n")

#    for glyph in font.glyphs():
#        fea_output.append(f"\n# Anchors for {glyph.glyphname}\n")
#        for anchor in glyph.anchors:
#            fea_output.append(f"<anchor {anchor.x} {anchor.y}> {anchor.name};\n")

#    with open(fea_output_path, "w") as fea_file:
#        fea_file.write("".join(fea_output))

#    print(f"Anchors exported to {fea_output_path}")


#def export_anchors_to_fea(font_path, fea_output_path):
#    font = fontforge.open(font_path)
#    fea_output = []

#    fea_output.append("languagesystem DFLT dflt;\n")

#    for glyph in font.glyphs():
#        fea_output.append(f"\n# Anchors for {glyph.glyphname}\n")
#        for anchor in glyph.anchorPoints:
#            if len(anchor) == 3:
#                x, y, name = anchor
#                fea_output.append(f"<anchor {x} {y}> {name};\n")
#            else:
#                print(f"Invalid anchor format for {glyph.glyphname}: {anchor}")

#    with open(fea_output_path, "w") as fea_file:
#        fea_file.write("".join(fea_output))

#    print(f"Anchors exported to {fea_output_path}")


def export_anchors_to_fea(font_path, fea_output_path):
    with open(font_path, 'r', encoding='utf-8') as font_file:
        lines = font_file.readlines()

    anchors = []
    current_glyph = None

    for line in lines:
        if line.startswith('StartChar:'):
            current_glyph = line.split(': ')[1].strip()
        elif line.startswith('AnchorPoint:'):
            match = re.match(r'AnchorPoint: "([^"]+)" (\d+) (\d+) ([a-zA-Z]+) \d+', line)
            if match:
                name, x, y, anchor_type = match.groups()
                anchors.append((current_glyph, name, int(x), int(y), anchor_type))

    with open(fea_output_path, 'w', encoding='utf-8') as fea_file:
        fea_file.write("lookup curs {\n")
        for glyph, name, x, y, anchor_type in anchors:
            fea_file.write(f"    pos {glyph} <anchor {name}> {anchor_type} ({x}, {y});\n")
        fea_file.write("} curs;\n")

        fea_file.write("feature curs {\n")
        fea_file.write("    script DFLT;\n")
        fea_file.write("    language dflt;\n")
        fea_file.write("        lookup curs;\n")
        fea_file.write("} curs;\n")



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ", sys.argv[0], "[font_path.sfd] [fea_output_path.fea]")
    else:
        font_path = sys.argv[1]
        fea_output_path = sys.argv[2]
        export_anchors_to_fea(font_path, fea_output_path)
