
import keyboard
from __builtin__ import type

__author__ = "Harvey Sama"
__date__ = "$17 mars 2017 07:55:15$"


class ClafricaKeyboard:
    def __init__(self):
        self.codes = {}
        self.currentDict = {}
        self.dictionaries = []
        self.currInput = []  # list of characters
        self.extrachar = None
        self.state = "none"


cKeyboard = ClafricaKeyboard()
typed = "false"
codes = open("codes.txt", "r")
for line in codes:
    keyVal = line.strip().split(" ")
    # cKeyboard.codes[keyval[0]] = keyval[1]
    cKeyboard.codes.update(dict(zip(*[iter(keyVal)] * 2)))
# print cKeyboard.codes

def getChars(character, dictionary):
    try:
        return dictionary.get(character)
    except (KeyError, TypeError, AttributeError):
        return None


def getExceptions(): return [".", "*", "-", "_", "?", "backspace", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                             "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                             "n", "o", "p", "q", "r", "s", "t", "t", "v", "w", "x", "y", "z"]


def writeString(string, length):
    for i in range(1, length+1):
        keyboard.send("backspace")
    keyboard.write(unicode(string, "utf-8"))

def updateDictionary(curr_dict, input):
    """ 
    :type input: str
    :type curr_dict: dict

    :return: dict
    """
    new_dict = {}

    def char_encode(char): return char.decode("utf-8").encode("utf-8")

    for key in curr_dict:
        if key.startswith("".join(map(char_encode, input))):
            new_dict[key] = curr_dict.get(key)
    return new_dict


def callback(event):
    """
    Callback function that is called each time a key is pressed
    :param event: 
    :return: None
    """
    if keyboard.is_pressed(event.name):
        if event.name not in getExceptions() and len(event.name) > 1:
            # print event.name.decode("utf-8").encode("windows-1252").decode("utf-8")
            return
        if event.name == "backspace":
            # print "in backspace"
            if len(cKeyboard.currInput) > 0:
                cKeyboard.currInput.pop()

            if bool(cKeyboard.dictionaries) and len(cKeyboard.dictionaries) > 0:

                cKeyboard.dictionaries.pop()
                cKeyboard.currentDict = cKeyboard.dictionaries[-1] if len(cKeyboard.dictionaries) > 0 else {}
            else:
                cKeyboard.currentDict = {}
            print cKeyboard.currInput
            return
        if event.name.isalpha() and keyboard.is_pressed('shift+' + event.name):
            cKeyboard.currInput.append(event.name.upper())
        else:
            cKeyboard.currInput.append(event.name)
        print cKeyboard.currInput
        # use ckcodes if currdict is empty
        this_dict = cKeyboard.codes if bool(cKeyboard.currentDict) is False else cKeyboard.currentDict
        # print this_dict
        # try:
        new_dict = updateDictionary(this_dict, cKeyboard.currInput)
        # except UnicodeDecodeError:

        print new_dict

        if bool(new_dict) and len(new_dict) == 1 and bool(cKeyboard.currentDict.get("".join(cKeyboard.currInput))):
            print "one item "
            print new_dict
            cKeyboard.state = "found_code"

        elif not bool(new_dict):
            # Let's check whether the previous input key exists in the dictionary
            if bool(cKeyboard.currentDict.get("".join(cKeyboard.currInput[:-1]))):
                print "Yay I exist "  # + char
                cKeyboard.state = "found_code_with_extra_char"
            elif bool(updateDictionary(cKeyboard.codes, cKeyboard.currInput[-1])):
                print "last character valid"
                cKeyboard.state = "last_valid"
            else:
                print "not found"
                cKeyboard.currInput = []
                cKeyboard.dictionaries = []
                cKeyboard.currentDict = {}
        # it is not the case that if the length is on then the user typed all the character codes
        # an exception is ae+: if the user types ae, len(new_dict) is one as its the only code with ae

        else:
            print "append: "
            print new_dict
            cKeyboard.currentDict = new_dict
            cKeyboard.dictionaries.append(new_dict)

        if cKeyboard.state == "found_code" or cKeyboard.state == "found_code_with_extra_char" \
                or cKeyboard.state == "last_valid":


            if cKeyboard.state == "found_code":
                string = cKeyboard.currentDict.get("".join(cKeyboard.currInput))
                print "found: " + string
                writeString(string, len(cKeyboard.currInput))
                # keyboard.send("backspace")
                cKeyboard.currInput = []
                cKeyboard.dictionaries = []
                cKeyboard.currentDict = {}
            elif cKeyboard.state == "found_code_with_extra_char":
                string = cKeyboard.currentDict.get("".join(cKeyboard.currInput[:-1]))
                print "found_code_with_extra_char" + cKeyboard.currInput[-1]
                # keyboard.send("backspace")
                writeString(string, len(cKeyboard.currInput))
                keyboard.send(cKeyboard.currInput[-1])
            else:
                last_char = cKeyboard.currInput[-1]
                cKeyboard.currInput = []
                cKeyboard.dictionaries = []
                cKeyboard.currentDict = {}
                writeString(last_char, 1)
            cKeyboard.state = "nothing"

keyboard.hook(callback)
keyboard.wait()