#!/usr/bin/env python3

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

def round_to_integer_coordinates(font):
    """
    Zaokrągla wszystkie współrzędne punktów do liczb całkowitych.
    """
    try:
        print("    ZAOKRĄGLAMY współrzędne punktów do liczb całkowitych...")
        for glyph in font.glyphs():
            for contour in glyph.foreground:
                for segment in contour.segments:
                    for point in segment:
                        point.x = int(point.x + 0.5)
                        point.y = int(point.y + 0.5)
        print("    ...Współrzędne punktów zostały zaokrąglone do całkowitych.")
    except AttributeError as e:
        print(f"    Wystąpił błąd podczas zaokrąglania współrzędnych: {e}")

def set_bearings_to_zero(font):
    """
    Ustawia MaxBearing i MinBearing na zero dla wszystkich glifów.
    """
    try:
        print("    USTAWIAM MaxBearing i MinBearing na zero...")
        for glyph in font.glyphs():
            glyph.left_side_bearing = 0
            glyph.right_side_bearing = 0
        print("    ...MaxBearing i MinBearing zostały ustawione na zero.")
    except AttributeError as e:
        print(f"    Wystąpił błąd podczas ustawiania MaxBearing i MinBearing: {e}")

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

    # Otwórz skopiowany plik SFD
    font = open_sfd_file(output_sfd_path)

    # Dodaj ekstrema
    #add_extrema_points(font)
    # Uprość kontury
    simplify_contours(font)

    # Usuń przecinające się krzywe
    remove_overlaps(font)

    # Zaokrąglij do pełnych wartości
    round_to_integer_coordinates(font)

    # Dodaj ekstrema
    add_extrema_points(font)

    # Ustaw MaxBearing i MinBearing na zero
    set_bearings_to_zero(font)

    # Zwaliduj
    validate(font)

    # Zapisz plik SFD
    save_sfd_file(font, output_sfd_path)

    # Wygeneruj czcionkę OTF
    generate_otf_font(font, output_otf_path)

    # Zamknij plik FontForge
    font.close()
