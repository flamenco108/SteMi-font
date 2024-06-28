#!/usr/bin/env python3

import sys
import shutil
import fontforge

def open_sfd_file(file_path):
    """
    Opens the specified FontForge SFD file.
    """
    try:
        font = fontforge.open(file_path)
        return font
    except OSError as e:
        print("    Error opening SFD file:", e)
        return None

def detach_references(font):
    """
    Detaches all references in the opened FontForge file.
    Use with caution!!!
    """
    if font is None:
        return None
    print("    DETACHING references...")
    for glyph in font.glyphs():
        glyph.references = []  # Remove all references from the glyph

    return font

def replace_references_with_splines(font):
    """
    Replaces references with splines in the opened FontForge file.
    Use with caution!!!
    """
    if font is None:
        return None
    print("    REPLACING references with splines...")
    for glyph in font.glyphs():
        if glyph.references:
            for reference in glyph.references:
                referenced_glyph_name = reference[0]  # Get the name of the referenced glyph
                referenced_glyph = font[referenced_glyph_name]  # Get the referenced glyph
                # Check if the referenced glyph has splines
                if referenced_glyph.foreground:
                    # Set the splines of the referenced glyph as the splines of the current glyph
                    glyph.foreground = referenced_glyph.foreground

    return font

def remove_overlaps(font):
    """
    Removes overlapping curves and replaces references with curves.
    """
    try:
        print("    REMOVING overlaps and references...")
        font.selection.all()
        print("    -- unlinking references...")
        font.unlinkReferences()
        print("    -- removing overlaps...")
        for glyph in font.glyphs():
            glyph.removeOverlap()
        print("    ...Overlaps and references removed.")
    except Exception as e:
        print(f"    Error removing overlaps and references: {e}")

def simplify_contours(font):
    """
    Simplifies the contours of each glyph in the font.
    """
    try:
        print("    SIMPLIFYING contours...")
        for glyph in font.glyphs():
            glyph.simplify()
        print("    ...Contours simplified.")
    except AttributeError as e:
        print(f"    Error simplifying contours: {e}")

def add_extrema_points(font):
    """
    Adds missing extrema points to all glyphs in the font.
    """
    try:
        print("    ADDING missing extrema points...")
        for glyph in font.glyphs():
            glyph.addExtrema()
        print("    ...Missing extrema points added.")
    except AttributeError as e:
        print(f"    Error adding extrema points: {e}")

def round_to_integer_coordinates(font):
    """
    Rounds all point coordinates to integers.
    """
    try:
        print("    ROUNDING point coordinates to integers...")
        for glyph in font.glyphs():
            for contour in glyph.foreground:
                for point in contour:
                    point.x = int(point.x + 0.5)
                    point.y = int(point.y + 0.5)
        print("    ...Rounding of point coordinates completed.")
    except AttributeError as e:
        print(f"    Error occurred while rounding coordinates: {e}")

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
        print("    ...MaxBearing and MinBearing setting finished.")
    except AttributeError as e:
        print(f"    Error occurred while setting MaxBearing and MinBearing: {e}")

def validate(font):
    """
    Validates the font.
    """
    print("    VALIDATING...")
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
    Saves the opened FontForge file under the specified name.
    """
    if font is None:
        return

    try:
        print("    SAVING SFD file as", file_path)
        font.save(file_path)
        print("    ...SFD file successfully saved as", file_path)
    except OSError as e:
        print("    Error saving SFD file:", e)

def generate_otf_font(font, file_path):
    """
    Generates an OTF font from the opened FontForge file.
    """
    if font is None:
        return

    try:
        print("    GENERATING OTF as", file_path)
        font.generate(file_path)
        print("    ...OTF font successfully generated as", file_path)
    except OSError as e:
        print("    Error generating OTF font:", e)
    except Exception as e:
        print("    General error generating OTF font:", e)

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

def check_missing_glyphs(font):
    """
    Checks for missing essential glyphs in the font.
    """
    required_glyphs = ['space', 'a', 'b', 'c']  # Add more essential glyphs as needed
    missing_glyphs = [glyph for glyph in required_glyphs if glyph not in font]
    if missing_glyphs:
        print("    Missing essential glyphs:", missing_glyphs)
    else:
        print("    All essential glyphs are present.")

def check_glyph_validity(font):
    """
    Validates individual glyphs to identify issues.
    """
    for glyph in font.glyphs():
        errors = glyph.validate()
        if errors:
            print(f"    Validation errors in glyph '{glyph.glyphname}': {errors}")

##############

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python process_sfd.py <input_sfd> <output_sfd> <output_otf>")
        sys.exit(1)

    input_sfd_path = sys.argv[1]
    output_sfd_path = sys.argv[2]
    output_otf_path = sys.argv[3]

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

    ############## ADDITIONAL STEPS AND MODIFICATIONS ---------------
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
    # twice
    part_to_remove = [
        "60 80 m 29,0,-1",
        " 60 40 l 5,1,-1",
        " 40 60 l 5,2,-1",
        " 80 60 l 1029,3,-1"
    ]
    glyphs_to_modify = [ "konCONS","konCONbis","konCON.krzyz" ]
    remove_specific_part_of_glyph_in_sfd(output_sfd_path, glyphs_to_modify, part_to_remove)
    # thrice
    part_to_remove = [ "60 80 m 1049,0,-1" ]
    glyphs_to_modify = [ "konCONS","konCONbis","konCON.krzyz" ]
    remove_specific_part_of_glyph_in_sfd(output_sfd_path, glyphs_to_modify, part_to_remove)

    print("# # # # # # # #\n")
    ##############-----------------

    # Check for missing essential glyphs
    check_missing_glyphs(font)

    # Validate individual glyphs
    check_glyph_validity(font)

    # Simplify contours
    simplify_contours(font)

    # Round to integer coordinates
    round_to_integer_coordinates(font)

    # Remove overlaps
    remove_overlaps(font)

    # Add extrema points
    add_extrema_points(font)

    # Set bearings to zero, excluding certain glyphs
    exclude_glyphs = ["space", "colon", "semicolon"]
    set_bearings_to_zero(font, exclude_glyphs)

    # Validate the font
    validate(font)

    # Save the SFD file
    save_sfd_file(font, output_sfd_path)

    # Generate OTF font
    generate_otf_font(font, output_otf_path)

    # Close the FontForge file
    font.close()
