from xmler import dict2xml
import json

dict1 = {"DATE": "http://www.w3.org/2001/XMLSchema#date",
         "TIME": "http://www.w3.org/2001/XMLSchema#time",
         "INTEGER": "http://www.w3.org/2001/XMLSchema#integer",
         "LOGIC": "http://www.w3.org/2001/XMLSchema#boolean",
         "MAIL": "http://www.w3.org/2001/XMLSchema#unsignedLong",
         "CURRENCY": "http://www.w3.org/2001/XMLSchema#nonNegativeInteger",
         "ISSN": "http://www.w3.org/2001/XMLSchema#token",
         "ISBN": "http://www.w3.org/2001/XMLSchema#token",
         "IPv6": "http://www.w3.org/2001/XMLSchema#token",
         "IPv4": "http://www.w3.org/2001/XMLSchema#token",
         "PERCENT": "http://www.w3.org/2001/XMLSchema#positiveInteger",
         "CARD": "http://www.w3.org/2001/XMLSchema#token",
         "COLOR": "http://www.w3.org/2001/XMLSchema#positiveInteger",
         "EMAIL": "http://www.w3.org/2001/XMLSchema#string",
         "FLOAT": "http://www.w3.org/2001/XMLSchema#float",
         "SYMBOL": "http://www.w3.org/2001/XMLSchema#token",
         "NONE": "http://www.w3.org/2001/XMLSchema#string"}


