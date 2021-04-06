import csv
import json
import sys


def vvvod(csv_path, json_path):
    if csv_path[len(csv_path) - 4:len(csv_path)] == '.csv' and json_path[len(json_path) - 5:len(json_path)] == '.json':
        return csv_path, json_path
    else:
        return sys.exit()


csv_path = input()
json_path = input()
vvvod(csv_path, json_path)

with open(csv_path) as f:
    reader = csv.DictReader(f, skipinitialspace=True, delimiter=',')
    rows = list(reader)

with open(json_path, 'w') as f:
    json.dump(rows, f, indent=4)ent=4)