#!/usr/bin/env python3

from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeatures

def add_fea_to_otf(fea_file_path, otf_file_path):
    # Load the OTF font
    font = TTFont(otf_file_path)

    # Read the .fea file in binary mode
    with open(fea_file_path, 'rb') as fea_file:
        fea_content_bytes = fea_file.read()

    # Print the first 20 bytes for debugging
    print(f"First 20 bytes: {fea_content_bytes[:20]}")

    # Remove null bytes and decode
    fea_content_bytes = fea_content_bytes.replace(b'\x00', b'')
    fea_content = fea_content_bytes.decode('utf-8', errors='replace')

    # Print the first 100 characters of the decoded content
    print(f"First 100 characters of decoded content: {fea_content[:100]}")

    # Add features from the .fea file to the OTF font
    try:
        addOpenTypeFeatures(font, fea_content)
        print("Features added successfully")
    except Exception as e:
        print(f"Error adding features: {str(e)}")

    # Save the modified OTF font
    font.save(otf_file_path)
    print(f"Font saved to {otf_file_path}")

# Usage example: python script.py path/to/input.fea path/to/font.otf
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python", sys.argv[0], "path/to/input.fea path/to/font.otf")
    else:
        fea_file_path = sys.argv[1]
        otf_file_path = sys.argv[2]
        add_fea_to_otf(fea_file_path, otf_file_path)
