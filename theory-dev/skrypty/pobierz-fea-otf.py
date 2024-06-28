#!/usr/bin/env python3

from fontTools import ttLib
from fontTools.feaLib.builder import addOpenTypeFeatures, Builder
from fontTools.feaLib.parser import Parser
from io import StringIO

def extract_features(font_path, output_fea_path):
    font = ttLib.TTFont(font_path)
    builder = Builder(font, font.getGlyphOrder())
    
    fea = StringIO()
    builder.buildFeatures(fea)
    
    with open(output_fea_path, 'w') as f:
        f.write(fea.getvalue())

# Usage
extract_features('path/to/your/font.otf', 'output_features.fea')
