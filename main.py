import csv
import json
import sys
import ftfy
import os
import re
import shutil
import subject_column_identifier
import ontology_creator
import click


def define_literal_categorical(json_path1, json_path2, json_path3):
    """
    Определение типов столбцов
    :param json_path1: название файла, в котором определены литеральные значения в ячейках
    :param json_path2: название файла, в котором будут определены типы ячеек("CATEGORICAL" или "LITERAL")
    :param json_path3: название файла, в котором будут определены типы столбцов("CATEGORICAL" или "LITERAL")
    """
    with open(json_path1, 'r', encoding='utf-8') as f:
        text1 = []
        text = json.load(f)
        i = -1
        j = 0
        dictionary = {}
        dictionary1 = {}
        for str_json in text:
            keys = str_json.keys()
            for key in keys:
                dictionary[key] = ''
                dictionary1[key] = ''
            break
        for str_json in text:
            i = i + 1
            for obj_json in str_json:
                if text[i][obj_json] == 'NONE':
                    text[i][obj_json] = 'CATEGORICAL'
                else:
                    text[i][obj_json] = 'LITERAL'
                dictionary[obj_json] = [text[j][object_json] for object_json in str_json]
        k = 0
        for key in dictionary.keys():
            dictionary1[key] = [dictionary[key][k] for key in dictionary.keys()]
            k = k + 1
        keys = dictionary1.keys()
        c = 0
        length = 0
        error = 0
        for key in keys:
            k = 0
            while k < len(dictionary1[key]):
                if dictionary1[key][k] == 'CATEGORICAL':
                    c = c + 1
                else:
                    length = length + 1
                k = k + 1
            if c > length:
                dictionary1[key] = "CATEGORICAL"
            else:
                dictionary1[key] = 'LITERAL'
            if c == 0:
                error = error + 1
            c = 0
            length = 0
            text1 = [dictionary1]
        if error != 0:
            i = -1
            for str_json in text:
                i = i + 1
                for obj_json in str_json:
                    text[i][obj_json] = "CATEGORICAL"
                    break
            i = -1
            for str_json in text1:
                i = i + 1
                for obj_json in str_json:
                    text1[i][obj_json] = "CATEGORICAL"
                    break
        open_json_file(json_path2, text)
        open_json_file(json_path3, text1)


