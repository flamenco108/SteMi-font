#!/usr/bin/env python3

import sys
import re

def replace_strings(file_path, gloski_do_zmiany, gloski_zmienione):
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()

        for i, regex_pattern in enumerate(gloski_do_zmiany):
            if i < len(gloski_zmienione):
                replacement_string = gloski_zmienione[i]
                file_contents = re.sub(regex_pattern, lambda match: match.group(1) + replacement_string, file_contents)

        return file_contents

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Example lists
    gloski_do_zmiany = [
                        'cz', 'sz', 'ch',
                        'szcz',
                        'ó', 
                        'dz', 'dż', 'dź',
                        'civa', 'civi', 'civo', 'civu', 
                        'ciga',
                        'cifa,' 'cife', 'cifi', 'cife', 'cifu', 'cifo',
                        'cił', 'cia', 'cią', 'cie', 'cię' 'cio', 'ciu', 
                        'ci',
                        'zia', 'zią', 'zie', 'zię' 'zio', 'ziu', 'ził', 
                        'zić',
                        'sia', 'sią', 'sie', 'się' 'sio', 'siu', 'sił', 
                        'sić',
                        'ścia', 'ścią', 'ście', 'ścię' 'ścio', 'ściu', 'ścił',
                        'ścić',
                        'ść', # (ś, ć, ź nie wymaga konwersji)
                         # zamiana 'rz' na 'ż' z wyjątkami
                         r'(^|[^zmnp])(rz)(?![zmnp])',
                        #'zarzn', 'marzn', 'narzn', # [zmn]arznie
                        #'marzł', 'perzł', # marzł superzłoczyńca
                        #'mierzn', 'mierzł', 'nierzn', 'mierzi', # [mn]ierz[nł]
                        #'zerzn', 'werzn', 'perzn', 'derzn', 'berzn', # o[wzbd]erznie superznawca
                        ]
    gloski_zmienione = [
                        'č', 'š', 'h',
                        'ƌ', #szcz
                        'u', 
                        'ʒ', 'ǯ', 'd̦',
                        'ciwa', 'ciwi', 'ciwo', 'ciwu',
                        'ciga',
                        'cifa', 'cife', 'cifi', 'cife', 'cifu', 'cifo',
                        'ćł', 'ća', 'ćą', 'će', 'ćę', 'ćo', 'ću', # ci
                        'ći',
                        'źa', 'źą', 'źe', 'źę', 'źo', 'źu', 'źł',  # zi
                        'źić',
                        'śa', 'śą', 'śe', 'śę', 'śo', 'śu', 'śł', 'śić',  # si
                        'śić', 
                        'əa', 'əą', 'əe', 'əę', 'əo', 'əu', 'əł', 'əć',  # ści
                        'əić',
                        'ə', # ść
                         # zamiana 'rz' na 'ż' z wyjątkami
                         '\\1ż\\2',
                        #'zarzn', 'marzn', 'narzn', # [zmn]arznie
                        #'marzł', 'perzł', # marzł superzłoczyńca
                        #'mierzn', 'mierzł', 'nierzn', 'mierźi', # [mn]ierz[nł]
                        #'zerzn', 'werzn', 'perzn', 'derzn', 'berzn', # o[wzbd]erznie superznawca
                        ]

    replaced_contents = replace_strings(file_path, gloski_do_zmiany, gloski_zmienione)

    if replaced_contents:
        print(replaced_contents)