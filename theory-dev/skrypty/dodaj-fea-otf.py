#!/usr/bin/env python3

from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeatures

#def add_fea_to_otf(fea_file_path, otf_file_path):
    # Load the OTF font
#    font = TTFont(otf_file_path)

    # Read the .fea file
#    with open(fea_file_path, 'r') as fea_file:
#        fea_content = fea_file.read()

    # Add features from the .fea file to the OTF font
#    addOpenTypeFeatures(font, fea_content)

    # Save the modified OTF font
#    font.save(otf_file_path)


def add_fea_to_otf(fea_content, otf_file_path):
    # Load the OTF font
    font = TTFont(otf_file_path)

    # Add features from the .fea content to the OTF font
    addOpenTypeFeatures(font, fea_content)

    # Save the modified OTF font
    font.save(otf_file_path)




# Usage example: python script.py path/to/input.fea path/to/font.otf
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python", sys.argv[0], "path/to/input.fea path/to/font.otf")
    else:
        fea_content = sys.argv[1]
        otf_file_path = sys.argv[2]
        add_fea_to_otf(fea_content, otf_file_path)