def create_json(json_path, json_path1):
    """
    Определение литеральных значений в ячейках
    :param json_path: название исходного json-файла
    :param json_path1: название файла, в котором будут определены литеральные значения в ячейках
    :return:
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        text = json.load(f)
        i = -1
        for str_json in text:
            i = i + 1
            for obj_json in str_json:
                text[i][obj_json] = ftfy.fix_text(text[i][obj_json])
                text_string = text[i][obj_json]
                if text[i][obj_json] == 'NONE':
                    text[i][obj_json] = 'SYMBOL'
                result = re.search('[A-Za-z0-9А-Яа-я]', text_string)
                if result:
                    result = re.search(r'^[-+]?[0-9]+$', text_string)
                    if result:
                        text[i][obj_json] = 'INTEGER'
                    result = re.search('[0-2][0-9][0-9][0-9]', text_string)
                    if result:
                        text[i][obj_json] = 'DATE'
                    result = re.search(
                        '(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d|(19|20)\d\d-((0[1-9]|1[012])-(0[1-9]|[12]\d)|(0[13-9]|1[012])-30|(0[13578]|1[02])-31)',
                        text_string)
                    if result:
                        text[i][obj_json] = 'DATE'
                    result = re.search(
                        '^(0?[1-9]|1[0-2]):[0-5][0-9]$|((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))|^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$|^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$|(?:[01]\d|2[0-3]):(?:[0-5]\d):(?:[0-5]\d)',
                        text_string)
                    if result:
                        text[i][obj_json] = 'TIME'
                    result = re.search('^"true|false|True|False|TRUE|FALSE"&', text_string)
                    if result:
                        text[i][obj_json] = 'LOGIC'
                    result = re.search('^\d{6}$', text_string)
                    if result:
                        text[i][obj_json] = 'MAIL'
                    result = re.search('^[-+]?([1-9]\d*|0)\\$|\\£|\\€', text_string)
                    if result:
                        text[i][obj_json] = 'CURRENCY'
                    result = re.search('^\d{5}(?:[-\s]\d{4})?$', text_string)
                    if result:
                        text[i][obj_json] = 'MAIL'
                    result = re.search('^[0-9]{4}-[0-9]{3}[0-9xX]$', text_string)
                    if result:
                        text[i][obj_json] = 'ISSN'
                    result = re.search('^(?:ISBN(?:: ?| ))?((?:97[89])?\d{9}[\dx])+$', text_string)
                    if result:
                        text[i][obj_json] = 'ISBN'
                    result = re.search('((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)', text_string)
                    if result:
                        text[i][obj_json] = 'IPv4'
                    result = re.search('((\\b100)|(\\b[0-9]{1,2}\\.?[0-9]?))(?=%| *percent)', text_string)
                    if result:
                        text[i][obj_json] = 'PERCENT'
                    result = re.search(r'^([456][0-9]{3})-?([0-9]{4})-?([0-9]{4})-?([0-9]{4})$', text_string)
                    if result:
                        text[i][obj_json] = 'CARD'
                    result = re.search(r'#[0-9A-Fa-f]{6}', text_string)
                    if result:
                        text[i][obj_json] = 'COLOR'
                    result = re.search(r'[\w.-]+@[\w.-]+\.?[\w]+?', text_string)
                    if result:
                        text[i][obj_json] = 'EMAIL'
                    result = re.search("[+-]?\d+\.\d+", text_string)
                    if result:
                        text[i][obj_json] = 'FLOAT'
                if (text[i][obj_json] != 'INTEGER' and text[i][obj_json] != 'SYMBOL' and text[i][obj_json] != 'DATE' and
                        text[i][obj_json] != 'TIME' and text[i][obj_json] != 'LOGIC' and text[i][obj_json] != 'MAIL' and
                        text[i][obj_json] != 'CURRENCY' and text[i][obj_json] != 'ISSN' and text[i][
                            obj_json] != 'ISBN' and
                        text[i][obj_json] != 'IPv4' and text[i][obj_json] != 'IPv6' and text[i][
                            obj_json] != 'PERCENT' and
                        text[i][obj_json] != 'CARD' and text[i][obj_json] != 'COLOR' and text[i][
                            obj_json] != 'EMAIL' and
                        text[i][obj_json] != 'FLOAT'):
                    text[i][obj_json] = 'NONE'
        open_json_file(json_path1, text)


def check_path_ent(csv_path):
    """
    Проверка, является ли файл .csv файлом
    :param csv_path: название файла
    :return: название файла, если это .csv файл, иначе 1
    """
    if csv_path[len(csv_path) - 4:len(csv_path)] == '.csv':
        return csv_path
    else:
        return 1


def uno_code_ftfy(json_path):
    """
    Исправление битых символов и удаление лишних пробелов
    :param json_path: название json файла
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        text = json.load(f)
        new_dictionary = {}
        text1 = []
        i = -1
        for str_json in text:
            i = i + 1
            for obj_json in str_json:
                if text[i][obj_json] is None:
                    text[i][obj_json] = ""
                json_str = ftfy.fix_text(str(text[i][obj_json]))
                json_str = re.sub(r'\s+', ' ', json_str)
                json_str = re.sub(
                    r'[\!\?\№\»\^\&\*\[\]\{\}\+\=\(\)\’\/\\\|\_\№\&\<\>\-\$\#\%\`\±\−\,\′\×\;\°\–\'\≥\•\½\:]', '',
                    json_str)
                json_str = re.sub(r'\s+', ' ', json_str)
                if json_str == "":
                    json_str = "NONE"
                new_obj_json = ftfy.fix_text(obj_json)
                new_obj_json = re.sub(r'\s+', ' ', new_obj_json)
                new_obj_json = re.sub(
                    r'[\!\?\№\»\^\&\*\[\]\{\}\+\=\(\)\’\/\\\|\_\№\&\<\>\-\$\#\%\`\±\−\,\′\×\;\°\–\'\≥\•\½\:]', '',
                    new_obj_json)
                new_obj_json = re.sub(r'\s+', ' ', new_obj_json)
                if new_obj_json == "":
                    new_obj_json = "NONE"
                new_dictionary[new_obj_json] = json_str
            text1.append(new_dictionary)
            new_dictionary = {}
    open_json_file(json_path, text1)


def open_csv_file(csv_path):
    """
    Открытие .csv файла
    :param csv_path: название .csv файла
    :return: 0, если файл пуст, rows(строка) - содержимое .csv файла
    """
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f, skipinitialspace=True, delimiter=',')
        rows = list(reader)
        if reader.line_num <= 1:
            return 0
        else:
            return rows


def open_json_file(json_path, rows):
    """
    Запись .json файла
    :param json_path: название .json файла
    :param rows: список с содержимым .json файла
    """
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rows, f, indent=4, ensure_ascii=False, )


