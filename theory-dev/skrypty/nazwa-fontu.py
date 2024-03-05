#!/usr/bin/env python3

import fontforge
import sys

def get_font_name(sfd_file):
    # Open the SFD file as a font
    font = fontforge.open(sfd_file)

    # Get the font name
    font_name = font.fullname

    return font_name

# Check if the correct number of arguments is provided
if len(sys.argv) < 2:
    print("Usage: ", sys.argv[0], " <SFD_file>")
    sys.exit(1)

# Extract the SFD file path from sys.argv
sfd_file_path = sys.argv[1]

# Retrieve the font name from the SFD file
font_name = get_font_name(sfd_file_path)

print(font_name)

