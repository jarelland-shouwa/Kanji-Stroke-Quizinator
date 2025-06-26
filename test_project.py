from app_classes import *

character_file_info = [("以", "04ee5.svg", {1: [12.50, 29.50], 2: [6.75, 81.50], 3: [36.75, 23.50], 4: [74.50, 20.50], 5: [77.50, 62.50]}, "kanken_kanji_svg/kanken7_kanji_svg/04ee5.svg"),
                        ("工", "05de5.svg", {1: [21.25, 32.63], 2: [45.75, 42.50], 3: [7.50, 84.50]}, "kanken_kanji_svg/kanken9_kanji_svg/05de5.svg"),
                        ("主", "04e3b.svg", {1: [35.25, 15.50], 2: [17.50, 40.63], 3: [46.50, 48.50], 4: [21.50, 66.50], 5: [8.50, 94.50]}, "kanken_kanji_svg/kanken8_kanji_svg/04e3b.svg")]

def test_convert_character_to_file_name():
    for pair in character_file_info:
        assert convert_character_to_file_name(pair[0]) == pair[1]


def test_convert_file_name_to_character():
    for pair in character_file_info:
        assert convert_file_name_to_character(pair[1]) == pair[0]


def test_obtain_stroke_x_y_position():
    for kanji_info in character_file_info:
        assert obtain_stroke_x_y_position(kanji_info[3]) == kanji_info[2]


def test_create_image_path():
    assert KanjiFrame.create_image_path(self=None, kanji_file_name="04e0a.svg", level="10") == "kanken_kanji_svg/kanken10_kanji_svg/04e0a.svg"
    assert KanjiFrame.create_image_path(self=None, kanji_file_name="08a08.svg", level="9") == "kanken_kanji_svg/kanken9_kanji_svg/08a08.svg"
    assert KanjiFrame.create_image_path(self=None, kanji_file_name="04e8b.svg", level="8") == "kanken_kanji_svg/kanken8_kanji_svg/04e8b.svg"
    assert KanjiFrame.create_image_path(self=None, kanji_file_name="04ee4.svg", level="7") == "kanken_kanji_svg/kanken7_kanji_svg/04ee4.svg"
    assert KanjiFrame.create_image_path(self=None, kanji_file_name="04f59.svg", level="6") == "kanken_kanji_svg/kanken6_kanji_svg/04f59.svg"
    assert KanjiFrame.create_image_path(self=None, kanji_file_name="05b87.svg", level="5") == "kanken_kanji_svg/kanken5_kanji_svg/05b87.svg"
    
def main():
    test_convert_character_to_file_name()
    test_convert_file_name_to_character()

if __name__ == "__main__":
    main()