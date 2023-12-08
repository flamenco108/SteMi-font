#!/usr/bin/env python3

import fontforge, sys, time

# Open the font
#font = fontforge.open("myfont.sfd")
if __name__ == "__main__":
	font = fontforge.open(sys.argv[1])


# Loop through all glyphs
	for glyph in font.glyphs():
	    # Replace references with splines
	    #glyph.replaceWithSpline()
	    glyph.UnlinkReference()

	# Save the font
	font.save(sys.argv[1])