#!/usr/bin/env python3
import sys
from fontTools.ttLib import TTFont

def extract_features(font):
    """Extract OpenType features from the font."""
    # Access the GSUB and GPOS tables
    gsub_table = font['GSUB'].table
    gpos_table = font['GPOS'].table

    # Initialize an empty string to store feature definitions
    feature_definitions = ""

    # Extract GSUB features (ligatures, substitutions, etc.)
    for lookup in gsub_table.LookupList.Lookup:
        # Your logic to process each lookup here
        # Example: feature_definitions += f"lookup {lookup.LookupType} {{ ... }}\n"

    # Extract GPOS features (kerning, positioning, etc.)
    for lookup in gpos_table.LookupList.Lookup:
        # Your logic to process each lookup here
        # Example: feature_definitions += f"lookup {lookup.LookupType} {{ ... }}\n"

    return feature_definitions

def main():
    if len(sys.argv) != 3:
        print("Usage: python myfonttool.py input.otf output.fea")
        sys.exit(1)

    input_otf = sys.argv[1]
    output_fea = sys.argv[2]

    try:
        font = TTFont(input_otf)
        extracted_features = extract_features(font)

        # Write extracted features to .fea file
        with open(output_fea, 'w') as fea_file:
            fea_file.write(extracted_features)

        print(f"Features extracted from {input_otf} and saved to {output_fea}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()






##################

        #from fontTools.ttLib import TTFont
#from fontTools.feaLib.builder import addOpenTypeFeatures

#def extract_features_and_lookups(font_path, output_fea_path):
    # Load the OTF font using FontTools
#    font = TTFont(font_path)

    # Create a file to write the extracted features and lookups
#    with open(output_fea_path, 'w') as fea_file:
        # Initialize an empty feature file
#        fea_file.write("languagesystem DFLT dflt;\n")
#        fea_file.write("languagesystem latn dflt;\n\n")

        # Extract OpenType features and lookups using FontTools
#        features, lookups = addOpenTypeFeatures(font)

        # Write the extracted features and lookups to the .fea file
#        for feature in features:
#            fea_file.write(feature.asFea() + "\n\n")

#        for lookup in lookups:
#            fea_file.write(lookup.asFea() + "\n\n")

#    print(f"Features and lookups extracted from {font_path} and saved to {output_fea_path}")

# Example usage
#font_path = "path/to/your/font.otf"
#output_fea_path = "path/to/output/font_features.fea"
#extract_features_and_lookups(font_path, output_fea_path)
##############