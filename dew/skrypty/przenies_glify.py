#!/usr/bin/env python3

import fontforge, sys

def move_glyphs_forward_in_sfd(input_file, output_file, start_range, end_range, offset):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("StartChar: "):
                parts = line.split()
                next_line = lines[i + 1]
                if next_line.startswith("Encoding:"):
                    encoding_parts = next_line.split()[1:]
                    codepoint1, codepoint2, creation_number = map(int, encoding_parts)
                    if start_range <= codepoint1 < end_range:
                        new_codepoint1 = codepoint1 + offset
                        new_codepoint2 = codepoint2 + offset
                        lines[i + 1] = f"Encoding: {new_codepoint1} {new_codepoint2} {creation_number}\n"
            f.write(line)
            i += 1

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(f"\nScript moving glyphs inside the FontForge sfd file.\n\nUsage: python3 {sys.argv[0]} INPUT_file OUTPUT_file START_range END_range OFFset\n\nexample:\npython3 {sys.argv[0]} input.sfd output.sfd 57600 57700 100")
        sys.exit(1)

if __name__ == "__main__":
#    input_file = "Stemi-01.2-2024.sfd"
#    output_file = "Stemi-01.2a-2024.sfd"
#    start_range = 57680
#    end_range = 57833
#    offset = 50
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    start_range = int(sys.argv[3])
    end_range = int(sys.argv[4])
    offset = int(sys.argv[5])
    #main(input_file, output_file, start_range, end_range, offset)
    move_glyphs_forward_in_sfd(input_file, output_file, start_range, end_range, offset)