def open_file(json_file):
    """
    Открытие .json файла и извлечение содержимого
    :param json_file: название .json файла
    :return: список с содержимым .json файла
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        text = json.load(f)
    return text


def class_creator(entity_name, i):
    """
    Создание класса
    :param entity_name: название класса
    :param i: порядковый номер класса
    :return: словарь с классом
    """
    entity_name = entity_name.replace("_", "")
    ont_class = [{"Class" + str(i): {  # The root tag. Will not necessarily be root. (see #customRoot)
        "@ns": "owl",
        "@name": "Class",
        "@attrs": {
            "rdf:about": '#' + entity_name.replace(" ", "")
        }
    }}]
    return ont_class


def objectProperty_creator(entity_name, sub_name, j):
    """
    Создание объектного свойства сущности
    :param entity_name: название объектного свойства
    :param sub_name: Название домена
    :param j: порядковый номер объекта
    :return: словарь с объектным свойством сущности
    """
    entity_name = entity_name.replace("_", "")
    sub_name = sub_name.replace("_", "")
    ont_obj_prop = [{"ObjectProperty" + str(j): {  # The root tag. Will not necessarily be root. (see #customRoot)
        "@ns": "owl",
        "@name": "ObjectProperty",
        "@attrs": {
            "rdf:about": '#' + "has" + entity_name.replace(" ", "")
        },
        "domain": {
            "@ns": "rdfs",
            "@attrs": {
                "rdf:resource": '#' + sub_name.replace(" ", "")
            }
        },
        "range": {
            "@ns": "rdfs",
            "@attrs": {
                "rdf:resource": '#' + entity_name.replace(" ", "")
            }
        }
    }}]
    return ont_obj_prop


def sub_atr(s_name, subject_value, dictionary3):
    """
    Создание тега с названием индивида
    :param s_name: название класса, к которому принадлежит индивид
    :param subject_value: название атрибута тега
    :param dictionary3: словарь, в котором формируется индивид
    :return: словарь с названием индивида
    """
    s_name = s_name.replace("_", "")
    subject_value = subject_value.replace("_", "")
    dictionary5 = {
        "@ns": "rdf",
        "@attrs": {
            "rdf:resource": '#' + s_name.replace(" ", "")
        }
    }
    dictionary3.update({"@ns": "owl",
                        "@name": "NamedIndividual",
                        "@attrs": {
                            "rdf:about": '#' + subject_value.replace(" ", "")
                        }, "type": dictionary5})
    return dictionary3


def c_obj_atr(c_obj_name, c_obj_value, dictionary3):
    """
    Создание словаря с объектными свойствами индивида
    :param c_obj_name: название объектного свойства
    :param c_obj_value: значение объектного свойства
    :param dictionary3: словарь, в котором формируется индивид
    :return: словарь с объектными свойствами индивида
    """
    c_obj_name = c_obj_name.replace("_", "")
    c_obj_value = c_obj_value.replace("_", "")
    dictionary5 = {
        "@attrs": {
            "rdf:resource": '#' + c_obj_value.replace(" ", "")
        }
    }
    dictionary3.update({"has" + c_obj_name.replace(" ", ""): dictionary5})
    return dictionary3


def l_obj_atr(l_obj_name, l_obj_value, dictionary3):
    """
    Создание словаря с типом данных индивида
    :param l_obj_name: название типа данных индивида
    :param l_obj_value: литеральное значение индивида
    :param dictionary3: словарь, в котором формируется индивид
    :return: словарь с литеральными свойствами индивида
    """
    l_obj_name = l_obj_name.replace("_", "")
    l_obj_value = l_obj_value.replace("_", "")
    dictionary5 = {
        "@attrs": {
            "rdf:resource": l_obj_value.replace(" ", "")
        }
    }
    dictionary3.update({"has" + l_obj_name.replace(" ", ""): dictionary5})
    return dictionary3


def datatypeProperty_creator(obj_json, subj_name, type_name, j):
    """
    Преобразование всех заголовков L-столбцов таблицы в свойства-значения
    :param obj_json: название заголовка L-столбца
    :param subj_name: Название домена
    :param type_name: название типа данных
    :param j: порядковый номер объекта
    :return: словарь с литеральными значениями
    """
    obj_json = obj_json.replace("_", "")
    subj_name = subj_name.replace("_", "")
    ont_data_prop = [{"DatatypeProperty" + str(j): {  # The root tag. Will not necessarily be root. (see #customRoot)
        "@ns": "owl",
        "@name": "DatatypeProperty",
        "@attrs": {
            "rdf:about": '#' + "has" + obj_json.replace(" ", "")
        },
        "domain": {
            "@ns": "rdfs",
            "@attrs": {
                "rdf:resource": '#' + subj_name.replace(" ", "")
            }
        },
        "range": {
            "@ns": "rdfs",
            "@attrs": {
                "rdf:resource": type_name
            }
        }
    }}]
    return ont_data_prop


def nameIndividualCategorical_creator(obj_json, obj_name, j):
    """
    Генерация индивида
    :param obj_json: тип индивида
    :param obj_name: название индивида
    :param j: порядковый номер индивида
    :return: словарь с индивидом
    """
    obj_json = obj_json.replace("_", "")
    obj_name = obj_name.replace("_", "")
    ont_name_individual_categorical = [
        {"NamedIndividual1" + str(j): {  # The root tag. Will not necessarily be root. (see #customRoot)
            "@ns": "owl",
            "@name": "NamedIndividual",
            "@attrs": {
                "rdf:about": '#' + obj_name.replace(" ", "")
            },
            "type": {
                "@ns": "rdf",
                "@attrs": {
                    "rdf:resource": '#' + obj_json.replace(" ", "")
                }
            }
        }}]
    return ont_name_individual_categorical


def create_ontology(json_path, json_path1, json_path4, dictionary3):
    """
    Создание онтологии
    :param json_path: название исходного json-файла
    :param json_path1: название файла, в котором определены литеральные значения в ячейках
    :param json_path4: название файла с оценкой для каждого столбца
    :param dictionary3: словарь, в коором будет формироваться индивид
    :return:
    """
    json_file = json_path
    ont_namespace = {"@ns": "rdf",  # The namespace for the RootTag. The RootTag will appear as <rdf:RootTag ...>
                     "@attrs": {  # @attrs takes a dictionary. each key-value pair will become an attribute
                         "xmlns:rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                         "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
                         "xmlns:rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                         "xmlns:owl": "http://www.w3.org/2002/07/owl#",
                         "xmlns:base": "http://test.org/onto.owl",
                         "xmlns": "http://test.org/onto.owl#",
                     }}
    ont_ontology = {"Ontology": {  # The root tag. Will not necessarily be root. (see #customRoot)
        "@ns": "owl",
        "@attrs": {
            "rdf:about": "http://test.org/onto.owl"
        }
    }}
    ont_class = []
    text = open_file(json_file)
    text1 = open_file(json_path4)
    text2 = open_file(json_path1)
    i = -1
    j = 0
    entity_name = set()
    for str_json in text:
        i = i + 1
        for obj_json in str_json:
            length_set = len(entity_name)
            if (text1[0][obj_json] == "SUBJECT") or (text1[0][obj_json] == "CATEGORICAL"):
                entity_name.add((obj_json.replace(" ", "")).replace("_", ""))
                if length_set == len(entity_name):
                    continue
                else:
                    j = j + 1
                    lst = class_creator(obj_json.title(), j)
                    ont_class.extend(lst)

    entity_name = set()
    i = -1
    j = 0
    ont_obj_prop = []
    for str_json in text:
        i = i + 1
        for obj_json in str_json:
            length_set = len(entity_name)
            if text1[0][obj_json] == "SUBJECT":
                subject_name = obj_json
            if text1[0][obj_json] == "CATEGORICAL":
                entity_name.add((obj_json.replace(" ", "")).replace("_", ""))
                if length_set == len(entity_name):
                    continue
                else:
                    j = j + 1
                    lst = objectProperty_creator(obj_json.title(), subject_name.title(), j)
                    ont_obj_prop.extend(lst)

    entity_name = set()
    i = -1
    j = 0
    ont_data_prop = []
    for str_json in text:
        i = i + 1
        for obj_json in str_json:
            length_set = len(entity_name)
            if text1[0][obj_json] == "SUBJECT":
                subject_name = obj_json
            if text1[0][obj_json] == "LITERAL":
                entity_name.add((obj_json.replace(" ", "")).replace("_", ""))
                if length_set == len(entity_name):
                    continue
                else:
                    j = j + 1
                    type_name = text2[len(text2) - 1][obj_json]
                    for key, value in dict1.items():
                        if type_name == key:
                            type_name = dict1[key]
                    lst = datatypeProperty_creator(obj_json.title(), subject_name.title(), type_name, j)
                    ont_data_prop.extend(lst)

    i = -1
    entity_name = set()
    k = 1
    for str_json in text:
        i = i + 1
        for obj_json in str_json:
            length_set = len(entity_name)
            entity_name.add((text[i][obj_json].replace(" ", "")).replace("_", ""))
            if (length_set == len(entity_name)) and (
                    text1[0][obj_json] == "CATEGORICAL" or text1[0][obj_json] == "SUBJECT"):
                text[i][obj_json] = text[i][obj_json] + str(k)
    entity_name = set()
    i = -1
    j = 0
    ont_name_individual_categorical = []
    for str_json in text:
        i = i + 1
        for obj_json in str_json:
            length_set = len(entity_name)
            if text1[0][obj_json] == "CATEGORICAL":
                entity_name.add((text[i][obj_json].replace(" ", "")).replace("_", ""))
                if length_set == len(entity_name):
                    continue
                else:
                    j = j + 1
                    obj_name = text[i][obj_json]
                    lst = nameIndividualCategorical_creator(obj_json.title(), obj_name, j)
                    ont_name_individual_categorical.extend(lst)

    i = -1
    entity_name = set()
    j = 0
    dictionary2 = {}

    for str_json in text:
        i = i + 1
        for obj_json in str_json:
            length_set = len(entity_name)
            if text1[0][obj_json] == "SUBJECT":
                entity_name.add((text[i][obj_json].replace(" ", "")).replace("_", ""))
                if length_set == len(entity_name):
                    continue
                else:
                    subject_name = obj_json
                    subject_value = text[i][obj_json]
                    dictionary3 = sub_atr(subject_name.title(), subject_value, dictionary3)
            if text1[0][obj_json] == "CATEGORICAL":
                c_obj_name = obj_json
                c_obj_value = text[i][obj_json]
                dictionary3 = c_obj_atr(c_obj_name.title(), c_obj_value, dictionary3)
            if text1[0][obj_json] == "LITERAL":
                l_obj_name = obj_json
                l_obj_value = text[i][obj_json]
                dictionary3 = l_obj_atr(l_obj_name.title(), l_obj_value, dictionary3)
        dictionary2.update({"NamedIndividual" + str(j): dictionary3})
        j = j + 1
        dictionary3 = {}
    ont_name_individual_subject = [dictionary2]

    ns_no = {}
    for key in ont_namespace.keys():
        ns_no.update({key: ont_namespace[key]})
    for key in ont_ontology.keys():
        ns_no.update({key: ont_ontology[key]})
    for str_json in ont_class:
        for key in str_json.keys():
            ns_no.update({key: str_json[key]})
    for str_json in ont_obj_prop:
        for key in str_json.keys():
            ns_no.update({key: str_json[key]})
    for str_json in ont_data_prop:
        for key in str_json.keys():
            ns_no.update({key: str_json[key]})
    for str_json in ont_name_individual_categorical:
        for key in str_json.keys():
            ns_no.update({key: str_json[key]})
    for str_json in ont_name_individual_subject:
        for key in str_json.keys():
            ns_no.update({key: str_json[key]})
    dictionary = {"RDF": ns_no}
    new_string = dict2xml(dictionary, pretty=True)
    return new_string
