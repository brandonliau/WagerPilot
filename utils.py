import json
import time

def writeToJson(toWrite: dict, fileName: str = None) -> None:
    """
    :param: Data to write (eg. getActiveSports), file to write to (eg. 'output.json'), whether to over write the file
    :return: None
    """
    json_object = json.dumps(toWrite, indent=4)
    if fileName == None:
        localTime = time.strftime("%H:%M:%S", time.localtime())
        with open(f'{localTime}.json', 'w') as file:
            file.write(json_object)
    else:
        with open(fileName, 'w') as file:
            file.write(json_object)

def readFromJson(fileName: str) -> dict:
    """
    :param: Data to read (eg. 'output.json')
    :return: Data from json file
    """
    try:
        with open(fileName, 'r') as file:
            output = json.load(file)
        return output
    except FileNotFoundError:
        print('Input file does not exist!')
        exit()

def div(x: int|float, y: int|float):
    """
    :param: Two numbers
    :return: The quotient of the two numbers
    """
    try:
        return x/y
    except TypeError:
        return 0