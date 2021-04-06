import csv
import json

csv_path = input("")
json_path = input("")
with open(csv_path) as f:
    reader = csv.DictReader(f, skipinitialspace=True, delimiter=',')
    rows = list(reader)

with open(json_path, 'w') as f:
    json.dump(rows, f, indent=4)