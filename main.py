import csv
import json
import sys
import ftfy
import os

#  print(ftfy.fix_text('HTML entities &lt;3'))


def pathent(csv_path):
    if csv_path[len(csv_path) - 4:len(csv_path)] == '.csv':
        return csv_path
    else:
        return 1


def csvent(csv_path, json_path):
    if csv_path[len(csv_path) - 4:len(csv_path)] != '.csv' or json_path[len(json_path) - 5:len(json_path)] != '.json':
        return csv_path, json_path
    else:
        return sys.exit()


path = input()

#  path = ['F:/test']
if os.path.exists(path):
    print('Такой путь существует: ', path)
    for dirs, folder, files in os.walk(path):
        print('Выбранный каталог: ', dirs)
        print('Вложенные папки: ', folder)
        print('Файлы в папке: ', files)
        print('\n')
        for awhile in files:
            if (pathent(awhile) == 1):
                print("Не csv")
                continue
            else:
                csv_path = awhile
                json_path = awhile[0:len(awhile) - 4] + '.json'

                with open(csv_path) as f:
                    reader = csv.DictReader(f, skipinitialspace=True, delimiter=',')
                    rows = list(reader)

                with open(json_path, 'w') as f:
                    json.dump(rows, f, indent=4)
                print(json_path)
else:
    print('Такого пути нет', path)

csv_path = input()
json_path = input()
csvent(csv_path, json_path)

#  csv_path = 'input.csv'
#  json_path = 'output.json'

with open(csv_path) as f:
    reader = csv.DictReader(f, skipinitialspace=True, delimiter=',')
    rows = list(reader)

with open(json_path, 'w') as f:
    json.dump(rows, f, indent=4)
