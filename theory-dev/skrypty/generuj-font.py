#!/usr/bin/env python3


import sys
import fontforge

def open_sfd_file(file_path):
    """
    Otwiera wskazany plik FontForge SFD.
    """
    try:
        font = fontforge.open(file_path)
        return font
    except fontforge.fontforgeError as e:
        print("Błąd podczas otwierania pliku SFD:", e)
        return None


def detach_references(font):
    """
    Odłącza wszystkie referencje w otwartym pliku FontForge.
    Nie używaj bez potrzeby!!!
    """
    if font is None:
        return None

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
        font.selection.all()
        font.unlinkReferences()
        for glyph in font.glyphs():
            glyph.removeOverlap()
        print("Przecinające się krzywe i referencje zostały usunięte.")
    except Exception as e:
        print(f"Wystąpił błąd podczas usuwania przecinających się krzywych i referencji: {e}")


#def simplify_contours(font):
#    """
#    Ma uprościć kontury
#    """
#    for glyph in font:
#        glyph.simplify()

def simplify_contours(font):
    """
    Ma uprościć kontury każdego znaku w czcionce.
    """
    try:
        for glyph in font.glyphs():
            glyph.simplify()
        print("Kontury zostały uproszczone.")
    except AttributeError as e:
        print(f"Wystąpił błąd podczas upraszczania konturów: {e}")


#def add_extrema_points(font):
#    """
#    Ma dodać brakujące ekstrema
#    """
#    for glyph in font:
#        glyph.addExtrema()

def add_extrema_points(font):
    """
    Dodaje brakujące punkty ekstremalne do wszystkich znaków w czcionce.
    """
    try:
        for glyph in font.glyphs():
            glyph.addExtrema()
        print("Dodano brakujące punkty ekstremalne.")
    except AttributeError as e:
        print(f"Wystąpił błąd podczas dodawania punktów ekstremalnych: {e}")


def round_to_integer_coordinates(font):
    """
    Zaokrągla wszystkie współrzędne punktów do liczb całkowitych.
    """
    try:
        for glyph in font.glyphs():
            for contour in glyph.foreground:
                for segment in contour.segments:
                    for point in segment:
                        point.x = int(point.x + 0.5)
                        point.y = int(point.y + 0.5)
        print("Współrzędne punktów zostały zaokrąglone do liczb całkowitych.")
    except AttributeError as e:
        print(f"Wystąpił błąd podczas zaokrąglania współrzędnych: {e}")



#def round_to_integer_coordinates(font):
#    """
#    Ma zaokrąglić do pełnych wartości współrzędnych
#    """
#    for glyph in font:
#        for contour in glyph:
#            for point in contour:
#                point.x = int(point.x + 0.5)
#                point.y = int(point.y + 0.5)




#def validate(font):
#    """
#    Ma dokonać walidacji
#    """
#    errors = font.validate()
#    if errors:
#        print("Validation errors:")
#        for error in errors:
#            print(error)

def validate(font):
    """
    Ma dokonać walidacji
    """
    errors = font.validate()
    if isinstance(errors, int):
        if errors > 0:
            print(f"Validation errors: {errors}")
    else:
        print("Validation errors:")
        for error in errors:
            print(error)



def save_sfd_file(font, file_path):
    """
    Zapisuje otwarty plik FontForge pod wskazaną nazwą.
    """
    if font is None:
        return

    try:
        font.save(file_path)
        print("Plik SFD został pomyślnie zapisany jako", file_path)
    except fontforge.fontforgeError as e:
        print("Błąd podczas zapisywania pliku SFD:", e)

def generate_otf_font(font, file_path):
    """
    Generuje czcionkę OTF na podstawie otwartego pliku FontForge.
    """
    if font is None:
        return

    try:
        font.generate(file_path)
        print("Czcionka OTF została pomyślnie wygenerowana jako", file_path)
    except fontforge.fontforgeError as e:
        print("Błąd podczas generowania czcionki OTF:", e)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        #print("Użycie: python script.py [ścieżka_do_pliku_sfd] [nazwa_zapisanego_pliku_sfd] [nazwa_wygenerowanej_czcionki_otf]")
        print("Użycie:", sys.argv[0], "[ścieżka_do_pliku_sfd] [nazwa_wynikowego_pliku_sfd] [nazwa_wygenerowanej_czcionki_otf]")
        sys.exit(1)

    input_sfd_path = sys.argv[1]
    output_sfd_path = sys.argv[2]
    output_otf_path = sys.argv[3]

    # Otwórz plik SFD
    font = open_sfd_file(input_sfd_path)

    # Zamień referencje w spline
    # UWAGA!!! Raczej zbędne
    #font = replace_references_with_splines(font)

    # Odłącz wszystkie referencje w otwartym pliku FontForge.
    #UWAGA!!! Raczej zbędne
    #font = detach_references(font):

    # Usuń przecinające się krzywe
    remove_overlaps(font)
    # Uprość kontury
    simplify_contours(font)
    # Dodaj ekstrema
    add_extrema_points(font)
    # Zaokrąglij do pełnych wartości
    round_to_integer_coordinates(font)
    # Zwaliduj
    validate(font)


    # Zapisz plik SFD
    save_sfd_file(font, output_sfd_path)

    # Wygeneruj czcionkę OTF
    generate_otf_font(font, output_otf_path)

    # Zamknij plik FontForge
    font.close()