@click.command()
@click.option("--name", prompt="Your path name", help="The path to the folder.")
def folder_owl(name):
    """
    Консольное взаимодействие с пользователем
    :param name: название пути к файлу, введенное пользователем
    """
    click.echo(f"{name}")
    path_in = name
    path = [path_in]
    # path = ['fj:\\test']
    for el in path:
        if os.path.exists(el):
            print('Такой путь существует: ', el)
            for dirs, folder, files in os.walk(el):
                for awhile in files:
                    if check_path_ent(awhile) == 1 and awhile[len(awhile) - 5:len(awhile)] != '.json':
                        continue
                    else:
                        cl = el + '/json'
                        if os.path.exists(cl):
                            print('Такой путь существует: ', cl)
                        else:
                            os.mkdir(cl)
                        csv_path = path_in + '/' + awhile
                        if awhile[len(awhile) - 5:len(awhile)] != '.json':
                            json_path = awhile[0:len(awhile) - 4] + '.json'
                            rows = open_csv_file(csv_path)
                        else:
                            json_full_path = path_in + '/' + awhile
                            with open(json_full_path, 'r', encoding='utf-8') as fileopen:
                                rows = json.load(fileopen)
                                json_path = awhile
                        if rows == 0:
                            continue
                        else:
                            open_json_file(json_path, rows)
                            shutil.copyfile(json_path, cl + '/' + json_path)
                            oa = cl + '/owl'
                            if os.path.exists(oa):
                                print('Такой путь существует: ', cl)
                            else:
                                os.mkdir(oa)
                            cl = cl + '/jsondocs'
                            if os.path.exists(cl):
                                print('Такой путь существует: ', cl)
                            else:
                                os.mkdir(cl)
                            json_path1 = json_path[0:len(json_path) - 5] + '1' + '.json'
                            json_path2 = json_path[0:len(json_path) - 5] + '2' + '.json'
                            json_path3 = json_path[0:len(json_path) - 5] + '3' + '.json'
                            json_path4 = json_path[0:len(json_path) - 5] + '4' + '.json'
                            owl_path = json_path[0:len(json_path) - 5] + '.owl'
                            uno_code_ftfy(json_path)
                            create_json(json_path, json_path1)
                            define_literal_categorical(json_path1, json_path2, json_path3)
                            with open(json_path3, 'r', encoding='utf-8') as f:
                                text = json.load(f)
                                with open(json_path, 'r', encoding='utf-8') as f1:
                                    text1 = json.load(f1)
                                    i = 0
                                    while i < len(text1):
                                        dictionary2 = subject_column_identifier.define_subject_column(text1[i], text[0])
                                        i += 1
                            text = [dictionary2]
                            open_json_file(json_path4, text)
                            dictionary3 = {}
                            new_string = ontology_creator.create_ontology(json_path, json_path1, json_path4,
                                                                          dictionary3)
                            with open(owl_path, "w", encoding='utf-8') as my_file:
                                my_file.write(new_string)
                            shutil.copyfile(json_path1, cl + '/' + json_path1)
                            shutil.copyfile(json_path2, cl + '/' + json_path2)
                            shutil.copyfile(json_path3, cl + '/' + json_path3)
                            shutil.copyfile(json_path4, cl + '/' + json_path4)
                            shutil.copyfile(owl_path, oa + '/' + owl_path)
                            os.remove(json_path)
                            os.remove(json_path1)
                            os.remove(json_path2)
                            os.remove(json_path3)
                            os.remove(json_path4)
                            os.remove(owl_path)
        else:
            print('Такого пути нет', el)
            """
    def file_creator(name1):

        Консольное взаимодействие с пользователем
        :param name1: название файла, введенное пользователем

        click.echo(f"{name1}")
        csv_file = name1
        if os.path.exists(csv_file):
            print('Такой файл существует: ', csv_file)
            if check_path_ent(csv_file) == 1 and csv_file[len(csv_file) - 5:len(csv_file)] != '.json':
                sys.exit()
            else:
                if csv_file[len(csv_file) - 4:len(csv_file)] == '.csv':
                    json_file = csv_file[0:len(csv_file) - 4] + '.json'
                    file_rows = open_csv_file(csv_file)
                else:
                    json_file = csv_file
                    with open(json_file, 'r', encoding='utf-8') as fileopen:
                        file_rows = json.load(fileopen)
                json_file1 = json_file[0:len(json_file) - 5] + '1' + '.json'
                json_file2 = json_file[0:len(json_file) - 5] + '2' + '.json'
                json_file3 = json_file[0:len(json_file) - 5] + '3' + '.json'
                json_file4 = json_file[0:len(json_file) - 5] + '4' + '.json'
                owl_file = json_file[0:len(json_file) - 5] + '.owl'
                if file_rows == 0:
                    sys.exit()
                else:
                    open_json_file(json_file, file_rows)
                    uno_code_ftfy(json_file)
                    create_json(json_file, json_file1)
                    define_literal_categorical(json_file1, json_file2, json_file3)
                    with open(json_file3, 'r', encoding='utf-8') as fj:
                        file_text = json.load(fj)
                        with open(json_file, 'r', encoding='utf-8') as fj1:
                            file_text1 = json.load(fj1)
                            t = 0
                            while t < len(file_text1):
                                file_dictionary = subject_column_identifier.define_subject_column(file_text1[t],
                                                                                                  file_text[0])
                                t += 1
                    file_text = [file_dictionary]
                    open_json_file(json_file4, file_text)
                    dictionary3_file = {}
                    new_file_string = ontology_creator.create_ontology(json_file, json_file1,
                                                                       json_file4, dictionary3_file)
                    with open(owl_file, "w", encoding='utf-8') as my_single_file:
                        my_single_file.write(new_file_string)
        else:
            print('Такого файла нет', csv_file)

    file_creator()
"""


if __name__ == '__main__':
    folder_owl()
