#!/bin/bash

if [[ $# -eq 0 ]] ; then
  echo "Usage: $0 sciezka/do/plik_do_przerobki"
  echo ""
  exit 0
fi



echo
echo "Usuwanie kotwic (anchorów)"
echo
echo "=============="


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

echo "================"
echo

#grep -v '^AnchorPoint: ' < $ARG > $PLIKSB.noanchor.$ROZSZERZENIE ;
cat $ARG | grep -v '^AnchorPoint: ' | grep -v '^AnchorClass' > $PLIKSB.noanchor.$ROZSZERZENIE && echo "Usuwanie linijek z Anchor w pliku $ARG zakończone"
