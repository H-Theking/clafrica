# -*- coding: UTF-8 -*-
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
    keyVal = line.split(" ")
    # cKeyboard.codes[keyval[0]] = keyval[1]
    cKeyboard.codes.update(dict(zip(*[iter(keyVal)] * 2)))


def getChars(character, dictionary):
    try:
        return dictionary.get(character)
    except (KeyError, TypeError, AttributeError):
        return None


def getExceptions(): return [".", "*", "-", "_", "?", "backspace","1", "2", "3", "4", "5", "6", "7", "8", "9"]


def writeString(string):
    for i in range(1, len(string)):
        keyboard.send("backspace")
    keyboard.write(unicode(string, "utf-8"))


def updateDictionary(curr_dict, input):
    """ 
    :type input: str
    :type curr_dict: dict
    
    :return: dict
    """
    new_dict = {}
    for key in curr_dict:
        if key.startswith("".join(input)):
            new_dict[key] = curr_dict.get(key)
    return new_dict

def callback(event):
    if keyboard.is_pressed(event.name):
        if event.name not in getExceptions() and len(event.name) > 1:
            return
        if event.name == "backspace":
            # print "in backspace"
            if bool(cKeyboard.dictionaries) and len(cKeyboard.dictionaries) > 0:
                # if len(cKeyboard.currInput) > 0:
                cKeyboard.currInput.pop()
                cKeyboard.currentDict = cKeyboard.dictionaries[-1]
                cKeyboard.dictionaries.pop()
            else:
                cKeyboard.currentDict = {}
            print cKeyboard.currInput
            return
        if event.name.isalpha() and keyboard.is_pressed('shift+' + event.name):
            cKeyboard.currInput.append(event.name.upper())
        else:
            cKeyboard.currInput.append(event.name)
        print cKeyboard.currInput
        new_dict = {}
        # use ckcodes if currdict is empty
        this_dict = cKeyboard.codes if bool(cKeyboard.currentDict) is False else cKeyboard.currentDict
        print this_dict

        new_dict = updateDictionary(this_dict, cKeyboard.currInput)
        print new_dict

        if bool(new_dict) is False:
            # Let's check whether the previous input key exists in the dictionary
            if bool(cKeyboard.currentDict.get("".join(cKeyboard.currInput[:-1]))):
                print "Yay I exist " #+ char
                cKeyboard.state = "found_code_with_extra_char"
            else:
                cKeyboard.currInput = []
                cKeyboard.dictionaries = []
                cKeyboard.currentDict = {}
        # it is not the case that if the length is on then the user typed all the character codes
        # an exception is ae+: if the user types ae, len(new_dict) is one as its the only code with ae
        elif len(new_dict) == 1 and bool(cKeyboard.currentDict.get("".join(cKeyboard.currInput))):
            print "one item "
            print new_dict
            cKeyboard.state = "found_code"
        else:
            print "append: "
            print new_dict
            cKeyboard.currentDict = new_dict
            cKeyboard.dictionaries.append(new_dict)

        if cKeyboard.state == "found_code" or cKeyboard.state == "found_code_with_extra_char":
            if cKeyboard.state == "found_code":
                string = cKeyboard.currentDict.get("".join(cKeyboard.currInput))
                print "found: "+ string
                writeString(string)
                keyboard.send("backspace")
                cKeyboard.currInput = []
                cKeyboard.dictionaries = []
                cKeyboard.currentDict = {}
            elif cKeyboard.state == "found_code_with_extra_char":
                string = cKeyboard.currentDict.get("".join(cKeyboard.currInput[:-1]))
                print "found_code_with_extra_char" + cKeyboard.currInput[-1]
                writeString(string)
                keyboard.send("backspace")

                keyboard.send(cKeyboard.currInput[-1])
                # Initially I had a keyboard.send(cKeyboard.currInput[-1]) a here so the callback automatically populates
                # currInput, dictionaries and currentDict. However write function sends many other keyboard events that disrupts
                # the normal flow of the algorithm and leaves it in a state in which it was not supposed to be found.
                # So I do the manual population here
                cKeyboard.currInput = [cKeyboard.currInput[-1]]
                cKeyboard.currentDict = updateDictionary(cKeyboard.codes, cKeyboard.currInput[-1])
                cKeyboard.dictionaries = [].append(cKeyboard.currentDict)
            cKeyboard.state = "nothing"


keyboard.hook(callback)
keyboard.wait()
