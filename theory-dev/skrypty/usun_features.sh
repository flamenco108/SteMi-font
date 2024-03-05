#!/usr/bin/fontforge
TTFfileName = $1;
#Font format - otf or ttf. In my case - otf
FontExt = "sfd"
Open(TTFfileName,1);
lookups = GetLookups("GSUB"); numlookups = SizeOf(lookups); i = 0;
    while (i < numlookups)
        RemoveLookup(lookups[i]); i++;
    endloop
lookups = GetLookups("GPOS"); numlookups = SizeOf(lookups); i = 0;
    while (i < numlookups)
        RemoveLookup(lookups[i]); i++;
    endloop
Generate(TTFfileName.FontExt); Close(); Quit(0);
