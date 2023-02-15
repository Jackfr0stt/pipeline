import re

def convert_to_camel_case(file):
    # Read the contents of the file
    with open(file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = words_to_camel_case(line)
        print(line, end='')

def words_to_camel_case(text):
    # Find all words in the text that are separated by undescores
    pattern = r'\b[a-zA-Z]+_[a-zA-Z]+\b'
    words = re.findall(pattern, text)

    # Convert each word to camelCase
    for word in words:
        camel_case = word.split("_")[0].lower()
        for part in word.split("_")[1:]:
            camel_case += part.capitalize()
        
        # Replace the original word with the camelCase version
        text = text.replace(word, camel_case)

    # Find all words in the text that are separated by undescores
    pattern2 = r'\b[a-zA-Z]+_[a-zA-Z]+_[a-zA-Z]+\b'
    words = re.findall(pattern2, text)

    # 2nd loop to make sure no "_" are present
    for word in words:
        camel_case = word.split("_")[0].lower()
        for part in word.split("_")[1:]:
            camel_case += part.capitalize()
        
        # Replace the original word with the camelCase version
        text = text.replace(word, camel_case)

    return text


# Usage
convert_to_camel_case('APIbusterModelled.json')
# convert_to_camel_case('peopleOntologyModelled.json')