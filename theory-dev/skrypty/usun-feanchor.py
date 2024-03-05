#!/usr/bin/env python3

#!/usr/bin/env python3

import fontforge
import sys
import os


def open_sfd_file(input_file):
    """
    Otwiera wskazany plik FontForge SFD.
    """
    try:
        font = fontforge.open(input_file)
        return font
    except fontforge.fontforgeError as e:
        print("OP Błąd podczas otwierania pliku SFD:", e)
        return None


def remove_all_features(font):
    try:
        #if font.gsub_lookups or font.gpos_lookups or font.features:
        if font.gsub_lookups or font.gpos_lookups:
            # Usunięcie wszystkich lookupów
            if font.gsub_lookups or font.gpos_lookups:
                for lookup_type in font.gsub_lookups + font.gpos_lookups:
                    for lookup in lookup_type:
                        font.removeLookup(lookup)
            # Usunięcie wszystkich funkcji OpenType
            if font.features:
                print("RAF font.features")
                for feature in font.features:
                    print("RAF del font.feature")
                    del font[feature]
                
            print("RAF Usunięto wszystkie funkcje z pliku.")
            return font
        else:
            print("RAF Brak funkcji do usunięcia w pliku.")
            return font
    except Exception as e:
        print(f"RAF Wystąpił błąd podczas przetwarzania pliku: {e}")
        #return None
        return font

#def usu_fea(font):
def usu_fea(font):
    if font.gsub_lookups or font.gpos_lookups:
        for lookup in font.gsub_lookups + font.gpos_lookups:
            print(f"USUF lukab {lookup}")
            font.removeLookup(lookup)
            #print("USUF lookup_type")
            #for look in lookup:
            #    font.removeLookup(lookup)
            #    print(f"USUF {lookup} usuniety")
            #for feat in lookup:
            #    font.removeLookup(feature)
            #    print(f"USUF {lookup} usuniety")
        print("USUF if koniec")
#    for glyph in font:
#            for anchor_class in glyph.anchorClasses:
#            print(f"USUF anchor_class {anchor_class}")
#            glyph.removeAnchorClass(anchor_class)
#        for anchor in glyph.anchors:
#            print(f"USUF anchor {anchor}")
#            glyph.removeAnchor(anchor)
        for glyph in font.glyphs():
            if glyph.isWorthOutputting():
                #for anchor_class in glyph.anchorClasses:
                #    print(f"USUF anchor_class worth {anchor_class}")
                #    glyph.removeAnchorClass(anchor_class)
                for anchor in glyph.anchors:
                    print(f"USUF anchor worth {anchor_class}")
                    glyph.removeAnchor(anchor)
        return font
    else:
        print(f"USUF else")
        return font

def remove_lookup(font, lookup_name):
    try:
        lookup = font.findLookup(lookup_name)
        if lookup is not None:
            # Usunięcie kotwic związanych z lookupem
            for anchor_class in lookup.getAnchorClasses():
                for anchor in anchor_class.anchors:
                    anchor.unlinkRef()
                    anchor_class.removeAnchor(anchor)
                font.removeLookup(anchor_class)

            # Usunięcie samego lookupu
            font.removeLookup(lookup)
            print(f"Usunięto lookup '{lookup_name}' i związane z nim kotwice.")
        else:
            print(f"Lookup '{lookup_name}' nie istnieje w czcionce.")
    except Exception as e:
        print(f"Wystąpił błąd podczas usuwania lookupu '{lookup_name}': {e}")


#    font = fontforge.open(font_file_path)
    
#    print("Lookups:")
#    for lookup in font.gpos_lookups + font.gsub_lookups:
#        print(lookup)
#    
#    print("\nFeatures:")
#    for feature in font.gsub_lookups + font.gpos_lookups:
#        print(feature)


def remove_anchor_lines(file_path):
    lines_to_keep = []
    modified_file = file_path + ".modified"
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if not line.strip().startswith('AnchorPoint:'):
                    lines_to_keep.append(line)

        # Zapisanie linii z AnchorPoint do zmodyfikowanego pliku
        with open(modified_file, 'w') as file:
            for line in lines_to_keep:
                file.write(line)
        return modified_file
    except Exception as e:
        print(f"RAN Wystąpił błąd podczas usuwania linii z AnchorPoint: {e}")
        return None


def save_to_output_file(font, output_file):
    try:
        font.generate(output_file)
        font.close()
        print(f"Zapisano do {output_file}.")
    except Exception as e:
        print(f"SAV Wystąpił błąd podczas zapisywania do pliku wyjściowego: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Użycie:", sys.argv[0], " input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    font = open_sfd_file(input_file)
    if font is None:
        sys.exit(1)
    
    #font = remove_all_features(font)
    font = usu_fea(font)
    modified_file = remove_anchor_lines(input_file)
    if modified_file is None:
        sys.exit(1)
    
    save_to_output_file(font, output_file)
    
    # Usunięcie tymczasowego pliku zmodyfikowanego
    os.remove(modified_file)


