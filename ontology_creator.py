from xmler import dict2xml
import json

dict1 = {"DATE" : "http://www.w3.org/2001/XMLSchema#date",
        "TIME" : "http://www.w3.org/2001/XMLSchema#time",
        "INTEGER" : "http://www.w3.org/2001/XMLSchema#integer",
        "LOGIC" : "http://www.w3.org/2001/XMLSchema#boolean",
        "MAIL" : "http://www.w3.org/2001/XMLSchema#unsignedLong",
        "CURRENCY" : "http://www.w3.org/2001/XMLSchema#nonNegativeInteger",
        "ISSN" : "http://www.w3.org/2001/XMLSchema#token",
        "ISBN" : "http://www.w3.org/2001/XMLSchema#token",
        "IPv6" : "http://www.w3.org/2001/XMLSchema#token",
        "IPv4" : "http://www.w3.org/2001/XMLSchema#token",
        "PERCENT" : "http://www.w3.org/2001/XMLSchema#positiveInteger",
        "CARD" : "http://www.w3.org/2001/XMLSchema#token",
        "COLOR": "http://www.w3.org/2001/XMLSchema#positiveInteger",
        "EMAIL": "http://www.w3.org/2001/XMLSchema#string",
        "FLOAT": "http://www.w3.org/2001/XMLSchema#float",
        "SYMBOL" : "http://www.w3.org/2001/XMLSchema#token",
        "NONE" : "http://www.w3.org/2001/XMLSchema#string"}


