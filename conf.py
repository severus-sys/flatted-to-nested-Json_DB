import json

dbname = "****"
user = "****"
password = "****"
host = "*****"
port = "***"


with open("./data/flatted.json", "r") as file:
    data = json.load(file)
