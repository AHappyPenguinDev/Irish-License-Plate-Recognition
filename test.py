from dictionaries import *

plate = "171-IB-2042"

def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.
    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """
    # -- Region formatting
    # Convert the content from this section to valid regions

    platesections = ["171","-","IA","-","2042"]
    region = platesections[2]
    region_list = list(region)

    # Preformat region (transform numbers into chars)
    for i in range(len(region)):
        if region_list[i] in dict_int_to_char:
            print("Assigning " +
                  dict_int_to_char[region_list[i]] + " to region")
            region_list = dict_int_to_char[region_list[i]]
            print("Region inside preformatting: ", region_list[i])

        region = ''.join(region_list)

        # If it's already a valid region, skip
        if region in regions:
            pass

        # If region has 1 char, assign character to single-lettered region that looks like that char
        if len(region) == 1:
            print("Region has 1 char and is: ", region)
            first_letter = region[0]
            region = dict_letter_to_one_letter_region.get(first_letter, region)
            print("1 char region: ", region)

        # If region has 2 chars ,find the first char and choose the best lookalike to the second char from
        # the possible choices of regions
        if len(region) == 2:
            # All possible next letters given a starting letter
            possible_letters = two_lettered_regions_next_possible_letters[region[0]]
            second_letter = region[1]

            # Dict of letters that look like each other
            lookalikes = ordered_letter_similarity[second_letter]

            min_index = float('inf')
            most_similar_letter = None
            for letter in possible_letters:
                if letter in lookalikes:
                    index = lookalikes.index(letter)
                    if index < min_index:
                        min_index = index
                        most_similar_letter = letter

            if most_similar_letter:
                # Update the second char
                region = region[0] + most_similar_letter
                print("Most similar letter is: ", most_similar_letter)

    platesections[2] = region

    print("Text before: ", text)
    text = ''.join(platesections)
    print("Text after: ", text)


format_license(plate)
