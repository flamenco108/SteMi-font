#!/usr/bin/env python3

import fontforge
import sys
import shutil
import traceback
import os

def open_sfd_file(path):
    try:
        font = fontforge.open(path)
        return font
    except Exception as e:
        print(f"Error opening SFD file '{path}': {e}")
        return None

def detach_references(font):
    for glyph in font.glyphs():
        if glyph.references:
            glyph.unlinkRef()
    print("References detached.")
    return font

def replace_references_with_splines(font):
    for glyph in font.glyphs():
        glyph.references = []
    print("References replaced with splines.")
    return font

def remove_specific_part_of_glyph_in_sfd(sfd_path, glyph_names, parts_to_remove):
    with open(sfd_path, 'r') as file:
        lines = file.readlines()

    with open(sfd_path, 'w') as file:
        skip_lines = False
        for line in lines:
            if any(glyph in line for glyph in glyph_names):
                if any(part in line for part in parts_to_remove):
                    skip_lines = True
                else:
                    skip_lines = False
            if not skip_lines:
                file.write(line)

def check_missing_glyphs(font):
    essential_glyphs = ["space", "A", "a", "zero"]
    missing_glyphs = [glyph for glyph in essential_glyphs if glyph not in font]
    if missing_glyphs:
        print(f"Missing essential glyphs: {', '.join(missing_glyphs)}")
        sys.exit(1)
    else:
        print("All essential glyphs are present.")

def check_glyph_validity(font):
    for glyph in font.glyphs():
        errors = glyph.validate()
        if errors:
            print(f"Validation errors in glyph '{glyph.glyphname}': {errors}")

def simplify_contours(font):
    for glyph in font.glyphs():
        glyph.simplify()
    print("Contours simplified.")

def round_to_integer_coordinates(font):
    for glyph in font.glyphs():
        glyph.round()
    print("Rounding of point coordinates completed.")

def remove_overlaps(font):
    for glyph in font.glyphs():
        glyph.removeOverlap()
    print("Overlaps and references removed.")

def add_extrema_points(font):
    for glyph in font.glyphs():
        try:
            glyph.addExtrema()
        except Exception as e:
            print(f"Error adding extrema points to glyph '{glyph.glyphname}': {e}")
    print("Missing extrema points added.")

def set_bearings_to_zero(font, exclude_glyphs):
    for glyph in font.glyphs():
        if glyph.glyphname not in exclude_glyphs:
            glyph.left_side_bearing = 0
            glyph.right_side_bearing = 0
    print("MaxBearing and MinBearing setting finished.")

def validate(font):
    validation_errors = font.validate()
    if validation_errors:
        print(f"Validation errors: {validation_errors}")

def log_validation_errors(font):
    validation_log = "validation_errors.log"
    with open(validation_log, "w") as log_file:
        for glyph in font.glyphs():
            errors = glyph.validate()
            if errors:
                log_file.write(f"Validation errors in glyph '{glyph.glyphname}': {errors}\n")
    print(f"Validation errors logged to {validation_log}")

def simplify_and_fix_splines(font):
    for glyph in font.glyphs():
        glyph.correctDirection()
        glyph.removeOverlap()
        glyph.simplify()
        glyph.round()

def process_glyphs_individually(font):
    for glyph in font.glyphs():
        print(f"Processing glyph: {glyph.glyphname}")
        glyph.correctDirection()
        glyph.removeOverlap()
        glyph.simplify()
        glyph.round()
        try:
            glyph.addExtrema()
        except Exception as e:
            print(f"Error adding extrema to glyph '{glyph.glyphname}': {e}")
        errors = glyph.validate()
        if errors:
            print(f"Validation errors in glyph '{glyph.glyphname}': {errors}")

def save_sfd_file(font, path):
    font.save(path)
    print(f"SFD file successfully saved as {path}")

def generate_otf_font(font, path):
    try:
        font.generate(path)
        print(f"OTF file successfully generated as {path}")
    except Exception as e:
        print(f"Error generating OTF font: {e}")
        with open("generate_otf_error.log", "w") as log_file:
            log_file.write(f"Error generating OTF font: {e}\n")
            traceback.print_exc(file=log_file)
        # Additional logging for detailed error
        for glyph in font.glyphs():
            try:
                font.generate(path, flags=("short-post",))
            except Exception as glyph_error:
                print(f"Error generating OTF font with glyph '{glyph.glyphname}': {glyph_error}")
                with open("generate_otf_error.log", "a") as log_file:
                    log_file.write(f"Error generating OTF font with glyph '{glyph.glyphname}': {glyph_error}\n")
                    traceback.print_exc(file=log_file)
                break

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python process_sfd.py <input_sfd> <output_sfd> <output_otf>")
        sys.exit(1)

    input_sfd_path = sys.argv[1]
    output_sfd_path = sys.argv[2]
    output_otf_path = sys.argv[3]

    # Check if output directory exists, if not, create it
    output_dir = os.path.dirname(output_sfd_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_dir = os.path.dirname(output_otf_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Copy the input SFD file to the output SFD path
    shutil.copy(input_sfd_path, output_sfd_path)

    # Open the copied SFD file
    font = open_sfd_file(output_sfd_path)
    if font is None:
        sys.exit(1)

    # Detach references
    font = detach_references(font)

    # Replace references with splines
    font = replace_references_with_splines(font)

    print("# # # # # # # #\n")

    # Perform additional steps or modifications here
    to_modify = [ "konCONS","konCONbis","konCON.krzyz" ]
    part_to_remove = [
        "60 80 m 1049,0,-1",
        " 60 80 l 1090,1,-1",
        " 60 40 l 1112,2,-1",
        " 40 60 l 1150,3,-1"
    ]
    glyphs_to_modify = [ "konCONS","konCONbis","konCON.krzyz" ]
    remove_specific_part_of_glyph_in_sfd(output_sfd_path, glyphs_to_modify, part_to_remove)
    part_to_remove = [
        "60 80 m 29,0,-1",
        " 60 40 l 5,1,-1",
        " 40 60 l 5,2,-1",
        " 80 60 l 1029,3,-1"
    ]
    glyphs_to_modify = [ "konCONS","konCONbis","konCON.krzyz" ]
    remove_specific_part_of_glyph_in_sfd(output_sfd_path, glyphs_to_modify, part_to_remove)
    part_to_remove = [ "60 80 m 1049,0,-1" ]
    glyphs_to_modify = [ "konCONS","konCONbis","konCON.krzyz" ]
    remove_specific_part_of_glyph_in_sfd(output_sfd_path, glyphs_to_modify, part_to_remove)

    print("# # # # # # # #\n")

    # Check for missing essential glyphs
    check_missing_glyphs(font)

    # Validate individual glyphs
    check_glyph_validity(font)

    # Simplify and fix splines
    simplify_and_fix_splines(font)

    # Process glyphs individually
    process_glyphs_individually(font)

    # Simplify contours
    simplify_contours(font)

    # Round point coordinates to integers
    round_to_integer_coordinates(font)

    # Remove overlaps
    remove_overlaps(font)

    # Add missing extrema points
    add_extrema_points(font)

    # Set MaxBearing and MinBearing to zero
    exclude_glyphs = ["space", "colon", "semicolon"]
    set_bearings_to_zero(font, exclude_glyphs)

    # Validate the font
    validate(font)

    # Log validation errors
    log_validation_errors(font)

    # Save the processed SFD file
    save_sfd_file(font, output_sfd_path)

    # Generate OTF font
    generate_otf_font(font, output_otf_path)
