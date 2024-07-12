#!/bin/bash

# Domyślna wiadomość komitu
default_message="$USER@$(hostname -s) AUTO-KOMIT $(date)"

# Funkcja do odliczania czasu
countdown() {
    local seconds=$1
    while [ $seconds -gt 0 ]; do
        echo -ne "\rCzas na wprowadzenie wiadomości: $seconds s "
        sleep 1
        : $((seconds--))
    done
    echo
}

# Prośba o wprowadzenie wiadomości komitu
echo "Wprowadź wiadomość komitu (lub naciśnij Enter dla domyślnej wiadomości):"
echo "Domyślna wiadomość: $default_message"

# Uruchomienie odliczania w tle
countdown 30 &
countdown_pid=$!

# Oczekiwanie na input użytkownika z timeoutem
read -t 30 komitmessage

# Zatrzymanie procesu odliczania
kill $countdown_pid 2>/dev/null

# Jeśli użytkownik nie wprowadził niczego, użyj domyślnej wiadomości
if [ -z "$komitmessage" ]; then
    komitmessage="$default_message"
fi

GIT=$(which git)

# Komitowanie zmian
$GIT add --all . && \
$GIT commit -m "$komitmessage" && \
$GIT push origin theory-dev
