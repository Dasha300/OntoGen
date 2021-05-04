import csv
import json
import sys
import ftfy
import os
import re
import shutil


def litcatdefender(json_path1):
    with open(json_path1, 'r', encoding='utf-8') as f:
        text1 = []
        text = json.load(f)
        i = -1
        j = 0
        dictionary = {}
        dictionary1 = {}
        for strjson in text:
            keys = strjson.keys()
            for key in keys:
                dictionary[key] = ''
                dictionary1[key] = ''
            break
        for strjson in text:
            i = i + 1
            for objjson in strjson:
                if text[i][objjson] == 'NONE':
                    text[i][objjson] = 'CATEGORICAL'
                else:
                    text[i][objjson] = 'LITERAL'
                dictionary[objjson] = [text[j][objjson] for objjson in strjson]
        k = 0
        for key in dictionary.keys():
            dictionary1[key] = [dictionary[key][k] for key in dictionary.keys()]
            k = k + 1
        k = 0
        keys = dictionary1.keys()
        c = 0
        l = 0
        for key in keys:
            k = 0
            while (k < len(dictionary1[key])):
                if (dictionary1[key][k] == 'CATEGORICAL'):
                    c = c + 1
                else:
                    l = l + 1
                k = k + 1
            if c > l:
                dictionary1[key] = 'CATEGORICAL'
            else:
                dictionary1[key] = 'LITERAL'
            c = 0
            l = 0
            text1 = [dictionary1]
        openjsonfile(json_path2, text)
        openjsonfile(json_path3, text1)


def create_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        text = json.load(f)
        i = -1
        for strjson in text:
            i = i + 1
            for objjson in strjson:
                text[i][objjson] = ftfy.fix_text(text[i][objjson])
                str = text[i][objjson]
                result = re.search('[A-Za-z1-9]', str)
                if result:
                    result = re.search(r'^[-+]?([1-9]\d*|0)$', str)
                    if result:
                        text[i][objjson] = 'INTEGER'
                    result = re.search('[0-2][0-9][0-9][0-9]', str)
                    if result:
                        text[i][objjson] = 'DATE'
                    result = re.search(
                        '(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d|(19|20)\d\d-((0[1-9]|1[012])-(0[1-9]|[12]\d)|(0[13-9]|1[012])-30|(0[13578]|1[02])-31)',
                        str)
                    if result:
                        text[i][objjson] = 'DATE'
                    result = re.search(
                        '^(0?[1-9]|1[0-2]):[0-5][0-9]$|((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))|^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$|^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$|(?:[01]\d|2[0-3]):(?:[0-5]\d):(?:[0-5]\d)',
                        str)
                    if result:
                        text[i][objjson] = 'TIME'
                    result = re.search('^"true|false|True|False|TRUE|FALSE"&', str)
                    if result:
                        text[i][objjson] = 'LOGIC'
                    result = re.search('^\d{6}$', str)
                    if result:
                        text[i][objjson] = 'MAIL'
                    result = re.search('^[-+]?([1-9]\d*|0)\\$|\\£|\\€', str)
                    if result:
                        text[i][objjson] = 'CURRENCY'
                    result = re.search('^\d{5}(?:[-\s]\d{4})?$', str)
                    if result:
                        text[i][objjson] = 'MAIL'
                    result = re.search('^[0-9]{4}-[0-9]{3}[0-9xX]$', str)
                    if result:
                        text[i][objjson] = 'ISSN'
                    result = re.search('^(?:ISBN(?:: ?| ))?((?:97[89])?\d{9}[\dx])+$', str)
                    if result:
                        text[i][objjson] = 'ISBN'
                    result = re.search('((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)', str)
                    if result:
                        text[i][objjson] = 'IPv4'
                    result = re.search('((\\b100)|(\\b[0-9]{1,2}\\.?[0-9]?))(?=%| *percent)', str)
                    if result:
                        text[i][objjson] = 'PERCENT'
                    result = re.search(r'^([456][0-9]{3})-?([0-9]{4})-?([0-9]{4})-?([0-9]{4})$', str)
                    if result:
                        text[i][objjson] = 'CARD'
                    result = re.search(r'#[0-9A-Fa-f]{6}', str)
                    if result:
                        text[i][objjson] = 'COLOR'
                    result = re.search(r'[\w.-]+@[\w.-]+\.?[\w]+?', str)
                    if result:
                        text[i][objjson] = 'EMAIL'
                    result = re.search("[+-]?\d+\.\d+", str)
                    if result:
                        text[i][objjson] = 'FLOAT'
                else:
                    text[i][objjson] = 'SYMBOL'
                if (text[i][objjson] != 'INTEGER' and text[i][objjson] != 'SYMBOL' and text[i][objjson] != 'DATE' and
                        text[i][objjson] != 'TIME' and text[i][objjson] != 'LOGIC' and text[i][objjson] != 'MAIL' and
                        text[i][objjson] != 'CURRENCY' and text[i][objjson] != 'ISSN' and text[i][objjson] != 'ISBN' and
                        text[i][objjson] != 'IPv4' and text[i][objjson] != 'IPv6' and text[i][objjson] != 'PERCENT' and
                        text[i][objjson] != 'CARD' and text[i][objjson] != 'COLOR' and text[i][objjson] != 'EMAIL' and
                        text[i][objjson] != 'FLOAT'):
                    text[i][objjson] = 'NONE'
        openjsonfile(json_path1, text)


