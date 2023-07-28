#!/bin/sh

#komitmessage="$USER@$(hostname -s) robi auto-komit z dnia $(date)" #auto wiado dla komita
komitmessage="$USER@$(hostname -s) AUTO-KOMIT $(date)" #auto wiado dla komita
#komitmessage="$USER AUTO-KOMIT $(date)" #auto wiado dla komita
GIT=`which git` #pełna ścieżka do git
# komitujemy
${GIT} add --all . && \
${GIT} commit -m "$komitmessage" && \
${GIT} push origin master
