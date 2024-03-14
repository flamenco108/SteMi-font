#!/usr/bin/env python3

import sys
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.otTables import GSUB

def inspect_gsub_table(font_path):
    # Open the font file
    font = TTFont(font_path)

    # Check if GSUB table exists
    if "GSUB" in font:
        gsub_table = font["GSUB"]
        if isinstance(gsub_table, GSUB):
            print("GSUB Table Information:")
            print(f"Version: {gsub_table.tableVersion}")
            print(f"ScriptList: {gsub_table.ScriptList}")
            print(f"FeatureList: {gsub_table.FeatureList}")
            print(f"LookupList: {gsub_table.LookupList}")
            # Add more specific information as needed for feature extraction
        else:
            print("Error: GSUB table has unexpected structure.")
    else:
        print("Error: GSUB table not found in the font.")

    # Close the font file
    font.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_gpos_table.py font_path")
        sys.exit(1)
    font_path = sys.argv[1]

# Specify the path to your OpenType font file
#font_path = "path/to/your/font.otf"

# Call the function to inspect the GSUB table
inspect_gsub_table(font_path)