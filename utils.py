import json

def writeToJson(toWrite: dict, fileName: json, overWrite: bool = True) -> None:
    """
    :param: Data to write (eg. getActiveSports), file to write to (eg. 'output.json'), whether to over write the file
    :return: None
    """
    json_object = json.dumps(toWrite, indent=4)
    if overWrite == True:
        with open(fileName, 'w') as file:
            file.write(json_object)
    else:
        with open(fileName, 'a') as file:
            file.write(json_object)

def readToDict(toRead: json) -> dict:
    """
    :param: Data to read (eg. 'output.json')
    :return: Data from json file
    """
    with open(toRead, 'r') as file:
        output = json.load(file)
    return output

def div(x,y):
    """
    :param: Two numbers
    :return: The quotient of the two numbers
    """
    try:
        return x/y
    except TypeError:
        return 0