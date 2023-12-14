#!/usr/bin/fontforge

if [[ $# -eq 0 ]] ; then
  echo "Usage: $0 sciezka/do/plik_do_przerobki"
  echo ""
  exit 0
fi

ARG=$1
echo "Podany argument: "$ARG
PLIK=${ARG##*/}
echo "Plik (bez ścieżki): "$PLIK
SCIEZKA=${ARG%/*}
echo "Ścieżka do pliku: "$SCIEZKA
ARGb=`realpath $ARG`
echo "Plik (ze ścieżką bezwzględną): "$ARGb
SCIEZKAB=${ARGb%/*}
echo "Ścieżka bezwzględna do pliku: " $SCIEZKAB
ROZSZERZENIE=${ARG##*.}
echo "Rozszerzenie pliku: "$ROZSZERZENIE
NAZWA=${PLIK%.*}
echo "Nazwa (bez rozszerzenia): "$NAZWA
PLIKS=$SCIEZKA/$NAZWA
echo "Nazwa (ze ścieżką): "$PLIKS
PLIKSB=$SCIEZKAB/$NAZWA
echo "Nazwa (ze ścieżką bezwgl): "$PLIKSB


TTFfileName = $ARG;
#Font format - otf or ttf. In my case - otf
#FontExt = "otf"
FontExt = $ROZSZERZENIE
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