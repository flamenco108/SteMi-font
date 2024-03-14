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
SKRYPTY="../skrypty" && echo "Dir skryptów: $SKRYPTY"

# kopia obrabianego pliku aby mieć jego gołą wersję
echo "Kopia zapasowa pliku $ARG"
cp $ARG $ARG.bck && echo "$ARG zbekapowane OK"

echo
echo "================"
echo


SFD0=$ARG

# zmiany w pliku źródłowym sfd (kosmetyka)
# zmiana nazwy fontu i font-family
DIRTESTU=`basename "$PWD"`
NAZFONTU="SteMi$DIRTESTU" #nazwa fontu w pliku
$SKRYPTY/zmien-nazwe-fontu.py $SFD0 $NAZFONTU $DIRTESTU && echo "Nazwę fontu zmieniono na $NAZFONTU"

# FEA 1 features and lookups
SFD1=$NAZWA-01-fea.sfd #&& echo $SFD1
FEAFILE=$NAZWA.fea
# dołożenie pliku .fea do pliku SFD
# odhaszuj w razie potrzeby i zahaszuj linię niżej
#$SKRYPTY/dodaj-fea.py $SFD0 $FEAFILE $SFD1 && echo "Dodano features z pliku $FEAFILE do pliku $SFD1"
cp $SFD0 $SFD1


# usunięcie niepotrzebnych kropek ze znaków (krzyżyk znacznika dla kotwicy)
#80 60 m 25,0,-1
CZESC='80 60 m 25,0,-1' #&& echo $CZESC
SFD2="$NAZWA-02-usgl.sfd" #&& echo $SFD2
#echo "$SKRYPTY/usun-czesc-glifu.sh $SFD1 $CZESC $SFD2"
$SKRYPTY/usun-czesc-glifu.sh "$SFD1" "$CZESC" "$SFD2"
if [ -z "$(cat $SFD2 | grep "$CZESC")" ]; then
    echo "Linijka $CZESC została usunięta z pliku $SFD2"
fi

echo
echo "---------------"
echo "Generowanie fontu:"


# wygenerowanie fontu
OTF=$NAZWA.otf

SFD3="$NAZWA-03-wyn.sfd"
#echo "$SKRYPTY/generuj-font.py $SFD2 $SFD3 $OTF"
$SKRYPTY/generuj-font.py $SFD2 $SFD3 $OTF
if [ -f "$OTF" ]; then
    echo "---------------"
fi


# FEA 2 features and lookups
# dodawanie fea do pliku OTF (jeżeli nie dodajemy do SFD wyżej)
# jeżeli dodajemy wyżej, to tu zahaszować
$SKRYPTY/dodaj-fea-otf.py $FEAFILE $OTF && echo "Dodano features z pliku $FEAFILE do pliku $OTF"


# skopiowanie fontu do ~/.fonts/
cp $OTF $HOME/.fonts/ && echo "Font $OTF został skopiowany do .fonts"
#cp $OTF /home/flamenco/.fonts/ && echo "Font $OTF został skopiowany do .fonts"

# tworzenie pliku testowego SIL
NAZSIL=$NAZWA.sil
if [ -f "$NAZSIL" ]; then
    rm "$NAZSIL"
fi
# tworzenie pliku testowego TeX
NAZTEX=$NAZWA.tex
if [ -f "$NAZTEX" ]; then
    rm "$NAZTEX"
fi

FONTNAZWA=$($SKRYPTY/nazwa-fontu.py $SFD3) && echo "Nazwa fontu to $FONTNAZWA"


### Tu testowy tekst
TEST=$(<test01.txt)

### do wykasowania
FONT8="\font[family=Liberation Serif,size=12pt]
$TEST
"

SILDOK="\begin[papersize=a4]{document}
\use[module=packages.linespacing]
\set[parameter=linespacing.method,value=fixed]
\set[parameter=linespacing.fixed.baselinedistance,value=1.6em]
\define[command=myquad]{\glue[width=1.2em plus 1.2em minus 1.2em]}
\set[parameter=linebreak.hyphenPenalty,value=3000]
\set[parameter=linebreak.tolerance,value=1000]

\font[family=$NAZFONTU,size=108pt]

$TEST

$FONT8

\end{document}
"
echo "$SILDOK" >> $NAZSIL

TEXDOK="
%!TEX TS-program = xelatex
%!TEX encoding = UTF-8 Unicode

%\documentclass{article}
\documentclass[a4paper, wide, 12pt]{mwart}
%\usepackage[margin=0.5cm]{geometry}
%\usepackage{graphicx}
%\usepackage[document]{ragged2e} % left justify
\tolerance=1 % prevent hyphenation
\emergencystretch=\maxdimen
\hyphenpenalty=10000
\hbadness=10000

\usepackage{fontspec}

\newfontfamily{\fonta}[Scale=8]{$OTF}
\newfontfamily{\fontb}[Scale=1]{Font_8.ttf}

\begin{document}

\huge tst01

{\fonta $TEST }

\end{document}
"
echo "$TEXDOK" >> $NAZTEX


# generuję PDF z SIL
sile $NAZSIL -o $NAZWA-sil.pdf
# generuję PDF z XeLaTeX
#xelatex $NAZTEX

# otwórz wynikowy PDF
#google-chrome $NAZWA.pdf


