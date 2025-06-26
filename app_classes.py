import sys

import tkinter as tk
from tkinter import ttk
import tksvg
import re
import os
import random
import webbrowser

# Checks if all required modules are imported
REQUIRED_MODULES = {"tkinter", "tkinter.ttk", "tksvg", "re", "os", "random", "webbrowser"}

for module in REQUIRED_MODULES:
    if module not in sys.modules.keys():
        print(f"Failed to import {module}")
        sys.exit()

# App
class App:
    '''App'''
    def __init__(self, title: str, size: str):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(size)
        self.root.resizable(False,False)

        HomeFrame.SIZE = size
        HomeFrame(self.root, size=size)
        self.root.mainloop()



# Front page
class HomeFrame:
    '''Front page that appears when starting the app'''
    # Constants
    MODES = ("Practice", "Quiz")
    LEVELS = ("5", "6", "7", "8", "9", "10")
    SIZE = ""

    # Change when an instance is created
    root = None
    
    def __init__(self, master, size: str):
        HomeFrame.root = master
        # Setting up frame
        self.frame = tk.LabelFrame(master, width=size.split("x")[0], height=size.split("x")[1], text="Kanji Stroke Quizinator", font=("Noto Sans JP", 15))
        self.frame.pack()

        # Title label
        self.title = ttk.Label(self.frame, text="Welcome to the Kanji Stroke Quizinator!", font=("Noto Sans JP", 12))
        self.title.pack()

        # Mode subtitle
        self.mode_subtitle = ttk.Label(self.frame, text="Select a mode below.", font=("Noto Sans JP", 10))
        self.mode_subtitle.pack()

        # Styles
        ttk.Style().configure("TRadiobutton", font=("Noto Sans JP", 10))
        ttk.Style().configure("TButton", font=("Noto Sans JP", 10))

        # Mode buttons
        self.mode_buttons = {}
        self.mode_var = tk.StringVar()
        for mode in HomeFrame.MODES:
            self.mode_buttons[mode] = ModeSelectionRadioButton(master=self, mode=mode)
            self.mode_buttons[mode].button.pack()

        # Level subtitle
        self.level_subtitle = ttk.Label(self.frame, text="Select a Kanken level below.", font=("Noto Sans JP", 10))
        self.level_subtitle.pack()

        # Level buttons
        self.level_buttons = {}
        self.level_var = tk.StringVar()
        for level in HomeFrame.LEVELS:
            self.level_buttons[level] = LevelSelectionRadiobutton(master=self, level=level)
            self.level_buttons[level].button.pack()

        # Start button
        start_button = StartButton(master=self)
        start_button.button.pack()

        # Quit button
        quit_button = ttk.Button(master=self.frame, text="Quit", command=HomeFrame.root.quit)
        quit_button.pack()

        # Attribution
        attribution_label_1 = ttk.Label(master=self.frame, text="For the Kanji SVG images and stroke annotation positions, I used data from ", font=("Noto Sans JP", 10))
        attribution_link_kanjivg = ttk.Label(master=self.frame, text="KanjiVG [https://kanjivg.tagaini.net/]", cursor="hand2", font=("Noto Sans JP", 10))
        attribution_link_kanjivg.bind("<Button-1>", lambda e:self.open_hyperlink(url="https://kanjivg.tagaini.net/"))
        attribution_label_2 = ttk.Label(master=self.frame, text=" by Ulrich Apel, licensed under CC BY-SA 3.0.\n", font=("Noto Sans JP", 10))

        attribution_label_3 = ttk.Label(master=self.frame, text="For the Kanjis found in each Kanken (漢検「日本漢字能力検定」) level, I obtained them from", font=("Noto Sans JP", 10))
        attribution_link_nihongo_pro = ttk.Label(master=self.frame, text="Nihongo-Pro.", cursor="hand2", font=("Noto Sans JP", 10))
        attribution_link_nihongo_pro.bind("<Button-1>", lambda e:self.open_hyperlink(url="https://www.nihongo-pro.com/kanji-pal/list/kanken"))
        
        attribution_label_1.pack()
        attribution_link_kanjivg.pack()
        attribution_label_2.pack()
        attribution_label_3.pack()
        attribution_link_nihongo_pro.pack()

    def open_hyperlink(self, url: str):
        webbrowser.open_new_tab(url)


