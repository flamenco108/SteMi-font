#!/usr/bin/env python3

import fontforge
import sys
import os

def create_glyph_class(sfd_path, fea_path):
    # Load the SFD file
    font = fontforge.open(sfd_path)

    # Get all glyph names
    glyph_names = [glyph.glyphname for glyph in font.glyphs()]

    # Sort glyph names alphabetically
    glyph_names.sort()

    # Create the class definition
    class_definition = "@glyphs = ["

    # Add glyph names to the class definition
    for name in glyph_names:
        class_definition += f" {name}"

    # Close the class definition
    class_definition += " ];"

    # Create the .fea file
    with open(fea_path, "w") as fea_file:
        fea_file.write(class_definition)

    print(f"Glyph class created in {fea_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <sfd_file_path> <fea_file_path>")
        sys.exit(1)

    sfd_path = sys.argv[1]
    fea_path = sys.argv[2]

    if not os.path.exists(sfd_path):
        print(f"Error: {sfd_path} does not exist.")
        sys.exit(1)

    create_glyph_class(sfd_path, fea_path)

