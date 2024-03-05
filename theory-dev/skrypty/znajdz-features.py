#!/usr/bin/env python3

import fontforge
import sys

def list_lookups_and_features(font):
    print("Lookups:")
    if font.gsub_lookups:
        for lookup_type in font.gsub_lookups:
            for lookup in lookup_type:
                print("  -", lookup)
    else:
        print("  No GSUB lookups found.")
    
    if font.gpos_lookups:
        print("GPOS Lookups:")
        for lookup_type in font.gpos_lookups:
            for lookup in lookup_type:
                print("  -", lookup)
    else:
        print("  No GPOS lookups found.")
    
    try:
        if font.features:
            print("Features:")
            for feature in font.features:
                print("  -", feature)
        else:
            print("  No features found.")
    except AttributeError:
        print("  No features found.")

def list_look_and_feat(font_file_path):
#    font = fontforge.open(font_file_path)
    
    print("Lookups:")
    for lookup in font.gpos_lookups + font.gsub_lookups:
        print(f"Lukap: {lookup}")
    
    print("\nFeatures:")
    for feature in font.gsub_lookups + font.gpos_lookups:
        print(f"Ficzer: {feature}")
    
    print ("\nLokupSubtablez:")
    for lsub in font.getLookupSubtables() + font.getLookupSubtableAnchorClasses():
        print(f"lsub: {lsub}")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        #font = fontforge.open(input_file)
        #list_lookups_and_features(font)
        #print("###########")
        font = fontforge.open(input_file)
        list_look_and_feat(font)
        font.close()
    except Exception as e:
        print("Error:", e)

