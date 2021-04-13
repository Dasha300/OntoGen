import csv
import json
import sys
import ftfy
import os
import re

def pathent(csv_path):
    if csv_path[len(csv_path) - 4:len(csv_path)] == '.csv':
        return csv_path
    else:
        return 1

def unocodeftfy(json_path):
    with open('input.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
        i = -1
        for strjson in text:
            i = i + 1
            for objjson in strjson:
                text[i][objjson] = ftfy.fix_text(text[i][objjson])
                j = 0
                str = ''
                for charact in text[i][objjson]:
                    str = str + text[i][objjson][j]
                    j = j + 1
                text[i][objjson] = re.sub(r'\s+', ' ', str)
                print(text[i][objjson])
    openjsonfile(json_path)

def csvent(csv_path, json_path):
    if csv_path[len(csv_path) - 4:len(csv_path)] != '.csv' or json_path[len(json_path) - 5:len(json_path)] != '.json':
        return csv_path, json_path
    else:
        return sys.exit()

def opencsvfile(csv_path):
    with open(csv_path) as f:
        reader = csv.DictReader(f, skipinitialspace=True, delimiter=',')
        rows = list(reader)
    return rows

def openjsonfile(json_path):
    with open(json_path, 'w') as f:
        json.dump(rows, f, indent=4)

path = input()

if os.path.exists(path):
    print('Такой путь существует: ', path)
    for dirs, folder, files in os.walk(path):
        for awhile in files:
            if (pathent(awhile) == 1):
                continue
            else:
                csv_path = awhile
                json_path = awhile[0:len(awhile) - 4] + '.json'
                rows = opencsvfile(csv_path)
                openjsonfile(json_path)
else:
    print('Такого пути нет', path)

csv_path = input()
json_path = input()
csvent(csv_path, json_path)
rows = opencsvfile(csv_path)
openjsonfile(json_path)
unocodeftfy(json_path)