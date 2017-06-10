from pynput.keyboard import Key, Controller
import time
import re

__author__ = "Harvey Sama"
__date__ = "$17 mars 2017 07:55:15$"

class ClafricaKeyboard:
    def __init__(self):
        self.codes = self.load_codes()
        self.current_dict = {}
        self.dictionaries = []
        self.curr_input = []  # list of characters
        self.state = "none"
        self.ended = False
        self.allowed_characters = [".", "*", "-", "_", "?", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                                   "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                                   "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                                   "A", "B", 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.controller = Controller()

    def load_codes(self):
        codes = open("codes.txt", "r", encoding="utf8")
        characters = {}
        for line in codes:
            # try:
            keyVal = re.split('\s+', line.strip())
                # cKeyboard.codes[keyval[0]] = keyval[1]
            characters.update(dict(zip(*[iter(keyVal)] * 2)))
        return characters

    def search_partial_valid_code(self, input_list):
        found_codes = self.update_dictionary(self.codes, input_list)
        print(input_list)
        if bool(found_codes):
            return found_codes, input_list
        elif len(input_list) == 1:
            return None, None
        else:
            return self.search_partial_valid_code(input_list[1:])

    def write_string(self, string, length):
        # print(string)
        for i in range(1, length + 1):
            # print("pressing backspace")
            time.sleep(0.01)
            self.controller.press(Key.backspace)

            # print("pressed")
        self.controller.type(string)

    def press_and_release(self, key):
        self.controller.press(key)
        self.controller.release(key)

    def run_state(self):
        print(self.state)
        if self.state == "found_code":
            self.state = "nothing"
            string = self.current_dict.get("".join(self.curr_input))
            # print("found: " + string)
            self.write_string(string, len(self.curr_input))
            # keyboard.press("backspace")
            self.clear_objects()
        elif self.state == "found_code_with_extra_char":
            self.state = "nothing"
            string = self.current_dict.get("".join(self.curr_input[:-1]))
            print("found_code_with_extra_char " + self.curr_input[-1])
            # controller.press(Key.backspace)
            extra = self.curr_input[-1]
            self.press_and_release(Key.left)
            time.sleep(0.01)
            self.write_string(string, len(self.curr_input) - 1)
            self.handle_extra_string(extra)
            self.press_and_release(Key.right)

        elif self.state == "last_valid":
            # print("right down here")
            self.state = "nothing"
            last_char = self.curr_input
            self.handle_extra_string(last_char)
            # self.clear_objects()

    def char_encode(self, char): return char

    def handle_extra_string(self, extra):
        self.clear_objects()
        char_dict = self.update_dictionary(self.codes, extra)
        if bool(char_dict):
            self.curr_input = extra if type(extra) is list else [extra]
            self.current_dict = char_dict
            self.dictionaries = [self.current_dict]

    def clear_objects(self):
        self.curr_input = []
        self.dictionaries = []
        self.current_dict = {}

    def update_dictionary(self, curr_dict, string):
        """ 
        :type string: str
        :type curr_dict: dict

        :return: dict
        """
        new_dict = {}
        for key in curr_dict:
            if key.startswith("".join(string)):
                new_dict[key] = curr_dict.get(key)
        return new_dict