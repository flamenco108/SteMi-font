#!/usr/bin/env python3

import fontforge
import sys

def modify_font_names(sfd_file, new_family_name, new_style_name):
    # Open the SFD file as a font
    font = fontforge.open(sfd_file)

    # Define the new names
    new_full_name = new_family_name + " " + new_style_name

    # Change the names
    font.familyname = new_family_name
    font.fullname = new_full_name
    font.fontname = new_full_name

    # Save the changes back to the SFD file
    font.save(sfd_file)

# Check if the correct number of arguments is provided
if len(sys.argv) < 4:
    print("Usage: ", sys.argv[0], " <SFD_file> <New_Family_Name> <New_Style_Name>")
    sys.exit(1)

# Extract arguments from sys.argv
sfd_file_path = sys.argv[1]
new_family_name = sys.argv[2]
new_style_name = sys.argv[3]

# Call the function to modify font names and save changes
modify_font_names(sfd_file_path, new_family_name, new_style_name)