class ModeSelectionRadioButton():
    '''App mode selection radio button to be displayed in the Front page'''
    def __init__(self, master, mode: str):
        self.master = master.frame
        self.mode = mode
        self.button = ttk.Radiobutton(master=master.frame, text=mode, value=mode, variable=master.mode_var, style="TRadiobutton")


class LevelSelectionRadiobutton():
    '''Level selection to be layed out in the Front page'''
    def __init__(self, master, level: str):
        self.master = master.frame
        self.level = level
        self.button = ttk.Radiobutton(master=master.frame, text=f"Level {level}｜{level}級", value=level, variable=master.level_var, style="TRadiobutton")


class StartButton():
    '''Start button to be layed out in the Front page'''
    def __init__(self, master):
        self.master = master
        self.button = ttk.Button(master=master.frame, text="Start", command=lambda: self.start_callback(), style="TButton")

    def start_callback(self):
        if self.master.mode_var.get() in HomeFrame.MODES and self.master.level_var.get() in HomeFrame.LEVELS:
            self.master.frame.destroy()
            KanjiFrame(master=HomeFrame.root, mode=self.master.mode_var.get(), level=self.master.level_var.get())



# Kanji frame (main interface)
class KanjiFrame:
    '''Main interactivity window for both Practice and Quiz modes'''
    # Constants
    SCALE_VALUE = 5

    # Change when an instance of KanjiFrame is created
    master = None
    check_button = None
    undo_button = None
    reset_button = None
    next_button = None
    result_label = None
    current_mode = None

    # Change throughout run
    buttons = dict()
    kanji_information = dict()
    current_kanji_character = ""
    current_kanji_svg_file = ""
    current_mode = ""
    main_stroke_number = 0
    question_number = 1

    def __init__(self, master, mode: str, level: str):
        # Setting of instance constants
        self.qns_quantity = 5 # Adjust based on MODE
        self.mode = mode
        self.level = level

        # Reset Class variables
        KanjiFrame.master = master
        KanjiFrame.stroke_buttons = dict()
        KanjiFrame.main_stroke_number = 0
        KanjiFrame.question_number = 1

        self.frame = tk.LabelFrame(master, width=500, height=600, text=f"{mode} Qns {KanjiFrame.question_number}/{self.qns_quantity}", font=("Noto Sans JP", 20))
        self.frame.pack()

        # Selecting unique Kanjis (file names)
        all_kanji_files = os.listdir(f"kanken_kanji_svg/kanken{level}_kanji_svg")
        i = 0
        self.kanji_char_chosen = []
        while i != self.qns_quantity:
            chosen = random.choice(all_kanji_files)
            if chosen not in self.kanji_char_chosen:
                kanji_char = convert_file_name_to_character(chosen)
                KanjiFrame.kanji_information[kanji_char] = dict()
                KanjiFrame.kanji_information[kanji_char]["file_name"] = chosen

                self.kanji_char_chosen.append(kanji_char)
                i += 1
        print(KanjiFrame.kanji_information.keys())
        self.kanji_question_setup()

    def kanji_question_setup(self):
        '''Calls all of the creation buttons'''
        self.question_creation()
        self.check_button_creation()
        self.undo_button_creation()
        self.reset_button_creation()
        self.result_label_creation()
        self.next_button_creation()
    
    def create_image_path(self, kanji_file_name: str, level: str):
        '''Creates file path for kanji image'''
        image_root_directory = f"kanken_kanji_svg/kanken{level}_kanji_svg/"
        return image_root_directory + kanji_file_name
    
    def stroke_button_creation(self, stroke_x_y_position_dict: dict):
        '''Creates all of the stroke buttons for a Kanji'''
        KanjiFrame.main_stroke_number = len(stroke_x_y_position_dict)

        for i in range(len(stroke_x_y_position_dict)):
            stroke_number = i+1
            KanjiFrame.stroke_buttons["button_" + str(stroke_number)] = \
            StrokeButton(kanji_frame=self, stroke_number=stroke_number, \
                          stroke_x_y_position_dict=stroke_x_y_position_dict)
            
            button = KanjiFrame.stroke_buttons["button_" + str(stroke_number)] # Temporary scope variable
            button.button.place(x=button.x, y =button.y)
    
    def question_creation(self):
        '''Sets up the svg image and stroke buttons'''
        # Set current information
        KanjiFrame.current_kanji_character = self.kanji_char_chosen[KanjiFrame.question_number-1]
        KanjiFrame.current_kanji_svg_file = KanjiFrame.kanji_information[KanjiFrame.current_kanji_character]["file_name"]

        image_path = self.create_image_path(KanjiFrame.current_kanji_svg_file, level=self.level)
        stroke_x_y_position_dict = obtain_stroke_x_y_position(image_path)
        KanjiFrame.kanji_information[KanjiFrame.current_kanji_character]["image_path"] = image_path
        KanjiFrame.kanji_information[KanjiFrame.current_kanji_character]["stroke_positions"] = stroke_x_y_position_dict
        
        # Add Kanji image to frame
        self.svg_image = tksvg.SvgImage(file=image_path)
        self.svg_image.configure(scale=KanjiFrame.SCALE_VALUE)
        self.image_label = ttk.Label(self.frame, image=self.svg_image)
        self.image_label.image = self.svg_image
        self.image_label.grid(row=0, column=0)

        # Stroke Button creation
        self.stroke_button_creation(stroke_x_y_position_dict=stroke_x_y_position_dict)

    def check_button_creation(self):
        '''Creates and places Check button'''
        KanjiFrame.check_button = CheckButton(kanji_frame=self)
        KanjiFrame.check_button.button.grid(row=1, column=0)
    
    def undo_button_creation(self):
        '''Creates and places Undo button'''
        KanjiFrame.undo_button = UndoButton(kanji_frame=self)
        KanjiFrame.undo_button.button.grid(row=2, column=0)

    def reset_button_creation(self):
        '''Creates and places Reset button'''
        KanjiFrame.reset_button = ResetButton(kanji_frame=self)
        KanjiFrame.reset_button.button.grid(row=3, column=0)

    def result_label_creation(self):
        '''Creates and places Result label'''
        style = ttk.Style()
        style.configure("result.TLabel", foreground="black", background="white", font=("Noto Sans JP", 10))

        KanjiFrame.result_label = ttk.Label(text="<Your result will be shown here>", style="result.TLabel", master=self.frame)
        KanjiFrame.result_label.grid(row=4, column=0)

    def next_button_creation(self):
        '''Creates and places Next button'''
        KanjiFrame.next_button = NextButton(kanji_frame=self)
        KanjiFrame.next_button.button.grid(row=5, column=0)


