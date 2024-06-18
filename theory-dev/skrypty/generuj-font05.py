#!/usr/bin/env python3

import re
import sys
import shutil
import fontforge

def open_sfd_file(file_path):
    """
    Otwiera wskazany plik FontForge SFD.
    """
    try:
        font = fontforge.open(file_path)
        return font
    except fontforge.fontforgeError as e:
        print("    Błąd podczas otwierania pliku SFD:", e)
        return None

def detach_references(font):
    """
    Odłącza wszystkie referencje w otwartym pliku FontForge.
    Nie używaj bez potrzeby!!!
    """
    if font is None:
        return None
    print("    ODŁĄCZAMY referencje...")
    for glyph in font.glyphs():
        glyph.references = []  # Usuń wszystkie referencje z glifu

    return font

def replace_references_with_splines(font):
    """
    Zamienia referencje w spline w otwartym pliku FontForge.
    Nie używaj bez potrzeby!!!
    """
    if font is None:
        return None
    print("    ZAMIENIAMY referencje w spline...")
    for glyph in font.glyphs():
        if glyph.references:
            for reference in glyph.references:
                referenced_glyph_name = reference[0]  # Pobierz nazwę referencjonowanego glifu
                referenced_glyph = font[referenced_glyph_name]  # Pobierz referencjonowany glif
                # Sprawdź, czy referencjonany glif ma spline
                if referenced_glyph.foreground:
                    # Ustaw spline referencjonowanego glifu jako spline bieżącego glifu
                    glyph.foreground = referenced_glyph.foreground

    return font

def remove_overlaps(font):
    """
    Usuwa przecinające się krzywe i zamienia referencje na krzywe.
    """
    try:
        print("    USUWAMY przecinające się krzywe i referencje...")
        font.selection.all()
        print("    -- usuwamy referencje...")
        font.unlinkReferences()
        print("    -- usuwamy przecinające się krzywe...")
        for glyph in font.glyphs():
            glyph.removeOverlap()
        print("    ...Przecinające się krzywe i referencje zostały usunięte.")
    except Exception as e:
        print(f"    Wystąpił błąd podczas usuwania przecinających się krzywych i referencji: {e}")

def simplify_contours(font):
    """
    Ma uprościć kontury każdego znaku w czcionce.
    """
    try:
        print("    UPRASZCZAMY kontury...")
        for glyph in font.glyphs():
            glyph.simplify()
        print("    ...Kontury zostały uproszczone.")
    except AttributeError as e:
        print(f"    Wystąpił błąd podczas upraszczania konturów: {e}")

def add_extrema_points(font):
    """
    Dodaje brakujące punkty ekstremalne do wszystkich znaków w czcionce.
    """
    try:
        print("    DODAJEMY brakujące punkty ekstremalne...")
        for glyph in font.glyphs():
            # -- Add all missing extrema points
            #glyph.addExtrema("all")
            # -- Add extrema points only on longer splines (relative to the em-size)
            #glyph.addExtrema("only_good")
            # -- Add extrema points on longer splines and merge nearby on-curve points
            #glyph.addExtrema("only_good_rm")
            # -- Add extrema points without flags
            glyph.addExtrema()
        print("    ...Dodano brakujące punkty ekstremalne.")
    except AttributeError as e:
        print(f"    Wystąpił błąd podczas dodawania punktów ekstremalnych: {e}")

#def round_to_integer_coordinates(font):
#    """
#    Zaokrągla wszystkie współrzędne punktów do liczb całkowitych.
#    """
#    try:
#        print("    ZAOKRĄGLAMY współrzędne punktów do liczb całkowitych...")
#        for glyph in font.glyphs():
#            for contour in glyph.foreground:
#                for segment in contour.segments:
#                    for point in segment:
#                        point.x = int(point.x + 0.5)
#                        point.y = int(point.y + 0.5)
#        print("    ...Współrzędne punktów zostały zaokrąglone do całkowitych.")
#    except AttributeError as e:
#        print(f"    Wystąpił błąd podczas zaokrąglania współrzędnych: {e}")

