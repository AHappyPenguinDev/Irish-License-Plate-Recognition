# Chars to their int lookalikes
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'L': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'B': '8',
                    'S': '5'}

# Ints to their char lookalikes
dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}

dict_underscore_to_score = {
    '_': '-',
    '*': '-'}

# -- Region sections

# All regions for the region section of the plate
regions = ['CN', 'C', 'DL', 'KE', 'KK', 'KY', 'LD', 'LH', 'LK', 'LM', 'LS', 'MH', 'MN', 'MO', 'OY', 'RN', 'SO', 'TN', 'TS', 'WD', 'WH', 'WW', 'WX', 'ZV', 'ZZ', 'BI', 'CI', 'DI', 'EI', 'FI', 'GI', 'HI', 'IC', 'ID', 'IE', 'IF', 'IH', 'IK', 'IM', 'IN', 'IO', 'IP', 'IR', 'IS', 'IT', 'IU', 'IV', 'IX', 'IY', 'IZ', 'KI', 'LI', 'MI', 'NI', 'PI', 'RI', 'SI', 'TI', 'WI', 'YI', 'ZA', 'ZB', 'ZC', 'ZD', 'ZE', 'ZF', 'ZC', 'ZG', 'ZH', 'ZJ', 'ZK', 'ZL', 'ZM', 'ZN', 'ZO', 'ZP', 'ZR', 'ZS', 'ZT', 'ZU', 'ZV', 'ZW', 'ZX', 'ZY', 'ZZ', 'C', 'CE',
           'CN', 'CW', 'D', 'DL', 'G', 'KE', 'KK', 'KY', 'L', 'LD', 'LH', 'LK', 'LM', 'LS', 'MH', 'MN', 'MO', 'OY', 'RN', 'SO', 'TN', 'TS', 'W', 'WD', 'WH', 'WW', 'WX', 'Z', 'ZV', 'ZZ', 'CI', 'DI', 'EI', 'FI', 'GI', 'HI', 'IC', 'ID', 'IE', 'IF', 'IH', 'IK', 'IM', 'IN', 'IO', 'IP', 'IR', 'IS', 'IT', 'IU', 'IV', 'IX', 'IY', 'IZ', 'KI', 'LI', 'MI', 'NI', 'PI', 'RI', 'SI', 'TI', 'WI', 'YI', 'Z', 'ZA', 'ZB', 'ZC', 'ZD', 'ZE', 'ZF', 'ZC', 'ZG', 'ZH', 'ZJ', 'ZK', 'ZL', 'ZM', 'ZN', 'ZO', 'ZP', 'ZR', 'ZS', 'ZT', 'ZU', 'ZV', 'ZW', 'ZX', 'ZY', 'ZZ']

