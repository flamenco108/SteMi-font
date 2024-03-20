#!/usr/bin/env python3
import sys
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.otTables import BASE, GSUB, GPOS

def extract_features(font_file, output_file):
    font = TTFont(font_file)
    
    features = {}
    if GSUB in font:
        gsub_table = font[GSUB]
        for table in gsub_table.table.FeatureList.FeatureRecord:
            feature_tag = table.FeatureTag
            lookup_indices = [lookup.LookupListIndex for lookup in table.Feature.LookupListIndex]
            features[feature_tag] = lookup_indices
    
        with open(output_file, 'w') as fea_file:
            for feature in features:
                fea_file.write(f"feature {feature} {{\n")
                for lookup_index in features[feature]:
                    fea_file.write(f"    lookup {lookup_index};\n")
                fea_file.write("}};\n\n")
    else:
        print("GSUB table not found in the font file.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <font_file.otf> <output_file.fea>")
    else:
        font_file = sys.argv[1]
        output_file = sys.argv[2]
        extract_features(font_file, output_file)







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