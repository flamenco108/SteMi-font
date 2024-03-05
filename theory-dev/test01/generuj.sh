#!/bin/bash

if [[ $# -eq 0 ]] ; then
  echo "Usage: $0 sciezka/do/plik_do_przerobki"
  echo ""
  exit 0
fi

echo
echo "Generowanie plików testowych"
echo "=============="


ARG=$1 && echo "Podany argument: $ARG"
PLIK=${ARG##*/} && echo "Plik (bez ścieżki): $PLIK"
SCIEZKA=${ARG%/*} && echo "Ścieżka do pliku: $SCIEZKA"
ARGb=`realpath $ARG` && echo "Plik (ze ścieżką bezwzględną): $ARGb"
SCIEZKAB=${ARGb%/*} && echo "Ścieżka bezwzględna do pliku: $SCIEZKAB" 
ROZSZERZENIE=${ARG##*.} && echo "Rozszerzenie pliku: $ROZSZERZENIE"
NAZWA=${PLIK%.*} && echo "Nazwa (bez rozszerzenia): $NAZWA"
PLIKS=$SCIEZKA/$NAZWA && echo "Nazwa (ze ścieżką): $PLIKS"
PLIKSB=$SCIEZKAB/$NAZWA && echo "Nazwa (ze ścieżką bezwgl): $PLIKSB"
echo "----------------"
JA=`whoami`

FONTDIR="$HOME/.fonts/" && echo "Dir fontów: "$FONTDIR
echo
echo "================"
echo
SKRYPTY="../skrypty"

# kopia obrabianego pliku aby mieć jego gołą wersję
echo "Kopia zapasowa pliku $ARG"
cp $ARG $ARG.bck && echo "OK"

SFD0=$ARG

# zmiany w pliku źródłowym sfd (kosmetyka)
# zmiana nazwy fontu i font-family
DIRTESTU=`basename "$PWD"`
NAZFONTU="SteMi$DIRTESTU" #nazwa fontu w pliku
$SKRYPTY/zmien-nazwe-fontu.py $SFD0 $NAZFONTU $DIRTESTU && echo "Nazwę fontu zmieniono na $NAZFONTU"

# dołożenie pliku .fea
SFD1=$NAZWA-01-fea.sfd && echo $SFD1
FEAFILE=$NAZWA.fea
$SKRYPTY/dodaj-fea.py $SFD0 $FEAFILE $SFD1 && echo "Dodano features z pliku $FEAFILE"


# usunięcie niepotrzebnych kropek ze znaków (krzyżyk znacznika dla kotwicy)
#80 60 m 25,0,-1
CZESC='80 60 m 25,0,-1' #&& echo $CZESC
SFD2="$NAZWA-02-usgl.sfd" #&& echo $SFD2
#echo "$SKRYPTY/usun-czesc-glifu.sh $SFD1 $CZESC $SFD2"
$SKRYPTY/usun-czesc-glifu.sh "$SFD1" "$CZESC" "$SFD2"


# wygenerowanie fontu
OTF=$NAZWA.otf

SFD3="$NAZWA-03-wyn.sfd"
#echo "$SKRYPTY/generuj-font.py $SFD2 $SFD3 $OTF"
$SKRYPTY/generuj-font.py $SFD2 $SFD3 $OTF

# skopiowanie fontu do ~/.fonts/
cp $OTF $HOME/.fonts/ && echo "Font $OTF został skopiowany do .fonts"
#cp $OTF /home/flamenco/.fonts/ && echo "Font $OTF został skopiowany do .fonts"

# tworzenie pliku testowego SIL
NAZSIL=$NAZWA.sil
if [ -f "$NAZSIL" ]; then
    rm "$NAZSIL"
fi


FONTNAZWA=$($SKRYPTY/nazwa-fontu.py $SFD3) && echo "Nazwa fontu to $FONTNAZWA"
echo "\begin[papersize=a4]{document}" >> $NAZSIL
echo "" >> $NAZSIL
#echo "\font[family=$FONTNAZWA,size=26pt]" >> $NAZSIL
echo "\font[family=$NAZFONTU,size=26pt]" >> $NAZSIL
echo "" >> $NAZSIL
echo "
\use[module=packages.linespacing]
\set[parameter=linespacing.method,value=fixed]
\set[parameter=linespacing.fixed.baselinedistance,value=1.6em]
\define[command=myquad]{\glue[width=1.2em plus 1.2em minus 1.2em]}
\set[parameter=linebreak.hyphenPenalty,value=3000]
\set[parameter=linebreak.tolerance,value=1000]
" >> $NAZSIL
echo "" >> $NAZSIL
echo "k h g m" >> $NAZSIL
echo "gs g s" >> $NAZSIL
echo "" >> $NAZSIL
echo "\end{document}" >> $NAZSIL

# generuję PDF z SIL
sile $NAZSIL

# otwórz wynikowy PDF
#google-chrome $NAZWA.pdf


