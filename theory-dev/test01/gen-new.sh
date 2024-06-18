#!/bin/bash

# Check if the required number of arguments is provided
#if [ "$#" -ne 5 ]; then
if [ "$#" -ne 3 ]; then
    #echo "Usage: $0 <txt_tstowy> <plik.sfd> <wynik.sfd> <plik.otf> <plik.fea>"
    echo "Usage: $0 \"<text_testowy>\" <plik.sfd>  <plik.fea>"
    exit 1
fi



# Assign the arguments to variables
#ttxt="$1" #text testowy
#isfd="$2" #wejściowy sfd
#osfd="$3" #wynikowy sfd
#ootf="$4" #wynikowy otf
#fea_file="$5" #plik fea

ttxt="$1" #text testowy
isfd="$2" #wejściowy sfd
fea_file="$3" #plik fea

nazwa=${isfd%.*} && echo "Nazwa (bez rozszerzenia): $nazwa"


# Execute the commands
#../skrypty/generuj-font03.py "$isfd" "$osfd" "$ootf" && \
../skrypty/generuj-font03.py $isfd $nazwa-wyn.sfd $nazwa.otf && \
../skrypty/dodaj-fea-otf.py $fea_file $nazwa.otf && \
echo "" && \
echo "$ttxt" && \
#hb-shape --ned --no-positions "$ootf" "$ttxt" && \
hb-shape --ned --no-positions $nazwa.otf "$ttxt" && \
hb-view -O png $nazwa.otf "$ttxt" > onon.png && \
feh onon.png
