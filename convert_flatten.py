import json


with open("./data/measurements.json", "r") as file:
    data = json.load(file)


flattened_data = []
for measurement_set in data:
    for measurement in measurement_set:
        ts = measurement["ts"]
        for key, values in measurement["series"].items():
            if key != "$_time":
                for i, value in enumerate(values):
                    time_point = measurement["series"]["$_time"][i]
                    flattened_data.append(
                        {"timestamp": ts, "time_point": time_point, key: value}
                    )


with open("./data/flatted.json", "w") as file:
    json.dump(flattened_data, file, indent=4)
