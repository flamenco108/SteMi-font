#!/bin/sh

komitmessage="auto-commit from $USER@$(hostname -s) on $(date)" #auto wiado dla komita
GIT=`which git` #pełna ścieżka do git
# komitujemy
${GIT} add --all . && \
${GIT} commit -m "$komitmessage" && \
${GIT} push origin master
