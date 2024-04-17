import json


with open("./data/valid.json", "r") as file:
    data = json.load(file)


measurements = [item["measurements"] for item in data]


with open("./data/measurements.json", "w") as new_file:
    json.dump(measurements, new_file, indent=4)
