#!/usr/bin/env python3

import sys
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.otTables import GPOS

def inspect_gpos_table(font_path):
    # Open the font file
    font = TTFont(font_path)

    # Check if GPOS table exists
    if "GPOS" in font:
        gpos_table = font["GPOS"]
        if isinstance(gpos_table, GPOS):
            print("GPOS Table Information:")
            print(f"Version: {gpos_table.tableVersion}")
            print(f"ScriptList: {gpos_table.ScriptList}")
            print(f"FeatureList: {gpos_table.FeatureList}")
            print(f"LookupList: {gpos_table.LookupList}")
            # Add more specific information as needed for anchor extraction
        else:
            print("Error: GPOS table has unexpected structure.")
    else:
        print("Error: GPOS table not found in the font.")

    # Close the font file
    font.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_gpos_table.py font_path")
        sys.exit(1)
    font_path = sys.argv[1]

    # Call the function to inspect the GPOS table
    inspect_gpos_table(font_path)