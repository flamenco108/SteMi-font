#!/usr/bin/env python3

import sys
import re

# Define transformation rules
transformation_rules = [
    (r'zerzn', 'zerżn'),
    (r'werzn', 'werżn'),
    (r'derzn', 'derżn'),
    (r'berzn', 'berżn'),
    (r'narzn', 'narżn'),
    (r'zarzn', 'zarżn'),
    (r'nierzn', 'nierżn'),
    (r'szcz', 'ƌ'),
    (r'ó', 'u'),
    (r'cz', 'č'),
    (r'sz', 'š'),
    (r'ch', 'h'),
    (r'dz', 'ʒ'),
    (r'dż', 'ǯ'),
    (r'dź', 'd̦'),
    (r'ść', 'ə'),
    (r'rz', 'ż'),
    (r'prz|psz', 'pš'),
    (r'krz|ksz', 'kš'),
    (r'chrz|hrz|chsz|hsz', 'hš'),
    (r'trz|tsz', 'tš'),
    (r'fsz|frz', 'fš'),
    (r'pszcz', 'pƌ'),
    (r'trzcza|tszcza', 'tšč'),
    (r'ci$', 'ći'),
    (r'si$', 'śi'),
    (r'zi$', 'źi'),
    (r'ści$', 'əi'),
    (r'dzi$', 'd̦i'),
    (r'cić|cici([aąeęouóy])', r'ćić\1'),
    (r'sić|sici([aąeęouóy])', r'śić\1'),
    (r'zić|zici([aąeęouóy])', r'źić\1'),
    (r'ścić|ścici([aąeęouóy])', r'əić\1'),
    (r'dzić|dzici([aąeęouóy])', r'd̦ić\1'),
    (r'ci([sśzżźcćvwdtfrgbhnmjklłp])', r'ći\1'),
    (r'si([sśzżźcćvwdtfrgbhnmjklłp])', r'śi\1'),
    (r'zi([sśzżźcćvwdtfrgbhnmjklłp])', r'źi\1'),
    (r'ści([sśzżźcćvwdtfrgbhnmjklłp])', r'əi\1'),
    (r'śći([sśzżźcćvwdtfrgbhnmjklłp])', r'əi\1'),
    (r'd̦i([sśzżźcćvwdtfrgbhnmjklłp])', r'ći\1'),
    (r'civa', 'ciwa'),
    (r'civi', 'ciwi'),
    (r'civo', 'ciwo'),
    (r'civu', 'ciwu'),
    (r'v', 'w'),
]

# Define pre-transformation rules for -b flag
pre_b_rules = [
    (r'prz|psz', 'ƥ'),
    (r'krz|ksz', 'ǩ'),
    (r'chrz|hrz|chsz|hsz', 'ȟ'),
    (r'frz|fsz', 'ƒ'),
    (r'tsz|trz', 'ť'),
    (r'pś', 'п'),
    (r'psi', 'п'),
    (r'kś', 'ќ'),
    (r'ksi', 'ќ'),
    (r'chś|hś', 'х'),
    (r'chsi|hsi', 'х'),
    (r'fś', 'ф'),
    (r'fsi', 'ф'),
    (r'psi$', 'пi'),
    (r'ksi$', 'ќi'),
    (r'chsi$', 'хi'),
    (r'hsi$', 'хi'),
    (r'fsi$', 'фi'),
    (r'brz|ż', 'ƀ'),
    (r'grz|gż', 'ǧ'),
    (r'mrz|mż', 'ɱ'),
    (r'wrz|wż', 'ŵ'),
    (r'drz', 'ď'),
    (r'dż', 'đ'),
    (r'bź', 'б'),
    (r'bzi', 'б'),
    (r'gź', 'г'),
    (r'gzi', 'г'),
    (r'mź', 'м'),
    (r'mzi', 'м'),
    (r'mś', 'м'),
    (r'msi', 'м'),
    (r'wź', 'ᲈ'),
    (r'wzi', 'ᲈ'),
    (r'bzi$', 'бi'),
    (r'gzi$', 'гi'),
    (r'mzi$', 'мi'),
    (r'msi$', 'мi'),
    (r'wzi$', 'ᲈi'),
]

# Define pre-transformation rules for -w flag
pre_w_rules = [
    (r'kw|kf|kow|kof|ków|kuw|kuf', 'ƙ'),
    (r'pw|pf|pow|pof|pów|puw|puf', 'Þ'),
    (r'chow|hw|chf|hf|chow|how|chof|hof|chów|hów|chuf|huf', 'ƕ'),
    (r'tw|tf|tow|tof|tów|tóf|tuf', 'ƫ'),
    (r'szw|szf|szef|szew|szów|szuf', 'ş'),
    (r'czw|czf|czef|czew|czów|czuf', 'ĉ'),
    (r'gw|gow|gov|gów|guf', 'ģ'),
    (r'bw|bow|bov|bów|buf', 'ḇ'),
    (r'mw|mf|mów|muf|mow|mof', 'ṃ'),
    (r'dw|dow|dów|duw|dóf|duf', 'ḏ'),
    (r'żw|rzw|żew|żef|rzef|rzew|rzów|rzuf|żuf|żów|rzow|rzof|żof|żow', 'ȥ'),
    (r'drzw|drzew|drzów|drzow', 'ḑ'),
    (r'dżw|dżew|dżów|dżow', 'ȡ'),
]

# List of words to keep unchanged
unchanged_words = [
    'marzn', 'marzł', 'perzł', 'mierzn', 'mierzł', 'mierzi', 'perzn'
]

# Words to keep unchanged regardless of the position
whole_words = [
    'cifa', 'cife', 'cifi', 'recife', 'cifu', 'cifo', 'ciga'
]

def apply_transformations(text, rules, unchanged_set, whole_word_set):
    if text in unchanged_set or text in whole_word_set:
        return text
    for pattern, replacement in rules:
        text = re.sub(pattern, replacement, text)
    return text

def process_file(input_path, output_path, pre_rules=[], show_source=False):
    with open(input_path, 'r', encoding='utf-8') as infile:
        words = infile.readlines()
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for word in words:
            original_word = word.strip()
            transformed_word = original_word
            for rules in pre_rules:
                transformed_word = apply_transformations(transformed_word, rules, set(), set())
            transformed_word = apply_transformations(transformed_word, transformation_rules, set(unchanged_words), set(whole_words))
            if show_source:
                outfile.write(f"{original_word} {transformed_word}\n")
            else:
                outfile.write(f"{transformed_word}\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: script.py dictionary_file_path output_file [-b] [-w] [-s]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    pre_rules = []
    show_source = False
    
    if '-b' in sys.argv:
        pre_rules.append(pre_b_rules)
    if '-w' in sys.argv:
        pre_rules.append(pre_w_rules)
    if '-s' in sys.argv:
        show_source = True

    process_file(input_file, output_file, pre_rules, show_source)