class StrokeButton(KanjiFrame):
    # Change when an instance is created
    order_clicked = []
    click_index = 1
    def __init__(self, kanji_frame, stroke_number: int, stroke_x_y_position_dict: dict):
        # self.kanji_frame = kanji_frame
        self.stroke_number = stroke_number
        StrokeButton.click_index = 1
        self.x = stroke_x_y_position_dict[self.stroke_number][0] * KanjiFrame.SCALE_VALUE
        self.y = stroke_x_y_position_dict[self.stroke_number][1] * KanjiFrame.SCALE_VALUE

        self.stroke_button_style = ttk.Style()
        self.stroke_button_style.configure("clicked.TButton", background="red", font=("Noto Sans JP", 8))
        self.stroke_button_style.configure("unclicked.TButton", font=("Noto Sans JP", 8))
        
        self.button = ttk.Button(kanji_frame.frame, text="?", width=5, style="unclicked.TButton")
        self.button.config(command= lambda: self.stroke_callback(button=self.button, stroke_n=self.stroke_number))
    
    def stroke_callback(self, button, stroke_n: int):
        '''Function of stroke button activation'''
        if not stroke_n in StrokeButton.order_clicked:
            StrokeButton.order_clicked.append(stroke_n)
            button.config(text=str(StrokeButton.click_index), style="clicked.TButton")
        # elif StrokeButton.order_clicked[StrokeButton.click_index-1] == stroke_n:
        else:
            StrokeButton.order_clicked.remove(stroke_n)
            button.config(text="?", style="unclicked.TButton")
        print(f"Click index = {StrokeButton.click_index}")
        StrokeButton.click_index = len(StrokeButton.order_clicked) + 1
        print(f"StrokeButton.order_clicked = {StrokeButton.order_clicked}")

        # Check to whether disable or enable the Check button
        if len(StrokeButton.order_clicked) == KanjiFrame.main_stroke_number:
            KanjiFrame.check_button.button.config(state=['!disabled'])
        else:
            KanjiFrame.check_button.button.config(state=['disabled'])
        
        # Check whether disable or enable the Undo and Reset button
        if len(StrokeButton.order_clicked) != 0:
            KanjiFrame.undo_button.button.config(state=["!disabled"])
            KanjiFrame.reset_button.button.config(state=["!disabled"])
        else:
            KanjiFrame.undo_button.button.config(state=["disabled"])
            KanjiFrame.reset_button.button.config(state=["disabled"])


