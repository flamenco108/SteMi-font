#!/bin/bash

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

# 1. Remove all features and lookups from fontforge .sdf file: STEMI.sdf and write STEMI01.sdf
#fontforge -lang=ff -c 'Open($1); RemoveLookup(); Generate($2);' STEMI.sdf STEMI01.sdf

# 2. Remove all anchors from fontforge .sdf file: STEMI01.sdf and write STEMI02.sdf
#fontforge -lang=ff -c 'Open($1); SelectAll(); UnlinkAnchors(); Generate($2);' STEMI01.sdf STEMI02.sdf


#fontforge -lang=ff -c 'Open($1); SelectAll(); RemoveLookup(); UnlinkAnchors(); Generate($2);' $ARG STEMI02.sdf

#fontforge -lang=ff -c 'Open($1); SelectAll(); ClearLookup(); UnlinkAnchors(); Generate($2);' $ARG STEMI02.sdf

#fontforge -lang=ff -c 'Open($1); lookups = GetLookups("GSUB"); foreach (lookup in lookups) { RemoveLookup(lookup); } lookups = GetLookups("GPOS"); foreach (lookup in lookups) { RemoveLookup(lookup); }; UnlinkAnchors(); Generate($2);' $ARG STEMI02.sdf


#fontforge -lang=ff -c 'Open($1); lookups = GetLookups("GSUB"); foreach (lookup in lookups) { RemoveLookup(lookup); } lookups = GetLookups("GPOS"); foreach (lookup in lookups) { RemoveLookup(lookup); } UnlinkAnchors(); Generate($2);' $1 STEMI02.sdf

#fontforge -lang=ff -c 'Open($1); lookups = GetLookups("GSUB"); foreach (lookup in lookups) RemoveLookup(lookup); lookups = GetLookups("GPOS"); foreach (lookup in lookups) RemoveLookup(lookup); UnlinkAnchors(); Generate($2);' $1 STEMI02.sdf

fontforge -lang=ff -c 'Open($1); lookups = GetLookups("GSUB"); foreach (lookup in lookups) { RemoveLookup(lookup); }; lookups = GetLookups("GPOS"); foreach (lookup in lookups) { RemoveLookup(lookup); } UnlinkAnchors(); Generate($2);' $ARG STEMI02.sdf