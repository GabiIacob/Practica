import json 

with open("persoane.json", "r") as file:
    data=json.load(file)
    print(data)