class CheckButton(KanjiFrame):
    '''When clicked, checks whether the user's click order is correct.'''
    def __init__(self, kanji_frame):
        # self.kanji_frame = kanji_frame
        self.frame = kanji_frame
        self.button = ttk.Button(kanji_frame.frame, text="Check", width=10, state=['disabled'])
        self.button.config(command= lambda: self.check_callback())

    def check_callback(self):
        '''When called, checks whether the user's click order is correct or not.'''
        stroke_number = KanjiFrame.main_stroke_number
        correct_stroke_list = [i+1 for i in range(stroke_number)]
        
        if len(StrokeButton.order_clicked) != stroke_number:
            print("(This should not occur.) Make sure you have clicked all of the stroke buttons. Try again.")
        elif correct_stroke_list == StrokeButton.order_clicked:
            KanjiFrame.result_label.config(text="Correct")
            print("Correct")

            if self.frame.mode == "Practice":
                KanjiFrame.next_button.button.config(text="Next")
            
            KanjiFrame.kanji_information[KanjiFrame.current_kanji_character]["is_correct"] = True
            KanjiFrame.kanji_information[KanjiFrame.current_kanji_character]["attempt"] = correct_stroke_list
            KanjiFrame.kanji_information[KanjiFrame.current_kanji_character]["answer"] = correct_stroke_list
            StrokeButton.order_clicked = []

            print(f"StrokeButton.order_clicked = {StrokeButton.order_clicked}")

            # Configure buttons
            self.reset_stroke_buttons()

            KanjiFrame.check_button.button.config(state=['disabled'])
            KanjiFrame.undo_button.button.config(state=["disabled"])
            KanjiFrame.reset_button.button.config(state=["disabled"])
            KanjiFrame.next_button.button.config(state=['!disabled'])
        else:
            print("Wrong. Check your answer and try again.")
            KanjiFrame.kanji_information[KanjiFrame.current_kanji_character]["is_correct"] = False
            KanjiFrame.kanji_information[KanjiFrame.current_kanji_character]["attempt"] = StrokeButton.order_clicked
            KanjiFrame.kanji_information[KanjiFrame.current_kanji_character]["answer"] = correct_stroke_list
            
            # Configure buttons
            if self.frame.mode == "Quiz": # Quiz mode
                KanjiFrame.result_label.config(text="Wrong.")
                for i in range(KanjiFrame.main_stroke_number):
                    KanjiFrame.stroke_buttons["button_" + str(i+1)].button.config(state=['disabled'])
                StrokeButton.order_clicked = []
                print(f"StrokeButton.order_clicked = {StrokeButton.order_clicked}")

                KanjiFrame.check_button.button.config(state=['disabled'])
                KanjiFrame.undo_button.button.config(state=['disabled'])
                KanjiFrame.reset_button.button.config(state=['disabled'])
            else: # Practice mode
                KanjiFrame.result_label.config(text="Wrong. Check your answer and try again.")
                KanjiFrame.next_button.button.config(text="Skip")

            KanjiFrame.next_button.button.config(state=['!disabled'])

    def reset_stroke_buttons(self):
        '''Resets stroke buttons by changing their text to ?.'''
        for i in range(KanjiFrame.main_stroke_number):
            KanjiFrame.stroke_buttons["button_" + str(i+1)].button.config(text="?")
            KanjiFrame.stroke_buttons["button_" + str(i+1)].button.config(state=['disabled'])


