#!/usr/bin/env python3

import sys
import fontforge

def apply_hinting(input_sfd_file):
    # Open the FontForge .sfd file
    font = fontforge.open(input_sfd_file)

    # Apply hinting to the font
    font.autoHint()

    # Save the hinted font back to the same .sfd file
    font.save(input_sfd_file)

    # Close the font
    font.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hint_font.py input_font.sfd")
        sys.exit(1)
    
    input_sfd_file = sys.argv[1]

    # Apply hinting to the input FontForge .sfd file
    apply_hinting(input_sfd_file)
