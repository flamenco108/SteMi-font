#!/usr/bin/env python3

import fontforge, sys, time
if __name__ == "__main__":
    font = fontforge.open(sys.argv[1])
    for glyph in font:
        #glyph.anchorPoints = ()
        font[glyph].anchorPoints = ()
        #glyph.anchorClasses = {}
    for anchorklas in font.getLookupSubtableAnchorClasses:
        font.removeAnchorClass(anchorklas)
        #font[font].anchorClasses = {}
    for lookup in font.gsub_lookups:
        font.removeLookup(lookup)
    for lookup in font.gpos_lookups:
        font.removeLookup(lookup)
    font.unlinkReferences()
    font.save(sys.argv[1])
	

# Loop through all glyphs
#	for glyph in font.glyphs():
	    # Replace references with splines
	    #glyph.replaceWithSpline()
#	    glyph.UnlinkReference()


#import fontforge, sys, time

# Open the font

#if __name__ == "__main__":
#	font = fontforge.open(sys.argv[1])
#	for glyphname in font:
#		font[glyphname].anchorPoints = ()
#	lookups = font.getLookupList("GSUB")
#	for lookup in lookups:
#		font.removeLookup(lookup)
#	lookups = font.getLookupList("GPOS")
#	for lookup in lookups:
#		font.removeLookup(lookup)
	# Save the font
#	font.save(sys.argv[1])