class NextButton(KanjiFrame):
    '''When clicked, moves onto the next question. Also acts as Skip button for Practice Mode'''
    def __init__(self, kanji_frame):
        self.kanji_frame = kanji_frame
        if kanji_frame.mode == "Quiz":
            text = "Next"
        else:
            text = "Skip"
        self.button = ttk.Button(kanji_frame.frame, text=text, width=20) # state=['disabled'] Re-ADD THIS FOR NON TESTING PURPOSES
        self.button.config(state=['disabled'])
        self.button.config(command= lambda: self.next_callback())
    
    def next_callback(self):
        '''When clicked, checks whether the question can be moved on (later feature)'''
        if self.kanji_frame.mode == "Practice":
            KanjiFrame.next_button.button.config(text="Skip")
            StrokeButton.order_clicked = []
        KanjiFrame.next_button.button.config(state=['disabled'])
        KanjiFrame.undo_button.button.config(state=['!disabled'])
        KanjiFrame.reset_button.button.config(state=['!disabled'])
        KanjiFrame.question_number += 1
        # KanjiFrame.question_number = 10 # UNCOMMENT THIS FOR NON TESTING PURPOSES

        if KanjiFrame.question_number > self.kanji_frame.qns_quantity: # End of question answering; goes to Results
            print("Quiz ended")
            KanjiFrame.result_label.config(text="Quiz ended")
            self.kanji_frame.frame.destroy()
            ResultsFrame(master=KanjiFrame.master, mode=self.kanji_frame.mode)
        else: # Moves onto next question
            print("Onto the next Kanji!")
            self.kanji_frame.image_label.destroy()
            for i in range(len(KanjiFrame.stroke_buttons)):
                KanjiFrame.stroke_buttons["button_" + str(i+1)].button.destroy()
            KanjiFrame.stroke_buttons = dict()

            KanjiFrame.result_label.configure(text="<Your result will be shown here>")
            KanjiFrame.question_creation(self=self.kanji_frame)
            self.kanji_frame.frame.config(text=f"{self.kanji_frame.mode} Qns {KanjiFrame.question_number}/{self.kanji_frame.qns_quantity}")


class UndoButton(KanjiFrame):
    '''Appears in quiz mode. When clicked, undos the latest Stroke button clicked (if any).'''
    def __init__(self, kanji_frame):
        self.kanji_frame = kanji_frame
        self.button = ttk.Button(kanji_frame.frame, text="Undo", width=20, state=["disabled"])
        self.button.config(command= lambda: self.undo_callback())

    def undo_callback(self):
        print(f"StrokeButton.order_clicked = {StrokeButton.order_clicked}")
        if len(StrokeButton.order_clicked) != 0:
            # The next 2 lines mimics .pop() but ensuring does NOT modify value in StrokeButton.order_clicked
            # (due to how references and mutability in Python works)
            button_number_removed = StrokeButton.order_clicked[-1]
            StrokeButton.order_clicked = StrokeButton.order_clicked[:-1]

            StrokeButton.click_index = len(StrokeButton.order_clicked) + 1
            print(f"StrokeButton.order_clicked = {StrokeButton.order_clicked}")

            KanjiFrame.stroke_buttons[f"button_{button_number_removed}"].button.config(text="?", style="unclicked.TButton")
            KanjiFrame.check_button.button.config(state=["disabled"])
            if len(StrokeButton.order_clicked) == 0:
                self.button.config(state=["disabled"])
                KanjiFrame.reset_button.button.config(state=["disabled"])