def path_ent(csv_path):
    if csv_path[len(csv_path) - 4:len(csv_path)] == '.csv':
        return csv_path
    else:
        return 1


def uno_code_ftfy(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        text = json.load(f)
        i = -1
        for strjson in text:
            i = i + 1
            for objjson in strjson:
                text[i][objjson] = ftfy.fix_text(text[i][objjson])
                j = 0
                str = ''
                for _ in text[i][objjson]:
                    str = str + text[i][objjson][j]
                    j = j + 1
                text[i][objjson] = re.sub(r'\s+', ' ', str)
    openjsonfile(json_path, text)


def csvent(csv_path, json_path):
    if csv_path[len(csv_path) - 4:len(csv_path)] != '.csv' or json_path[len(json_path) - 5:len(json_path)] != '.json':
        return csv_path, json_path
    else:
        return sys.exit()


def opencsvfile(csv_path):
    with open(csv_path) as f:
        reader = csv.DictReader(f, skipinitialspace=True, delimiter=',')
        rows = list(reader)
        if reader.line_num <= 1:
            return 0
        else:
            return rows


def openjsonfile(json_path, rows):
    with open(json_path, 'w') as f:
        json.dump(rows, f, indent=4)


pathin = input()
path = [pathin]
print(path)
for el in path:
    if os.path.exists(el):
        print('Такой путь существует: ', el)
        for dirs, folder, files in os.walk(el):
            for awhile in files:
                if path_ent(awhile) == 1:
                    continue
                else:
                    cl = el + '/json'
                    if os.path.exists(cl):
                        print('Такой путь существует: ', cl)
                    else:
                        os.mkdir(cl)
                    csv_path = awhile
                    json_path = awhile[0:len(awhile) - 4] + '.json'
                    rows = opencsvfile(csv_path)
                    if rows == 0:
                        continue
                    else:
                        openjsonfile(json_path, rows)
                        shutil.copyfile(json_path, cl + '/' + json_path)
                        cl = cl + '/jsondop'
                        if os.path.exists(cl):
                            print('Такой путь существует: ', cl)
                        else:
                            os.mkdir(cl)
                        json_path1 = json_path[0:len(json_path) - 4] + '1' + '.json'
                        json_path2 = json_path[0:len(json_path) - 4] + '2' + '.json'
                        json_path3 = json_path[0:len(json_path) - 4] + '3' + '.json'
                        create_json(json_path)
                        litcatdefender(json_path1)
                        shutil.copyfile(json_path1, cl + '/' + json_path1)
                        shutil.copyfile(json_path2, cl + '/' + json_path2)
                        shutil.copyfile(json_path3, cl + '/' + json_path3)
                        os.remove(json_path)
                        os.remove(json_path1)
                        os.remove(json_path2)
                        os.remove(json_path3)
    else:
        print('Такого пути нет', el)

csv_path = input()
json_path = input()
csvent(csv_path, json_path)

json_path1 = json_path[0:len(json_path) - 4] + '1' + '.json'
json_path2 = json_path[0:len(json_path) - 4] + '2' + '.json'
json_path3 = json_path[0:len(json_path) - 4] + '3' + '.json'

rows = opencsvfile(csv_path)
if rows == 0:
    sys.exit()
else:
    openjsonfile(json_path, rows)
    uno_code_ftfy(json_path)
    create_json(json_path)
    litcatdefender(json_path1)