def round_to_integer_coordinates(font):
    """
    Rounds all point coordinates to integers.
    """
    try:
        print("    ZAOKRĄGLAMY współrzędne punktów do liczb całkowitych...")
        for glyph in font.glyphs():
            for contour in glyph.foreground:
                for point in contour:
                    point.x = int(point.x + 0.5)
                    point.y = int(point.y + 0.5)
        print("    ...ZAOKRĄGLANIE współrzędnych zakończone.")
    except AttributeError as e:
        print(f"    Error occurred while rounding coordinates: {e}")


#def set_bearings_to_zero(font):
#    """
#    Ustawia MaxBearing i MinBearing na zero dla wszystkich glifów.
#    """
#    try:
#        print("    USTAWIAM MaxBearing i MinBearing na zero...")
#        for glyph in font.glyphs():
#            glyph.left_side_bearing = 0
#            glyph.right_side_bearing = 0
#        print("    ...MaxBearing i MinBearing zostały ustawione na zero.")
#    except AttributeError as e:
#        print(f"    Wystąpił błąd podczas ustawiania MaxBearing i MinBearing: #    {e}")

def set_bearings_to_zero(font, exclude_glyphs=[]):
    """
    Sets MaxBearing and MinBearing to zero for all glyphs except those in the exclude_glyphs list.
    """
    try:
        print("    SETTING MaxBearing and MinBearing to zero...")
        for glyph in font.glyphs():
            if glyph.glyphname not in exclude_glyphs:
                glyph.left_side_bearing = 0
                glyph.right_side_bearing = 0
                #print(f"    Set bearings to zero for glyph '{glyph.glyphname}'")
            else:
                print(f"    Skipping glyph '{glyph.glyphname}' (excluded from bearing reset)")
        print("    ...SETTING MaxBearing and MinBearing to zero FINISHED.")
    except AttributeError as e:
        print(f"    Error occurred while setting MaxBearing and MinBearing: {e}")


def validate(font):
    """
    Ma dokonać walidacji
    """
    print("    WALIDUJEM...")
    errors = font.validate()
    if isinstance(errors, int):
        if errors > 0:
            print(f"    Validation errors: {errors}")
    else:
        print("    Validation errors:")
        for error in errors:
            print(error)

def save_sfd_file(font, file_path):
    """
    Zapisuje otwarty plik FontForge pod wskazaną nazwą.
    """
    if font is None:
        return

    try:
        print("    ZAPISUJEMY plik SFD jako", file_path)
        font.save(file_path)
        print("    ...Plik SFD został pomyślnie zapisany jako", file_path)
    except fontforge.fontforgeError as e:
        print("    Błąd podczas zapisywania pliku SFD:", e)

def generate_otf_font(font, file_path):
    """
    Generuje czcionkę OTF na podstawie otwartego pliku FontForge.
    """
    if font is None:
        return

    try:
        print("    GENERUJEMY OTF jako", file_path)
        font.generate(file_path)
        print("    ...Czcionka OTF została pomyślnie wygenerowana jako", file_path)
    except fontforge.fontforgeError as e:
        print("    Błąd podczas generowania czcionki OTF:", e)

def remove_specific_part_of_glyph_in_sfd(sfd_path, glyph_names, part_to_remove):
    """
    Removes a specific part of particular glyphs in the SFD file.
    """
    part_to_remove_lines = [line + '\n' for line in part_to_remove]

    with open(sfd_path, 'r') as file:
        lines = file.readlines()

    for glyph_name in glyph_names:
        print(f"    REMOVING part '{part_to_remove}' from GLYPH '{glyph_name}'...")

        start_index = None
        end_index = None
        glyph_start = f"StartChar: {glyph_name}"
        glyph_end = "EndChar"

        # Find the start and end indices of the glyph definition
        for i, line in enumerate(lines):
            if line.strip() == glyph_start:
                start_index = i
            if line.strip() == glyph_end and start_index is not None:
                end_index = i
                break

        if start_index is not None and end_index is not None:
            glyph_to_modify = lines[start_index:end_index+1]

            # Check if part_to_remove exists before removal
            part_found = any(line in glyph_to_modify for line in part_to_remove_lines)
            if not part_found:
                print(f"          NOT FOUND part in GLYPH '{glyph_name}'.")
                continue

            # Remove the specified part from the glyph definition
            modified_glyph = []
            part_found = False
            for line in glyph_to_modify:
                if line in part_to_remove_lines:
                    if not part_found:
                        part_found = True
                else:
                    if part_found:
                        part_found = False
                    modified_glyph.append(line)

            # Replace the original glyph definition with the modified one
            lines[start_index:end_index+1] = modified_glyph

            # Check if part_to_remove still exists after removal
            glyph_after_removal = lines[start_index:end_index+1]
            part_still_exists = any(line in glyph_after_removal for line in part_to_remove_lines)
            if part_still_exists:
                print(f"      ...Part '{part_to_remove}' still exists in glyph '{glyph_name}' after removal.")
            else:
                print(f"    ...REMOVED part from '{glyph_name}' in SFD file.")
        else:
            print(f"    Glyph '{glyph_name}' not found in SFD file.")

    with open(sfd_path, 'w') as file:
        file.writelines(lines)