# Two lettered regions can only start with these letters
two_lettered_regions_first_letters = ['B', 'C', 'D', 'E', 'F', 'G',
                                      'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'W', 'Y', 'Z']

# Possible second letters for regions with two letters
# For example, if a region starts with C it can only end with N,W or I
two_lettered_regions_next_possible_letters = {'C': ['N', 'W', 'I'],
                                              'D': ['L', 'I'],
                                              'F': ['I'],
                                              'G': ['I'],
                                              'I': ['C', 'D', 'E', 'F', 'H', 'K', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z'],
                                              'K': ['E', 'K', 'Y', 'I'],
                                              'L': ['D', 'H', 'K', 'M', 'S', 'I'],
                                              'N': ['I'],
                                              'P': ['I'],
                                              'W': ['D', 'H', 'W', 'X', 'I'],
                                              'Z': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
                                              }

# If the region has only one letter then the letter
# must be one of the following:
# C,D,G,L,W
# Map each char to their lookalikes
dict_letter_to_one_letter_region = {
    'A': 'L',
    'B': 'G',
    'E': 'L',
    'F': 'L',
    'H': 'W',
    'I': 'L',
    'J': 'Z',
    'K': 'W',
    'M': 'W',
    'N': 'W',
    'O': 'D',
    'P': 'D',
    'Q': 'G',
    'R': 'D',
    'S': 'C',
    'T': 'L',
    'U': 'C',
    'V': 'W',
    'X': 'W',
    'Y': 'W',
    'Z': 'G'}

# Dictionary mapping each uppercase letter (A-Z) to a list of the other 25 letters,
# ordered by approximate visual similarity in OCR contexts (based on common shape confusions,
# shared strokes, and typical misrecognition patterns). This is subjective and based on heuristics
# like serif styles, curves vs. straight lines, and historical OCR error data.
# Similarity decreases as you go down the list. Lowercase could be added similarly if needed.

ordered_letter_similarity = {
    'A': ['H', 'K', 'X', 'V', 'W', 'M', 'N', 'U', 'Y', 'Z', 'T', 'F', 'E', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S', 'I', 'J', 'L'],
    'B': ['D', 'P', 'R', 'E', 'F', 'H', 'K', 'M', 'N', 'A', 'X', 'V', 'W', 'U', 'Y', 'Z', 'T', 'O', 'C', 'G', 'S', 'I', 'J', 'L'],
    'C': ['G', 'O', 'E', 'D', 'U', 'S', 'I', 'J', 'L', 'A', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'Y', 'Z', 'T', 'F', 'P', 'R', 'B'],
    'D': ['B', 'O', 'C', 'G', 'P', 'R', 'A', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'U', 'Y', 'Z', 'T', 'F', 'E', 'S', 'I', 'J', 'L'],
    'E': ['F', 'B', 'P', 'R', 'D', 'C', 'G', 'O', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'U', 'Y', 'Z', 'T', 'A', 'S', 'I', 'J', 'L'],
    'F': ['E', 'P', 'R', 'B', 'D', 'T', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'U', 'Y', 'Z', 'A', 'O', 'C', 'G', 'S', 'I', 'J', 'L'],
    'G': ['C', 'O', 'D', 'E', 'S', 'U', 'I', 'J', 'L', 'A', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'Y', 'Z', 'T', 'F', 'P', 'R', 'B'],
    'H': ['A', 'K', 'X', 'N', 'M', 'V', 'W', 'U', 'Y', 'Z', 'T', 'F', 'E', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S', 'I', 'J', 'L'],
    'I': ['J', 'L', 'T', 'F', 'E', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'U', 'Y', 'Z', 'A', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S'],
    'J': ['I', 'L', 'T', 'F', 'E', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'U', 'Y', 'Z', 'A', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S'],
    'K': ['H', 'X', 'A', 'V', 'W', 'M', 'N', 'U', 'Y', 'Z', 'T', 'F', 'E', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S', 'I', 'J', 'L'],
    'L': ['I', 'J', 'T', 'F', 'E', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'U', 'Y', 'Z', 'A', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S'],
    'M': ['N', 'W', 'V', 'U', 'Y', 'H', 'K', 'X', 'A', 'Z', 'T', 'F', 'E', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S', 'I', 'J', 'L'],
    'N': ['M', 'H', 'K', 'X', 'V', 'W', 'U', 'Y', 'A', 'Z', 'T', 'F', 'E', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S', 'I', 'J', 'L'],
    'O': ['C', 'G', 'D', 'B', 'P', 'R', 'E', 'U', 'S', 'I', 'J', 'L', 'A', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'Y', 'Z', 'T', 'F'],
    'P': ['R', 'B', 'D', 'F', 'E', 'O', 'C', 'G', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'U', 'Y', 'Z', 'T', 'A', 'S', 'I', 'J', 'L'],
    'O': ['D', 'C', 'G','B', 'P', 'R', 'E', 'U', 'S', 'I', 'J', 'L', 'A', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'Y', 'Z', 'T', 'F'],
    'R': ['P', 'B', 'D', 'F', 'E', 'O', 'C', 'G', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'U', 'Y', 'Z', 'T', 'A', 'S', 'I', 'J', 'L'],
    'S': ['Z', 'C', 'G', 'O', 'E', 'U', 'I', 'J', 'L', 'A', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'Y', 'T', 'F', 'P', 'R', 'B', 'D'],
    'T': ['I', 'J', 'L', 'F', 'E', 'H', 'K', 'X', 'V', 'W', 'M', 'N', 'U', 'Y', 'Z', 'A', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S'],
    'U': ['V', 'W', 'M', 'N', 'Y', 'H', 'K', 'X', 'A', 'Z', 'C', 'G', 'O', 'S', 'I', 'J', 'L', 'T', 'F', 'E', 'P', 'R', 'B', 'D'],
    'V': ['U', 'W', 'M', 'N', 'Y', 'H', 'K', 'X', 'A', 'Z', 'T', 'F', 'E', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S', 'I', 'J', 'L'],
    'W': ['V', 'U', 'M', 'N', 'Y', 'H', 'K', 'X', 'A', 'Z', 'T', 'F', 'E', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S', 'I', 'J', 'L'],
    'X': ['K', 'H', 'A', 'V', 'W', 'M', 'N', 'U', 'Y', 'Z', 'T', 'F', 'E', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S', 'I', 'J', 'L'],
    'Y': ['V', 'W', 'U', 'M', 'N', 'H', 'K', 'X', 'A', 'Z', 'T', 'F', 'E', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'S', 'I', 'J', 'L'],
    'Z': ['S', 'X', 'K', 'H', 'A', 'V', 'W', 'M', 'N', 'U', 'Y', 'T', 'F', 'E', 'P', 'R', 'B', 'D', 'O', 'C', 'G', 'I', 'J', 'L']
}
