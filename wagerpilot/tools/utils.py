# Standard library imports
import time,json

def div(x: float, y: float):
    """
    :param: x, y
    :return: Quotient of x and y
    :usage: Allow division of two numbers even if denominator is None or 0
    """
    try:
        return x/y
    except (TypeError, ZeroDivisionError):
        return 0

def writeToJson(data: dict, fileName: str = None) -> None:
    """
    :param: data (eg. from allOdds), fileName (name of output file)
    :return: None
    :usage: Write dictionary data to json file
    """
    json_object = json.dumps(data, indent=4)
    if fileName != None:
        with open(fileName, 'w') as file:
            file.write(json_object)
    else:
        localTime = time.strftime("%H:%M:%S", time.localtime())
        with open(f'{localTime}.json', 'w') as file:
            file.write(json_object)

def readFromJson(fileName: str) -> dict:
    """
    :param: fileName (name of input file)
    :return: Data from json file
    :usage: Read json file and return it as a dictionary
    """
    try:
        with open(fileName, 'r') as file:
            output = json.load(file)
        return output
    except FileNotFoundError:
        print('Input file does not exist!')
        exit()
