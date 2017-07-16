from pynput.keyboard import Key, Controller
from keyboardthread import KeyboardThread
from mousethread import MouseThread
import time
import threading
import re
import codes

__author__ = "Harvey Sama"
__date__ = "$17 mars 2017 07:55:15$"


class ClafricaKeyboard(threading.Thread):
    def __init__(self, init_class=KeyboardThread):
        threading.Thread.__init__(self)
        self.init_class = init_class
        self.keyboard_thread_instance = None
        self.mouse_thread_instance = None
        self.typing = True
        self.codes = codes.character_codes
        self.current_dict = {}
        self.dictionaries = []
        self.curr_input = []  # list of characters
        self.state = "nothing"
        self.allowed_characters = [".", "*", "-", "_", "?", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                                   "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                                   "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                                   "A", "B", 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.controller = Controller()

    def run(self):
        self.keyboard_thread_instance = self.init_class()
        self.keyboard_thread_instance.set_clafrica_controller(self)
        self.keyboard_thread_instance.start()

        self.mouse_thread_instance = MouseThread()
        self.mouse_thread_instance.set_clafrica_controller(self)
        self.mouse_thread_instance.start()
        self.call()

    def _stop(self):
        self.keyboard_thread_instance.pause()
        self.mouse_thread_instance.pause()

    def call(self):
        while self.keyboard_thread_instance.is_alive():
            if self.state is not "nothing":
                string, extra, length = self.run_state()
                self.clear_objects()
                self.typing = False
                self.write_characters(string, extra, length)

            # print(self.state)

        print("Clafrica keyboard stopped. Now exiting")

    def search_partial_valid_code(self, input_list):
        found_codes = self.update_dictionary(self.codes, input_list)
        print("in recursive search")
        print(input_list)
        if bool(found_codes):
            return found_codes, input_list
        elif len(input_list) == 1:
            return None, None
        else:
            return self.search_partial_valid_code(input_list[1:])

    def run_state(self):
        """

        :rtype: tuple
        """
        # print(self.state)
        extra = ''
        string = ''
        if self.state == "found_code":
            string = self.current_dict.get("".join(self.curr_input))
        elif self.state == "found_code_with_extra_char":
            string = self.current_dict.get("".join(self.curr_input[:-1]))
            print("found_code_with_extra_char " + self.curr_input[-1])
            extra = self.curr_input[-1]
        return string, extra, len(self.curr_input)

    def write_characters(self, string, extra, length) -> None:
        for i in range(1, length + 1):
            self.controller.press(Key.backspace)
        self.controller.type(string)
        print("done typing")
        # self.clear_objects()

        if extra is not "":
            if extra is "space":
                self.controller.press(Key.space)
            elif extra is "enter":
                self.controller.press(Key.enter)
            else:
                self.controller.type(extra)
        self.state = "nothing"
        self.typing = True

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
