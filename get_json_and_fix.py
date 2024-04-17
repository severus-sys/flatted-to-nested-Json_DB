import json


def check_invalid_json(file_name):
    """this functions checks json is valid or invalid

    Args:
        file_name: path of the  will checking json

    Returns:
        If json is valid  function returns True
        If not  returns False
    """
    with open(file_name, "r") as file:
        try:
            json.load(file)
            print("Json is valid")
            return True
        except json.JSONDecodeError as error:
            print("Json is not valid")
            print("Error is ", error.msg)
            print("This row number is wrong : ", error.lineno)
            return False


def fix_corrupted_json(func, file_name, output_file):
    """If  json file is invalid
    this function repairs the json file with the requested conditions
    Args:
        func : the  control function
        file_name : path of the json
        output_file : path of the  fixed json  --output--
    Returns:
        valid  JSON data  or  None
    """

    if not func(file_name):
        with open(file_name, "r") as file:
            try:
                data = file.read()
                fixed_json = "[" + data + "]"
                json_data = json.load(fixed_json)
                print("json is valid")
                with open(output_file, "w") as output:
                    json.dump(json_data, output, indent=4)
                    print("Valid JSON data saved here.", output_file)
                    return "Successfuly process"
            except json.JSONDecodeError as error:
                print("Error while decoding JSON:", error)
                return None


file = "./data/corrupted-file.json"
json_list = fix_corrupted_json(check_invalid_json, file, "./data/valid.json")
print(json_list)
