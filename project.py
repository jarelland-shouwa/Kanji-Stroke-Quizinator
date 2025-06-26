import re

# Import classes
from app_classes import *

def main():
    App(title="Kanji Stroke Quizinator", size="600x800")

# For testing purposes
def obtain_stroke_x_y_position(image_path: str) -> dict:
    '''Obtains positions of stroke labels from svg source'''
    with open(image_path, "r") as svg_source:
        source_text = svg_source.read()

    stroke_number = 1
    stroke_x_y_position_dict = dict()
    while "transform" in source_text:
        matches = re.search(r"(\(1 0 0 1 (\d+\.?\d*\d*) (\d+\.?\d*\d*)\))+", source_text)
        stroke_x_y_position_dict[stroke_number] = [float(matches[2]), float(matches[3])] # x-, y- coordinates
        i = source_text.index(matches[0])
        source_text = source_text[i+len(matches[1]):] # cuts off text that a match has been found previously
        stroke_number += 1
    print(stroke_x_y_position_dict)
    return stroke_x_y_position_dict

def convert_character_to_file_name(character: str) -> str:
    '''Converts a Kanji character into the svg file name'''
    return f"{str(hex(ord(character)))[2:]:0>5}.svg"

def convert_file_name_to_character(file_name: str) -> str:
    '''Converts an svg file name into its the Kanji character associated'''
    return chr(int(file_name[:len(file_name)-4], 16))

if __name__ == "__main__":
    main()