#!/usr/bin/env python3

from fontTools import ttLib
from fontTools.feaLib.builder import addOpenTypeFeatures
import sys

def add_features_to_font(font_path, fea_path, output_font_path):
    font = ttLib.TTFont(font_path)
    
    try:
        with open(fea_path, 'rb') as fea_file:
            fea_bytes = fea_file.read()
        
        try:
            fea_text = fea_bytes.decode('utf-8')
        except UnicodeDecodeError as e:
            print(f"Error decoding {fea_path}: {e}")
            fea_text = fea_bytes.decode('utf-8', errors='replace')
            print("Problematic characters were replaced.")
        
        addOpenTypeFeatures(font, fea_text)
        font.save(output_font_path)
        print(f"Successfully added features to {output_font_path}")
    except Exception as e:
        print(f"Failed to add features to font: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python", sys.argv[0], "path/to/input-font.otf path/to/input.fea path/to/output-font.otf")
    else:
        font_path = sys.argv[1]
        fea_path = sys.argv[2]
        output_font_path = sys.argv[3]
        add_features_to_font(font_path, fea_path, output_font_path)
