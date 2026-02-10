import easyocr
import re
import string
from dictionaries import dict_char_to_int
from dictionaries import dict_int_to_char
from dictionaries import dict_letter_to_one_letter_region
from dictionaries import dict_underscore_to_score
from dictionaries import regions
from dictionaries import two_lettered_regions_first_letters
from dictionaries import two_lettered_regions_first_letters_lookalikes
from dictionaries import two_lettered_regions_next_possible_letters
from dictionaries import ordered_letter_similarity

# Initialize OCR reader
reader = easyocr.Reader(['en'], gpu=True)

# Mapping dictionaries for character conversion
# Similar characters and numbers which OCR might get confused

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

    # Plate must have 5 sections
    if len(platesections) == 5:

        # This var should be 5 at the end,
        # meaning all sections match the format
        matches = 0

        for char in platesections[0]:
            # Must be 2-3 digits
            if not len(platesections[0]) >= 2 and len(platesections[0] < 3):
                return False

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


def create_mapping(text):
    """
    Create the mapping to be used by format_license
    Args:
        text (str): License plate text.

    Returns:
        str: Mapping for each index of license plate.
    """
    license_plate_ = ''

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
    # print("INITIALIZE INDEX: ", current_index)
    for i in range(len(platesections[0])):
        mappingline = str(current_index) + ": dict_char_to_int,\n"
        str_mapping = str_mapping + mappingline
        current_index += 1

    # print("FIRST DASH INDEX: ", current_index)
    # Second section (dash)
    mappingline = str(current_index) + ": dict_underscore_to_score, \n"
    str_mapping = str_mapping + mappingline

    current_index += 1

    # print("MIDDLE INDEX: ", current_index)
    # Middle section (Letters)
    for i in range(len(platesections[2])):
        mappingline = str(current_index) + ": dict_int_to_char,\n"
        str_mapping = str_mapping + mappingline
        current_index += 1

    # print("SECOND DASH INDEX: ", current_index)
    # Fourth section (dash)
    mappingline = str(current_index) + ": dict_underscore_to_score, \n"
    str_mapping = str_mapping + mappingline

    current_index += 1

    # print("LAST SECTION INDEX: ", current_index)
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

    # print("FINAL INDEX: ", current_index)

    # print("\nMapping:", str_mapping)

    # Convert string mapping into a real mapping
    mapping = eval(str_mapping, {}, {
        "dict_int_to_char": dict_int_to_char, "dict_char_to_int": dict_char_to_int, "dict_underscore_to_score": dict_underscore_to_score})

    return mapping


def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.
    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """
    license_plate_ = ''

    # Dinamically create mapping so it is possible to substitute wrong chars
    # with their lookalikes
    mapping = create_mapping(text)

    # Split plate into 5 sections
    platesections = split_plate(text)

    # -- Region formatting
    # Convert the content from this section to valid regions

    region = platesections[2]
    region_list = list(region)

    # Preformat region (transform numbers into chars)
    print("Region: ", region)
    print("Region_List: ", region_list)
    for i in range(len(region)):
        if region_list[i] in dict_int_to_char:
            print("Assigning " +
                  dict_int_to_char[region_list[i]] + " to region at index [", i, "]")
            region_list[i] = dict_int_to_char[region_list[i]]
            print("Region inside preformatting: ", region_list[i])

        region = ''.join(region_list)

        print("Input: ", region)

        # If it's already a valid region, skip
        if region in regions:
            print("VALID REGION, SKIPPING")
            pass

        # If region has 1 char, assign character to single-lettered region that looks like that char
        if len(region) == 1:
            print("Region has 1 char and is: ", region)
            first_letter = region[0]
            region = dict_letter_to_one_letter_region.get(first_letter, region)
            print("1 char region: ", region)

        # If region has 2 chars ,find the first char and choose the best lookalike
        # to the second char from the possible choices of regions
        if len(region) == 2:

            # I still need to check if region[0] is present in two_lettered_regions_first_letters
            # If not, replace with lookalike
            if not region[0] in two_lettered_regions_first_letters:
                print("Region is: " + region)
                print(region[0] + " looks like " +
                      two_lettered_regions_first_letters_lookalikes[region[0]] + ", assigning")
                new_region = two_lettered_regions_first_letters_lookalikes[region[0]]
                new_region += region[1]
                region = new_region
                print("Region is: " + region)

            # All possible next letters given a starting letter
            possible_letters = two_lettered_regions_next_possible_letters[region[0]]
            second_letter = region[1]

            # Dict of letters that look like second_letter
            lookalikes = ordered_letter_similarity[second_letter]

            smallest_index = float('inf')
            most_similar_letter = None
            for letter in possible_letters:
                if letter in lookalikes:
                    index = lookalikes.index(letter)
                    if index < smallest_index:
                        smallest_index = index
                        most_similar_letter = letter

            if most_similar_letter:
                # Update the second char
                region = region[0] + most_similar_letter
                print("Most similar letter is: ", most_similar_letter)

    platesections[2] = region

    print("Text before: ", text)
    text = ''.join(platesections)
    print("Text after: ", text)

    # Substitute wrong chars with their lookalikes
    for j in range(len(text)):
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_


def read_license_plate(license_plate_crop):
    detections = reader.readtext(license_plate_crop)

    # Store all valid detections in list to use the best one
    valid_detections = []

    # Find the detection with the highest score

    for detection in detections:
        bbox, text, score = detection
        text = text.upper().replace(' ', '')

        print("DETECTED PLATE: ", text)
        if license_complies_format(text):
            valid_detections.append((bbox, format_license(text), score))

    if valid_detections:
        best_detection = max(valid_detections, key=lambda x: x[2])
        bbox, text, score = best_detection
        print("Best detection: ", text, "has a score of: ", score)
        print("Valid detections: ", valid_detections)
        return text, score

    print("No valid detections, try again")
    return None, None
