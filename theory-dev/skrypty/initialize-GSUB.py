#!/usr/bin/env python3

import sys
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.otTables import GSUB

def initialize_gsub_table(font_path):
    # Open the font file
    font = TTFont(font_path)

    # Initialize GSUB table if it doesn't exist
    if "GSUB" not in font:
        font.newTable("GSUB")
        gsub_table = font["GSUB"]
        gsub_table.tableVersion = 0x00010000
        gsub_table.ScriptList = []
        gsub_table.FeatureList = []
        gsub_table.LookupList = []

    # Close the font file
    font.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_gpos_table.py font_path")
        sys.exit(1)
    font_path = sys.argv[1]

# Specify the path to your OpenType font file
#font_path = "path/to/your/font.otf"

# Call the function to initialize the GSUB table
initialize_gsub_table(font_path)