"""
Package for searching through jsons via CLI
Author: Matthew Raburn
Date: September 15 2024
"""
import sys
import json
from typing import Iterable  # Confused about this

class JsonLevel:
    """
    This class handles a level of json data
    """

    def __init__(self, level_object: Iterable, name: str = ""):
        """
        Constructs a JsonLevel object.
        :param level_object: Dictionary or list object.
        :param name: Name of the level. If no level name given then it is Top Level.
        """
        self.level_object = level_object
        self.name = name

    def __repr__(self) -> str:
        """
        Overrides __repr__.
        :return: a string representation of the JsonLevel.
        """
        print_return: str = ""  # What gets returned eventually
        level_name: str = self.name  # Name of level

        # If no level name is set then it is the Top level with no name
        if self.name == "":
            level_name = "Top"

        if isinstance(self.level_object,dict): # if level is a dictionary
            type_of_level: str = "dict"

            # use key value pairs for dictionary
            for key, value in self.level_object.items():
                if isinstance(value, dict):
                    print_return = f"{print_return}\t{key}: dict\n"
                    continue

                if isinstance(value, list):
                    print_return = f"{print_return}\t{key}: list\n"
                    continue

                print_return = f"{print_return}\t{key}: {value}: {type(value)}\n"  # Normal situation

        else:  # if level is a list
            type_of_level: str = "list"

            x = 0   # must use this to know what number element
            for element in self.level_object:
                if isinstance(element, dict):
                    print_return = f"{print_return}\tElement: {x}: dict\n"
                    x = x + 1
                    continue
                if isinstance(element, list):
                    print_return = f"{print_return}\tElement: {x}: list\n"
                    x = x + 1
                    continue
                print_return = f"{print_return}\tElement: {x}: {element}: {type(element)}\n"
                x = x + 1

        # Add it all together
        print_return = f"JSON level: {level_name} {type_of_level}:\n" + f"{print_return}"

        return print_return

    def __getitem__(self, item) -> dict or list:

        if isinstance(self.level_object, dict):
            for key, value in self.level_object.items():
                if item == key: return value

        if isinstance(self.level_object, list):
            for element in self.level_object:
                if item == element: return element

        return None


def json_explore(file_path: str) -> None:
    """
    Lets the user explore a json
    :param file_path: file path to json
    :return:
    """
    print("Q to quit")
    print("^ to go up")
    print("key value to go into\n")

    with open(file_path, 'r') as f:  # open json file as dictionary d
        json_file = f
        level = json.load(json_file)

    json_object = JsonLevel(level)  # create the json level object with no name cause it begins at the top level

    json_list: list[JsonLevel] = [json_object]  # create a list of json levels. This keeps track of the level

    # while loop handles the input from the user
    while True:
        level = json_list[-1]  # last element in the json list is current level
        print(level)  # prints the level of the json
        i = input(':')
        if i == 'Q':
            break  # exit while loop
        elif i == '^':
            if level.name == "":  # if at the top of the level and use asks to go up then just repeat the prompt
                continue
            else:
                json_list.pop()  # if not at the top of the list then pop off top element and continue while loop
                continue
        else:
            if isinstance(level.level_object, list):  # if level object is a list then convert i to int
                i = int(i)

            # Check to see if level object is a dictionary
            # then check to see if input from user matches a key
            # lastly only append the value of the key if it is a list or a dictionary
            if isinstance(level.level_object, dict):
                if i in level.level_object and (isinstance(level.level_object[i], dict) or isinstance(level.level_object[i], list)):
                    json_list.append(JsonLevel(level[i],i))  # appends the new level to the json_list stack as a dictionary level

            # Check to see if level object is a list
            # then check to see if the index is actually found in the list
            # lastly only append the value of the element if it is a list or a dictionary
            else:
                if i in range(len(level.level_object)) and (isinstance(level.level_object[i], list) or isinstance(level.level_object[i], dict)):
                    # appends the new level to the json_list stack as a list level
                    json_list.append(JsonLevel(level.level_object[i],i))
