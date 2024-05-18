import sys
import json


def list_key(key: str) -> None:
    """
    Prints out key unless at top of file
    :param key: currrent key
    :return:
    """
    if key == "":
        print(f"Top of Json: {sys.argv[1]}")
    else:
        print(f"Key: {key}")
    print("________")


def list_keys(d: dict or list) -> list[str]:
    """
    Prints values and returns values in a dictionary
    :param d: dictionary
    :return: values as a list of strings
    """
    keys = []
    if isinstance(d, list):
        index = 0
        while index < len(d):
            value_type = str(type(d[index]))
            value_type = value_type.split('\'')[1]
            if isinstance(d[index], dict):
                print(f"{index}: {value_type}")
                keys.append(str(index))
            else:
                print(f"{d[index]}: {value_type}")
            index = index + 1
    else:
        for key in d:
            value_type = str(type(d[key]))
            value_type = value_type.split('\'')[1]
            if isinstance(d[key], dict) or isinstance(d[key], list):
                print(f"{key}: {value_type}")
                keys.append(str(key))
            else:
                print(f"{key}: {d[key]} {value_type}")
    return keys


def list_node(key: str, current_node: dict or list) -> list[str]:
    """
    returns values of a node in a dictionary and prints contents of a node
    :param key: current key
    :param current_node: current node in dictionary
    :return: list of dictionaries
    """
    list_key(key)
    keys = list_keys(current_node)
    print("")
    return keys


def json_explore(file_path: str) -> None:
    print("Q to quit")
    print("^ to go up")
    print("key value to go into\n")

    with open(file_path, 'r') as f:  # open json file as dictionary d
        json_file = f
        d = json.load(json_file)

    i = ""
    node_list: list[dict] = []
    key_list: list[str] = []
    node_list.append(d)  # add the top of the dictionary to the node list
    key_list.append("")
    while i != 'Q':  # create exploration loop

        sub_dicts = list_node(key_list[-1], node_list[-1])

        i = input(":")  # get input of where the user wants to go

        if i in sub_dicts:
            key_list.append(i)
            if isinstance(node_list[-1], list):
                node_list.append(node_list[-1][int(i)])
            else:
                node_list.append(node_list[-1][i])

        elif i == "^" and key_list[-1] != "":
            key_list.pop()
            node_list.pop()

    sys.exit()


def help_print() -> None:
    print("explore [filepath]")


if __name__ == "__main__":

    # if user doesn't give enough arguments
    if len(sys.argv) == 1:
        print("Must give path to json file.")
        print("run \"explore help\" for help")

    # if user gives correct arguments
    if len(sys.argv) == 2:
        # if user uses the help argument
        if sys.argv[1] == "help":
            help_print()
        else:
            json_explore(sys.argv[1])
