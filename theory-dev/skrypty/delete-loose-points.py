#!/usr/bin/env python3

import fontforge
import sys
import os

def remove_loose_handles(sfd_path):
    # Load the SFD file
    font = fontforge.open(sfd_path)

    # Iterate over each glyph in the font
    for glyph in font.glyphs():
        # Get the glyph's layer
        layer = glyph.foreground

        # Iterate over each contour in the layer
        for contour in layer:
            # Iterate over each point in the contour
            for point in contour:
                # Check if the point is a curve point
                if point.type == "curve":
                    # Check if the curve handles are loose (not attached to any curve)
                    if point.prev.type == "curve" and point.next.type == "curve":
                        # Remove the loose curve handles
                        point.prev.makepositioncurvenear(point.prev.x, point.prev.y)
                        point.next.makepositioncurvenear(point.next.x, point.next.y)

    # Save the modified font
    font.save(sfd_path)
    print(f"Loose curve handles removed from {sfd_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <sfd_file_path>")
        sys.exit(1)

    sfd_path = sys.argv[1]

    if not os.path.exists(sfd_path):
        print(f"Error: {sfd_path} does not exist.")
        sys.exit(1)

    remove_loose_handles(sfd_path)
