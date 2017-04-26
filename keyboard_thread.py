import threading
import time
import string
from pynput import keyboard
from pynput.keyboard import Key
from inputmethod import ClafricaKeyboard

__author__ = "Harvey Sama"
__date__ = "$22 April 2017 21:42:56$"


class Concur(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.cKeyboard = ClafricaKeyboard()
        self.listener = None

    def run(self):
        self.resume()

    def resume(self):
        with keyboard.Listener(
                on_press=self.on_press
        ) as self.listener:
            self.listener.join()

    def pause(self):
        self.listener.stop()

    def on_press(self, key):
        try:
            # Strip string representation of the key and search in string.punctuation( !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ )
            key_stripped = str(key).strip("'") if "'" not in str(key).strip("'") else str(key).strip('"')
            if key.char not in self.cKeyboard.allowed_characters and key_stripped not in string.punctuation:
                # print( "no " + key.char)
                return

            self.cKeyboard.curr_input.append(key.char)
            print(self.cKeyboard.curr_input)
            # We are sure that it wasn't backspace (else except will be executed)
            self.cKeyboard.ended = False
            # use ckcodes if currdict is empty
            this_dict = self.cKeyboard.codes if not bool(self.cKeyboard.current_dict) else self.cKeyboard.current_dict
            # print this_dict

            new_dict = self.cKeyboard.update_dictionary(this_dict, self.cKeyboard.curr_input)
            # print (new_dict)

            if bool(new_dict) and len(new_dict) == 1 and \
                    bool(self.cKeyboard.current_dict.get("".join(self.cKeyboard.curr_input))):
                # print(new_dict)
                self.cKeyboard.state = "found_code"
            elif bool(new_dict) is False:
                # Let's check whether the previous input key exists in the dictionary
                if bool(self.cKeyboard.current_dict.get("".join(self.cKeyboard.curr_input[:-1]))):
                    # print ("Yay I exist ")  # + char
                    self.cKeyboard.state = "found_code_with_extra_char"
                #     TODO: Reimplement to prevent search_partial_valid_code to be called twice here
                elif bool(self.cKeyboard.search_partial_valid_code(self.cKeyboard.curr_input[1:])[0]):
                    # search recursively starting from [1:] to [-1]
                    (self.cKeyboard.current_dict, self.cKeyboard.curr_input) = \
                        self.cKeyboard.search_partial_valid_code(self.cKeyboard.curr_input[1:])

                    print(self.cKeyboard.curr_input)
                    # all such lines to be removed
                    self.cKeyboard.dictionaries.append(self.cKeyboard.current_dict)
                    print("some character(s) valid")
                    self.cKeyboard.state = "last_valid"
                else:
                    print("not_found")
                    # print(self.cKeyboard.codes.get(key.char))
                    self.cKeyboard.clear_objects()
            # it is not the case that if the length is one then the user typed all the character codes
            # an exception is ae+: if the user types ae, len(new_dict) is one as its the only code with ae

            else:
                print("append: ")
                # print(new_dict)
                self.cKeyboard.current_dict = new_dict
                self.cKeyboard.dictionaries.append(new_dict)
            self.cKeyboard.run_state()
            # for some reason at the end of this method execution, backspace key events are sent
            # I use this variable as a workaround to prevent propagation in **PREVENT PROPAGATION
            self.cKeyboard.ended = True
            print(self.cKeyboard.curr_input)
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
            # **PREVENT PROPAGATION
            time.sleep(0.01)
            if key == Key.backspace:
                if self.cKeyboard.ended:
                    print("ended method")
                    return

                # print "in backspace"
                if len(self.cKeyboard.curr_input) > 0:
                    self.cKeyboard.curr_input.pop()

                if bool(self.cKeyboard.dictionaries) and len(self.cKeyboard.dictionaries) > 0:

                    self.cKeyboard.dictionaries.pop()
                    self.cKeyboard.current_dict = self.cKeyboard.dictionaries[-1] \
                        if len(self.cKeyboard.dictionaries) > 0 else {}
                else:
                    self.cKeyboard.current_dict = {}
                    # print(self.cKeyboard.curr_input)
            elif key in [Key.space, Key.enter]:
                if len(self.cKeyboard.curr_input) == 0 or \
                        not bool(self.cKeyboard.current_dict.get("".join(self.cKeyboard.curr_input))):
                    self.cKeyboard.clear_objects()
                    return
                print(self.cKeyboard.curr_input)
                self.cKeyboard.state = "found_code"
                self.cKeyboard.press_and_release(Key.left)
                time.sleep(0.01)
                self.cKeyboard.run_state()
                self.cKeyboard.press_and_release(Key.right)