class ResetButton(KanjiFrame):
    '''Appears in quiz mode. When clicked, undos all Stroke button clicked.'''
    def __init__(self, kanji_frame):
        self.kanji_frame = kanji_frame
        self.button = ttk.Button(kanji_frame.frame, text="Reset", width=20, state=["disabled"])
        self.button.config(command= lambda: self.reset_callback())
    def reset_callback(self):
        if len(StrokeButton.order_clicked) != 0:
            for i in StrokeButton.order_clicked:
                KanjiFrame.stroke_buttons[f"button_{i}"].button.config(text="?", style="unclicked.TButton")
            StrokeButton.click_index = 1
            StrokeButton.order_clicked = [] # .clear() cannot be used
            print(f"StrokeButton.order_clicked = {StrokeButton.order_clicked}")

            self.button.config(state=["disabled"])
            KanjiFrame.undo_button.button.config(state=["disabled"])
            KanjiFrame.check_button.button.config(state=["disabled"])



# Results frame
class ResultsFrame():
    # Constants
    GRADES = ("不可", "認", "可", "良", "優", "秀（満点！）") # For 5 qns (quiz)
    COMMENTS = ("そんな．．．", "残念．．．", "大変だったね", "大変よくできました。", "うわ！憧れ．．．", "すごい！") # For 5 qns (quiz)

    # Change when an instance is created
    root = None
    results_dict = dict()
    def __init__(self, master, mode: str):
        # print(f"KanjiFrame.kanji_information = \n{KanjiFrame.kanji_information}")
        ResultsFrame.root = master
        ResultsFrame.results_dict = KanjiFrame.kanji_information

        self.frame = tk.LabelFrame(master, width=500, height=600, font=("Noto Sans JP", 20))
        if mode == "Quiz":
            self.frame.config(text="Results")
        else:
            self.frame.config(text="Summary")
        self.frame.pack()

        # Tallying the score
        self.score = 0
        for kanji_character, info in ResultsFrame.results_dict.items():
            IndividualResultFrame(master=self, kanji_character=kanji_character, is_correct=info["is_correct"], kanji_file_name=info["file_name"])
            if info["is_correct"]:
                self.score += 1
        
        # (Quiz mode) Grade determination and comments
        if mode == "Quiz":
            self.grade = ResultsFrame.GRADES[self.score]
            
            self.score_label = ttk.Label(master=self.frame, text=f"Final score: {self.score}/{len(ResultsFrame.results_dict)}\t{self.grade}", font=("Yu Mincho Demibold", 20))
            self.score_label.pack()

            self.comment_label = ttk.Label(master=self.frame, text=ResultsFrame.COMMENTS[self.score], font=("Noto Sans JP", 20))
            self.comment_label.pack()

        self.return_button = ReturnButton(master=self.frame)
        self.return_button.button.pack()


class IndividualResultFrame():
    # Changes when an instance is created
    root = None
    def __init__(self, master, kanji_character: str, is_correct: bool, kanji_file_name: str):
        IndividualResultFrame.root = master.frame
        self.kanji_file_name = kanji_file_name
        self.kanji_character = kanji_character

        self.frame = ttk.Frame(master.frame, width=500, height=100)
        self.frame.pack()

        if is_correct:
            result = "⭕️"
        else:
            result = "×"
        
        self.kanji_label = ttk.Label(master=self.frame, text=kanji_character, font=("Noto Sans JP", 20))
        self.kanji_label.grid(row=0, column=0)

        self.result_label = ttk.Label(master=self.frame, text=result, font=("Noto Sans JP", 20))
        self.result_label.grid(row=0, column=1)

        IndividualResultExpandButton(master=self)


