# Definicje zmiennych
BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
TESTY=$(BASEDIR)/testy
SKRYPTY=$(BASEDIR)/skrypty
GENERUJ_FONTY_PY := generuj_fonty.py
DODAJ_FEA_PY := dodaj_fea.py
USUN_ANCHORY_SH := usun-anchory.sh

# Domyślne cele
.DEFAULT_GOAL := all

# Cele
all: generate_fea_fonts

# Reguła dla generowania czcionek i dodawania atrybutów OpenType
generate_fea_fonts:
    python3 $(DODAJ_FEA_PY) [ścieżka_do_pliku_sfd]
    python3 $(GENERUJ_FONTY_PY) [ścieżka_do_pliku_sfd] [nazwa_zapisanego_pliku_sfd] [nazwa_wygenerowanej_czcionki_otf]
    

# Reguła dla usuwania anchorów
remove_anchors:
    sh $(USUN_ANCHORY_SH) [ścieżka_do_pliku_sfd]

# Wyczyszczenie wygenerowanych plików
clean:
    # Tutaj można dodać polecenia usuwające wygenerowane pliki
