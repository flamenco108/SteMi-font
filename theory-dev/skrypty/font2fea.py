#!/usr/bin/env python3

'''Font2fea: A simple python FontForge script to export the smarts in a font into FEA format 
You need a recent version of FontForge with its python module.
This works on all font formats FontForge supports.'''
__url__ = 'http://projects.palaso.org/projects/pysilfont'
__copyright__ = 'Copyright (c) 2013, SIL International  (http://www.sil.org)'
__license__ = 'Released under the MIT License (http://opensource.org/licenses/MIT)'
__author__ = 'Nicolas Spalinger. '
__version__ = '1.0'

import fontforge, sys, time

''' version checking to make sure we have a decently recent FontForge '''
required_version = "20100212"
if fontforge.version() < required_version:
	print ("Your version of FontForge is too old - %s or newer is required" % (required_version))

if __name__ == "__main__":
	font = fontforge.open(sys.argv[1])

	''' get the names for the sfnt object '''
	names = {}
	for n in font.sfnt_names :
		if n[0] == "English (US)" :
			names[n[1]] = n[2]

	print ("") 
	''''
	print (font.copyright + "\n\n" + names.get('License URL') + "\n\nMake sure you have the rights to reuse, modify and redistribute the exported smart font code as indicated by copyright and license in the font")
	'''
	print ("") 
	
	font.generateFeatureFile(font.fontname + "-" + font.weight + "-" + "exported" + time.strftime("-%Y-%m-%d-%Hh%M") + ".fea")
	font.close()

	print ("Done: .fea feature file generated")