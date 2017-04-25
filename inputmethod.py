from pynput import keyboard
from pynput.keyboard import Key, Controller
import time


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
            keyVal = line.strip().split(" ")
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
        # if not press:
        #     controller.type(char)
        # else:
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

# self = ClafricaKeyboard()
# controller = Controller()
#
# def on_press(key):
#     try:
#         # Strip string representation of the key and search in string.punctuation( !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ )
#         key_stripped = str(key).strip("'") if "'" not in str(key).strip("'") else str(key).strip('"')
#         if key.char not in cKeyboard.allowed_characters and key_stripped not in string.punctuation:
#             # print( "no " + key.char)
#             return
#
#         cKeyboard.curr_input.append(key.char)
#         print(cKeyboard.curr_input)
#         # We are sure that it wasn't backspace (else except will be executed)
#         cKeyboard.ended = False
#         # use ckcodes if currdict is empty
#         this_dict = cKeyboard.codes if bool(cKeyboard.current_dict) is False else cKeyboard.current_dict
#         # print this_dict
#
#         new_dict = cKeyboard.update_dictionary(this_dict, cKeyboard.curr_input)
#         # print (new_dict)
#
#         if bool(new_dict) and len(new_dict) == 1 and bool(cKeyboard.current_dict.get("".join(cKeyboard.curr_input))):
#             # print(new_dict)
#             cKeyboard.state = "found_code"
#         elif bool(new_dict) is False:
#             # Let's check whether the previous input key exists in the dictionary
#             if bool(cKeyboard.current_dict.get("".join(cKeyboard.curr_input[:-1]))):
#                 # print ("Yay I exist ")  # + char
#                 cKeyboard.state = "found_code_with_extra_char"
#             #     TODO: Reimplement to prevent search_partial_valid_code to be called twice here
#             elif bool(cKeyboard.search_partial_valid_code(cKeyboard.curr_input[1:])[0]):
#                 # search recursively starting from [1:] to [-1]
#                 (cKeyboard.current_dict, cKeyboard.curr_input) = cKeyboard.search_partial_valid_code(cKeyboard.curr_input[1:])
#
#                 print(cKeyboard.curr_input)
#                 # all such lines to be removed
#                 cKeyboard.dictionaries.append(cKeyboard.current_dict)
#                 print("some character(s) valid")
#                 cKeyboard.state = "last_valid"
#             else:
#                 print("not_found")
#                 # print(cKeyboard.codes.get(key.char))
#                 cKeyboard.clear_objects()
#         # it is not the case that if the length is one then the user typed all the character codes
#         # an exception is ae+: if the user types ae, len(new_dict) is one as its the only code with ae
#
#         else:
#             print("append: ")
#             # print(new_dict)
#             cKeyboard.current_dict = new_dict
#             cKeyboard.dictionaries.append(new_dict)
#         cKeyboard.run_state()
#         # for some reason at the end of this method execution, backspace key events are sent
#         # I use this variable as a workaround to prevent propagation in **PREVENT PROPAGATION
#         cKeyboard.ended = True
#         print(cKeyboard.curr_input)
#     except AttributeError:
#         print('special key {0} pressed'.format(
#             key))
#         # **PREVENT PROPAGATION
#         time.sleep(0.01)
#         if key == Key.backspace:
#             if cKeyboard.ended:
#                 print("ended method")
#                 return
#
#             # print "in backspace"
#             if len(cKeyboard.curr_input) > 0:
#                 cKeyboard.curr_input.pop()
#
#             if bool(cKeyboard.dictionaries) and len(cKeyboard.dictionaries) > 0:
#
#                 cKeyboard.dictionaries.pop()
#                 cKeyboard.current_dict = cKeyboard.dictionaries[-1] if len(cKeyboard.dictionaries) > 0 else {}
#             else:
#                 cKeyboard.current_dict = {}
#             # print(cKeyboard.curr_input)
#         elif key in [Key.space, Key.enter]:
#             if len(cKeyboard.curr_input) == 0 or not bool(cKeyboard.current_dict.get("".join(cKeyboard.curr_input))):
#                 cKeyboard.clear_objects()
#                 return
#             print(cKeyboard.curr_input)
#             cKeyboard.state = "found_code"
#             cKeyboard.press_and_release(Key.left)
#             time.sleep(0.01)
#             cKeyboard.run_state()
#             cKeyboard.press_and_release(Key.right)
#
# # Collect events until released
# with keyboard.Listener(
#         on_press=on_press
#         ) as listener:
#     listener.join()
