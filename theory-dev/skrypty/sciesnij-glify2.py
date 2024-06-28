#!/usr/bin/env python3

import re
import argparse

def read_sfd_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

def write_sfd_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def parse_sfd_file(lines):
    glyphs = {}
    current_glyph = None

    for line in lines:
        if line.startswith("StartChar:"):
            current_glyph = line.split()[1]
            glyphs[current_glyph] = []
        if current_glyph:
            glyphs[current_glyph].append(line)
        if line.startswith("EndChar"):
            current_glyph = None

    return glyphs

def update_glyph_codepoints(glyphs, start_range, end_range):
    codepoint = start_range
    updated_glyphs = {}
    
    # Sort glyphs by their original codepoints
    sorted_glyph_names = sorted(glyphs.keys(), key=lambda g: int(re.search(r'Encoding: (\d+)', ''.join(glyphs[g])).group(1)))

    for glyph_name in sorted_glyph_names:
        if codepoint > end_range:
            break
        glyph_lines = glyphs[glyph_name]
        updated_lines = []
        for line in glyph_lines:
            if line.startswith("Encoding:"):
                parts = line.split()
                new_line = f"{parts[0]} {codepoint} {codepoint} {parts[3]}\n"
                updated_lines.append(new_line)
                codepoint += 1
            else:
                updated_lines.append(line)
        updated_glyphs[glyph_name] = updated_lines

    return updated_glyphs

def combine_sfd_file(lines, updated_glyphs):
    combined_lines = []
    current_glyph = None

    for line in lines:
        if line.startswith("StartChar:"):
            current_glyph = line.split()[1]
        if current_glyph and current_glyph in updated_glyphs:
            combined_lines.extend(updated_glyphs[current_glyph])
            current_glyph = None
            while not line.startswith("EndChar"):
                line = next(lines)
        else:
            combined_lines.append(line)
        if line.startswith("EndChar"):
            current_glyph = None

    return combined_lines

def main(input_file, output_file, start_range, end_range):
    lines = read_sfd_file(input_file)
    glyphs = parse_sfd_file(lines)
    updated_glyphs = update_glyph_codepoints(glyphs, start_range, end_range)
    combined_lines = combine_sfd_file(iter(lines), updated_glyphs)
    write_sfd_file(output_file, combined_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reorder glyphs in SFD file by codepoint")
    parser.add_argument("input_file", help="Input SFD file")
    parser.add_argument("output_file", help="Output SFD file")
    parser.add_argument("start_range", type=int, help="Start range for codepoints")
    parser.add_argument("end_range", type=int, help="End range for codepoints")
    args = parser.parse_args()

    main(args.input_file, args.output_file, args.start_range, args.end_range)