def open_file(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        text = json.load(f)
    return text


def class_creator(entity_name, i):
    entity_name = entity_name.replace("_", "")
    ont_class = [{"Class" + str(i): {  # The root tag. Will not necessarily be root. (see #customRoot)
        "@ns": "owl",
        "@name": "Class",
        "@attrs": {
            "rdf:about": '#' + entity_name.replace(" ", "")
        }
    }}]
    return ont_class


def objectProperty_creator(entity_name, subject_name, j):
    entity_name = entity_name.replace("_", "")
    subject_name = subject_name.replace("_", "")
    ont_objprop = [{"ObjectProperty" + str(j): {  # The root tag. Will not necessarily be root. (see #customRoot)
        "@ns": "owl",
        "@name": "ObjectProperty",
        "@attrs": {
            "rdf:about": '#' + "has" + entity_name.replace(" ", "")
        },
        "domain": {
            "@ns": "rdfs",
            "@attrs": {
                "rdf:resource": '#' + subject_name.replace(" ", "")
            }
        },
        "range": {
            "@ns": "rdfs",
            "@attrs": {
                "rdf:resource": '#' + entity_name.replace(" ", "")
            }
        }
    }}]
    return ont_objprop


def sub_atribute(subject_name, subject_value,dictionary3):
    subject_name=subject_name.replace("_", "")
    subject_value = subject_value.replace("_", "")
    dictionary5 = {
        "@ns": "rdf",
        "@attrs": {
            "rdf:resource": '#' + subject_name.replace(" ", "")
        }
    }
    dictionary3.update({"@ns": "owl",
                        "@name": "NamedIndividual",
                        "@attrs": {
                            "rdf:about": '#' + subject_value.replace(" ", "")
                        }, "type": dictionary5})
    return dictionary3


def cobj_atribute(cobj_name, cobj_value,dictionary3):
    cobj_name = cobj_name.replace("_", "")
    cobj_value = cobj_value.replace("_", "")
    dictionary5 = {
        "@attrs": {
            "rdf:resource": '#' + cobj_value.replace(" ", "")
        }
    }
    dictionary3.update({"has" + cobj_name.replace(" ", ""): dictionary5})
    return dictionary3


def lobj_atribute(lobj_name, lobj_value,dictionary3):
    lobj_name = lobj_name.replace("_", "")
    lobj_value = lobj_value.replace("_", "")

    dictionary5 = {
        "@attrs": {
            "rdf:resource": lobj_value.replace(" ", "")
        }
    }
    dictionary3.update({"has" + lobj_name.replace(" ", ""): dictionary5})
    return dictionary3

def datatypeProperty_creator(objjson, subject_name, type_name, j):
    objjson = objjson.replace("_", "")
    subject_name = subject_name.replace("_", "")
    ont_dataprop = [{"DatatypeProperty" + str(j): {  # The root tag. Will not necessarily be root. (see #customRoot)
        "@ns": "owl",
        "@name": "DatatypeProperty",
        "@attrs": {
            "rdf:about": '#' + "has" + objjson.replace(" ", "")
        },
        "domain": {
            "@ns": "rdfs",
            "@attrs": {
                "rdf:resource": '#' + subject_name.replace(" ", "")
            }
        },
        "range": {
            "@ns": "rdfs",
            "@attrs": {
                "rdf:resource": type_name
            }
        }
    }}]
    return ont_dataprop


def nameIndividualCategorical_creator(objjson, obj_name, j):
    objjson = objjson.replace("_", "")
    obj_name = obj_name.replace("_", "")
    ont_nameIndividCategorical = [
        {"NamedIndividual1" + str(j): {  # The root tag. Will not necessarily be root. (see #customRoot)
            "@ns": "owl",
            "@name": "NamedIndividual",
            "@attrs": {
                "rdf:about": '#' + obj_name.replace(" ", "")
            },
            "type": {
                "@ns": "rdf",
                "@attrs": {
                    "rdf:resource": '#' + objjson.replace(" ", "")
                }
            }
        }}]
    return ont_nameIndividCategorical

def create_ontology(json_path,json_path1,json_path4,dictionary3):
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
    length_set = 0
    for strjson in text:
        i = i + 1
        for objjson in strjson:
            length_set = len(entity_name)
            if (text1[0][objjson] == "SUBJECT") or (text1[0][objjson] == "CATEGORICAL"):
                entity_name.add((objjson.replace(" ","")).replace("_",""))
                if length_set == len(entity_name):
                    continue
                else:
                    j = j + 1
                    lst = class_creator(objjson.title(), j)
                    ont_class.extend(lst)

    entity_name = set()
    length_set = 0
    i = -1
    j = 0
    ont_objprop = []
    for strjson in text:
        i = i + 1
        for objjson in strjson:
            length_set = len(entity_name)
            if text1[0][objjson] == "SUBJECT":
                subject_name = objjson
            if text1[0][objjson] == "CATEGORICAL":
                entity_name.add((objjson.replace(" ","")).replace("_",""))
                if length_set == len(entity_name):
                    continue
                else:
                    j = j + 1
                    lst = objectProperty_creator(objjson.title(), subject_name.title(), j)
                    ont_objprop.extend(lst)

    entity_name = set()
    length_set = 0
    i = -1
    j = 0
    ont_dataprop = []
    for strjson in text:
        i = i + 1
        for objjson in strjson:
            length_set = len(entity_name)
            if text1[0][objjson] == "SUBJECT":
                subject_name = objjson
            if text1[0][objjson] == "LITERAL":
                entity_name.add((objjson.replace(" ","")).replace("_",""))
                if length_set == len(entity_name):
                    continue
                else:
                    j = j + 1
                    type_name = text2[len(text2)-1][objjson]
                    for key, value in dict1.items():
                        if type_name == key:
                            type_name = dict1[key]
                    lst = datatypeProperty_creator(objjson.title(), subject_name.title(), type_name, j)
                    ont_dataprop.extend(lst)

    i = -1
    entity_name = set()
    length_set = 0
    ont_nameIndividSubject = []
    j = 0
    dictionary2 = {}
    k = 1
    for strjson in text:
        i = i + 1
        for objjson in strjson:
            length_set = len(entity_name)
            entity_name.add((text[i][objjson].replace(" ", "")).replace("_", ""))
            if (length_set == len(entity_name)) and (text1[0][objjson] == "CATEGORICAL" or text1[0][objjson] == "SUBJECT"):
                text[i][objjson] = text[i][objjson] + str(k)
    entity_name = set()
    length_set = 0
    i = -1
    j = 0
    ont_nameIndividCategorical = []
    for strjson in text:
        i = i + 1
        for objjson in strjson:
            length_set = len(entity_name)
            if text1[0][objjson] == "CATEGORICAL":
                entity_name.add((text[i][objjson].replace(" ", "")).replace("_", ""))
                if length_set == len(entity_name):
                    continue
                else:
                    j = j + 1
                    obj_name = text[i][objjson]
                    lst = nameIndividualCategorical_creator(objjson.title(), obj_name, j)
                    ont_nameIndividCategorical.extend(lst)

    i = -1
    entity_name = set()
    length_set = 0
    ont_nameIndividSubject = []
    j = 0
    dictionary2 = {}

    for strjson in text:
        i = i + 1
        for objjson in strjson:
            length_set = len(entity_name)
            if text1[0][objjson] == "SUBJECT":
                entity_name.add((text[i][objjson].replace(" ", "")).replace("_", ""))
                if length_set == len(entity_name):
                    continue
                else:
                    subject_name = objjson
                    subject_value = text[i][objjson]
                    dictionary3 = sub_atribute(subject_name.title(), subject_value,dictionary3)
            if (text1[0][objjson] == "CATEGORICAL"):
                cobj_name = objjson
                cobj_value = text[i][objjson]
                dictionary3 = cobj_atribute(cobj_name.title(), cobj_value,dictionary3)
            if (text1[0][objjson] == "LITERAL"):
                lobj_name = objjson
                lobj_value = text[i][objjson]
                dictionary3 = lobj_atribute(lobj_name.title(), lobj_value,dictionary3)
        dictionary2.update({"NamedIndividual" + str(j): dictionary3})
        j = j + 1
        dictionary3 = {}
    ont_nameIndividSubject = [dictionary2]

    ns_no = {}
    for key in ont_namespace.keys():
        ns_no.update({key: ont_namespace[key]})
    for key in ont_ontology.keys():
        ns_no.update({key: ont_ontology[key]})
    for strjson in ont_class:
        for key in strjson.keys():
            ns_no.update({key: strjson[key]})
    for strjson in ont_objprop:
        for key in strjson.keys():
            ns_no.update({key: strjson[key]})
    for strjson in ont_dataprop:
        for key in strjson.keys():
            ns_no.update({key: strjson[key]})
    for strjson in ont_nameIndividCategorical:
        for key in strjson.keys():
            ns_no.update({key: strjson[key]})
    for strjson in ont_nameIndividSubject:
        for key in strjson.keys():
            ns_no.update({key: strjson[key]})
    Dict = {"RDF": ns_no}
    new_string = dict2xml(Dict, pretty=True)
    return new_string