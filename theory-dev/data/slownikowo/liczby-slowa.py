#!/usr/bin/env python3
import sys

def read_words_from_file(filename):
    with open(filename, 'r') as file:
        words = [word.strip() for word in file.readlines()]
    return words

def change_to_lowercase(words):
    return [word.lower() for word in words]

def change_strings(words):
    replacements = {
        'prz':'ƥ',
        'psz': 'ƥ',
        'brz': 'ƀ',
        'bż': 'ƀ',
        'krz': 'ķ',
        'ksz': 'ķ',
        'grz': 'ĝ',
        'trz': 'ƫ',
        'tsz': 'ƫ',
        'wrz': 'Ʋ',
        'wsz': 'ƒ',
        'gż': 'ĝ',
        'chsz': 'ĥ',
        'chrz': 'ĥ',
        'mrz': 'ƕ',
        'ch': 'h', 
        'szcz': 'ş', 
        'ść': 'ŝ', 
        'ści': 'ŝ',
        'si': 'ś', 
        'ci': 'ć', 
        'ni': 'ń',
        'sz': 'š', 
        'rz': 'ż', 
        'cz': 'č', 
        'ó': 'u', 
        'zi': 'ź', 
        'dż': 'ď',
        'dź': 'ģ', 
        'dzi': 'ģ', 
        'dz': 'đ', 
        'v': 'w'
    }
    for i, word in enumerate(words):
        for key, value in replacements.items():
            words[i] = words[i].replace(key, value)
    return words

def assign_numeric_values(words):
    letter_values = {
        'k,h': -12, 
        'p,ś,f,ƥ,ķ,ĥ,ƒ': -10, 
        'y,ą': 11, 
        'g,b,m,š,ć,č,ź,t,ŝ,ş,w,ƫ,Ʋ': -7,
        'd,ƕ,ƀ,ĝ':-5,
        'a,o,u': 7, 
        'r': -3,
        'ģ,j,ż,ď': -2, 
        'i': 3, 
        'ę,n,ń': 1, 
        's,z,c,đ,e,l,ł': 0
    }
    word_values = []
    for word in words:
        value = 0
        for letter in word:
            for key, val in letter_values.items():
                if letter in key:
                    value += val
                    break
        word_values.append(value)
    return word_values

def write_words_with_values_to_file(words, values, filename):
    with open(filename, 'w') as file:
        for word, value in zip(words, values):
            file.write(f"{word} = {value}\n")

def process_file(filename):
    words = read_words_from_file(filename)
    words = change_to_lowercase(words)
    words = change_strings(words)
    values = assign_numeric_values(words)
    
    with open(f"{filename}-fonetic", 'w') as file:
        for word in words:
            file.write(f"{word}\n")
    
    write_words_with_values_to_file(words, values, f"{filename}-fonetic-number")

    with open(f"{filename}-fonetic-number", 'r') as file:
        too_much = 20
        too_little = -20
        too_much_file = open(f"{filename}-toomuch", 'w')
        too_little_file = open(f"{filename}-toolittle", 'w')
        for line in file:
            word, value = line.strip().split(' = ')
            value = int(value)
            if value > too_much:
                too_much_file.write(f"{word} = {value}\n")
            elif value < too_little:
                too_little_file.write(f"{word} = {value}\n")
        too_much_file.close()
        too_little_file.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        filename = sys.argv[1]
        process_file(filename)