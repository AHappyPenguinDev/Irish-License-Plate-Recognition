import easyocr
import re
import string

# Initialize OCR reader
reader = easyocr.Reader(['en'], gpu=True)

# Mapping dictionaries for character conversion
# Similar characters and numbers which OCR might get confused
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'L': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'B': '8',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}

dict_underscore_to_score = {
    '_': '-',
    '*': '-'
}

# Splits license plate by dash


def split_plate(text):
    """

    Splits the given string by a dash using regex.

    Handles multiple dashes, spaces, and trims results.

    """

# Improve accuracy by replacing * and _ with - ,
# as this is a common mistake

    text = re.sub('\\*', '-', text)
    text = re.sub('_', '-', text)

    # Arrumar esse regex, o objetivo é dividir os hifens também
    parts = re.split(
        r'([A-Z0-9]{2,3})(-)([A-Z0-9]{1,2})(-)([A-Z0-9]{1,6})', text.strip())

    return [p for p in parts if p]

    return -1, -1, -1, -1, -1


def license_complies_format(text):

    # Format
    # 2012 > y
    # NN-L-NNNN
    # 2013 < y
    # First num of max of last sequence of digits is required
    # NN(1 or 2)-L-NNNNN
    """
    Check if the license plate text complies with the required format.

    Args:
        text (str): License plate text.

    Returns:
        bool: True if the license plate complies with the format, False otherwise.
    """

    # If 9 < len < 11 then the car was registered after 2012
    # O problema é que só é obrigatório ter um digito dos ultimos 5,
    # Então eu teria que fazer 5 Ifs checando para casos onde tem
    # 5 , 4 , 3, 2 , 1  digitos

    platesections = split_plate(text)

    # Plate must have 3 sections
    if len(platesections) == 5:
        # Max 3 digits, can be 2 if it's before 2013
        matches = 0
        for char in platesections[0]:
            if (char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or char in dict_char_to_int.keys()):
                matches += 1
            else:
                return False

            # Debug
            # if count == 3:
            #     if(char in ['1', '2'] or char in dict_char_to_int.keys()):
            #         print("First 3 match: ", platesections[0])
            # if count == 2:
            #     print("First 2 match: ", platesections[0])

        print("\n")

        for char in platesections[1]:
            if (char == '-' or char in dict_underscore_to_score.keys()):
                matches += 1
            else:
                return False

        # This section marks the region the car is from
        for char in platesections[2]:
            if (char in string.ascii_uppercase or char in dict_int_to_char.keys()):
                matches += 1
            else:
                return False

        for char in platesections[3]:
            if (char == '-' or char in dict_underscore_to_score.keys()):
                matches += 1
            else:
                return False

        # Debug
        # if count >= 1:
        #     print("Region matches: ", platesections[1])

        print("\n")

        # Max 5 digits code
        for char in platesections[4]:
            if (char[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or char[0] in dict_char_to_int.keys()):
                matches += 1
            else:
                return False

        # Debug
        # if count >= 1 and count < 7 :
        #     print("Last " , len(platesections[2]) , "match: ", platesections[2])

        # If there is one match for each index of text
        if matches == len(text):
            print("Full match for: ", platesections)
            return True

    else:
        # print("DOES NOT COMPLY")
        return False


def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.
    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """
    license_plate_ = ''
    # Logic for 2013 first
    # First 3 int
    # Next 1-2 letters
    # Last 1-6 int

    platesections = split_plate(text)
    str_mapping = "{"

    # Dinamically mapping each index of license plate to a conversion dictionary
    # If done statically , it would look something like this, but as sizes vary it must be dinamic:
    # (these mappings are not accurate, this is just an example)
    # mapping = {0: dict_int_to_char,
    #            1: dict_int_to_char,
    #            4: dict_int_to_char,
    #            5: dict_int_to_char,
    #            6: dict_int_to_char,
    #            2: dict_char_to_int,
    #            3: dict_char_to_int...

    # First section (Numbers)
    current_index = 0
    print("INITIALIZE INDEX: ", current_index)
    for i in range(len(platesections[0])):
        mappingline = str(current_index) + ": dict_char_to_int,\n"
        str_mapping = str_mapping + mappingline
        current_index += 1

    print("FIRST DASH INDEX: ", current_index)
    # Second section (dash)
    mappingline = str(current_index) + ": dict_underscore_to_score, \n"
    str_mapping = str_mapping + mappingline

    current_index += 1

    print("MIDDLE INDEX: ", current_index)
    # Middle section (Letters)
    for i in range(len(platesections[2])):
        mappingline = str(current_index) + ": dict_int_to_char,\n"
        str_mapping = str_mapping + mappingline
        current_index += 1

    print("SECOND DASH INDEX: ", current_index)
    # Fourth section (dash)
    mappingline = str(current_index) + ": dict_underscore_to_score, \n"
    str_mapping = str_mapping + mappingline

    current_index += 1

    print("LAST SECTION INDEX: ", current_index)
    # Last section (Numbers)
    for i in range(len(platesections[4])):
        # If it's the last mapping, close with "}"
        if current_index == len(text) - 1:
            mappingline = str(current_index) + ": dict_char_to_int}"
            str_mapping = str_mapping + mappingline
            continue

        # For all other mappings, simply append the mapping with a comma at the end
        mappingline = str(current_index) + ": dict_char_to_int,\n"
        str_mapping = str_mapping + mappingline
        current_index += 1

    print("FINAL INDEX: ", current_index)

    print("\nMapping:", str_mapping)

    # Convert string mapping into a real mapping
    mapping = eval(str_mapping, {}, {
        "dict_int_to_char": dict_int_to_char, "dict_char_to_int": dict_char_to_int, "dict_underscore_to_score": dict_underscore_to_score})

    #
    for j in range(len(text)):
        print("Value of J: ", j)
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_


def read_license_plate(license_plate_crop):
    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        bbox, text, score = detection

        # print('\nRaw License plate: ', text)

        text = text.upper().replace(' ', '')

        if license_complies_format(text):
            return format_license(text), score

    return None, None


#         f.close()