##############

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Użycie:", sys.argv[0], "[ścieżka_do_pliku_sfd] [nazwa_wynikowego_pliku_sfd] [nazwa_wygenerowanej_czcionki_otf]")
        sys.exit(1)

    input_sfd_path = sys.argv[1]
    output_sfd_path = sys.argv[2]
    output_otf_path = sys.argv[3]

    # Skopiuj plik SFD
    try:
        print(f"    KOPIUJEMY plik {input_sfd_path} do {output_sfd_path}.")
        shutil.copy(input_sfd_path, output_sfd_path)
        print(f"    Plik {input_sfd_path} został skopiowany do {output_sfd_path}.")
    except IOError as e:
        print(f"    Błąd podczas kopiowania pliku: {e}")
        sys.exit(1)

    ##############-----------------
    ### USUWANIE krzyżyka z glifów
    ##############-----------------
    print("\n# # # # # # # #")
    # raz
    part_to_remove = [
        " 60 80 m 25,0,-1",
        " 60 40 l 1,1,-1",
        " 40 60 l 1,2,-1",
        " 80 60 l 1025,3,-1"
    ]
    glyphs_to_modify = [ "konCONS","konCONbis","konCON.krzyz" ]
    remove_specific_part_of_glyph_in_sfd(output_sfd_path, glyphs_to_modify, part_to_remove)
    # dwa
    part_to_remove = [
        "60 80 m 29,0,-1",
        " 60 40 l 5,1,-1",
        " 40 60 l 5,2,-1",
        " 80 60 l 1029,3,-1"
    ]
    glyphs_to_modify = [ "konCONS","konCONbis","konCON.krzyz" ]
    remove_specific_part_of_glyph_in_sfd(output_sfd_path, glyphs_to_modify, part_to_remove)
    # trzy
    part_to_remove = [ "60 80 m 1049,0,-1" ]
    glyphs_to_modify = [ "konCONS","konCONbis","konCON.krzyz" ]
    remove_specific_part_of_glyph_in_sfd(output_sfd_path, glyphs_to_modify, part_to_remove)

    print("# # # # # # # #\n")
    ##############-----------------


    # Otwórz skopiowany plik SFD
    font = open_sfd_file(output_sfd_path)

    # Dodaj ekstrema
    #add_extrema_points(font)
    # Uprość kontury
    simplify_contours(font)



    # Zaokrąglij do pełnych wartości
    round_to_integer_coordinates(font)

    # Usuń referencje oraz przecinające się krzywe
    remove_overlaps(font)

    # Dodaj ekstrema
    add_extrema_points(font)

    # Ustaw MaxBearing i MinBearing na zero
    # wylistuj glify, które nie mają mieć odsadek na zero
    #set_bearings_to_zero(font)
    exclude_glyphs = ["space", "colon", "semicolon"]
    set_bearings_to_zero(font, exclude_glyphs)

    # Zwaliduj
    validate(font)

    # Zapisz plik SFD
    save_sfd_file(font, output_sfd_path)

    # Wygeneruj czcionkę OTF
    generate_otf_font(font, output_otf_path)

    # Zamknij plik FontForge
    font.close()