class IndividualResultExpandButton():
    '''Button that shows Correct answer and User's attempt when clicked'''
    # Constants
    SCALE = 2
    def __init__(self, master):
        self.master = master
        self.image_path = KanjiFrame.kanji_information[self.master.kanji_character]["image_path"]
        self.stroke_x_y_position_dict = KanjiFrame.kanji_information[self.master.kanji_character]["stroke_positions"]

        self.button = ttk.Button(master=master.frame, text="Expand", command=lambda: self.result_button_callback())
        self.button.grid(row=0, column=2)

        # Correct answer
        self.correct_kanji_stroke_frame = tk.LabelFrame(master=self.master.frame, text="Correct answer")
        # Add Kanji image with CORRECT stroke order to result frame
        self.svg_image = tksvg.SvgImage(file=self.image_path)
        self.svg_image.configure(scale=IndividualResultExpandButton.SCALE)
        self.image_label = ttk.Label(self.correct_kanji_stroke_frame, image=self.svg_image)
        self.image_label.image = self.svg_image
        self.image_label.pack()

        # Correct stroke order labels creation
        for i in range(len(self.stroke_x_y_position_dict)):
            stroke_number = i + 1
            x=self.stroke_x_y_position_dict[i+1][0] * IndividualResultExpandButton.SCALE
            y=self.stroke_x_y_position_dict[i+1][1] * IndividualResultExpandButton.SCALE
            ttk.Label(master=self.correct_kanji_stroke_frame, text=str(stroke_number)).place(x=x, y=y)

        # User's attempt
        self.user_kanji_stroke_frame = tk.LabelFrame(master=self.master.frame, text="Your answer")
        # Add Kanji image with USER'S stroke order to result frame
        self.image_label_user = ttk.Label(self.user_kanji_stroke_frame, image=self.svg_image)
        self.image_label_user.image = self.svg_image
        self.image_label_user.pack()

        # User's stroke order labels creation
        self.incorrect_stroke = ttk.Style()
        self.incorrect_stroke.configure("incorrect.TLabel", foreground="red")

        for i in range(len(self.stroke_x_y_position_dict)):
            stroke_number = ResultsFrame.results_dict[self.master.kanji_character]["attempt"][i]
            x=self.stroke_x_y_position_dict[i+1][0] * IndividualResultExpandButton.SCALE
            y=self.stroke_x_y_position_dict[i+1][1] * IndividualResultExpandButton.SCALE
            
            if stroke_number != i + 1:
                ttk.Label(master=self.user_kanji_stroke_frame, text=f"{stroke_number}(×)", style=("incorrect.TLabel")).place(x=x, y=y)
            else:
                ttk.Label(master=self.user_kanji_stroke_frame, text=str(stroke_number)).place(x=x, y=y)

    def result_button_callback(self):
        '''Buttons that Expand or contracts more Info'''
        if self.button["text"] == "Expand":
            self.button.config(text="Contract")
            self.correct_kanji_stroke_frame.grid(row=1, column=0)
            self.user_kanji_stroke_frame.grid(row=1, column=1)
        else:
            self.button.config(text="Expand")
            self.correct_kanji_stroke_frame.grid_forget()
            self.user_kanji_stroke_frame.grid_forget()


class ReturnButton():
    '''When clicked, returns to Home window'''
    def __init__(self, master):
        self.master = master
        self.button = ttk.Button(master=master, text="Return to main menu", command=lambda: self.return_callback())
    def return_callback(self):
        self.master.destroy()
        HomeFrame(master=ResultsFrame.root, size=HomeFrame.SIZE)

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
    # print(stroke_x_y_position_dict)
    return stroke_x_y_position_dict

def convert_character_to_file_name(character: str) -> str:
    '''Converts a Kanji character into the svg file name'''
    return f"{str(hex(ord(character)))[2:]:0>5}.svg"

def convert_file_name_to_character(file_name: str) -> str:
    '''Converts an svg file name into its the Kanji character associated'''
    return chr(int(file_name[:len(file_name)-4], 16))
