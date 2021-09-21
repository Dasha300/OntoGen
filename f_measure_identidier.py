import json


def f_measure(json_path, json_path3, json_path4, owl_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        text = json.load(f)
        k = 0
        for str_json in text:
            k = k + 1
    with open(json_path4, 'r', encoding='utf-8') as f:
        text = json.load(f)
        i = -1
        count = 0
        categorical = 0
        subject = 0
        literal = 0
        for str_json in text:
            i = i + 1
            for obj_json in str_json:
                if text[i][obj_json] == "CATEGORICAL":
                    count = count + 2
                    categorical = categorical + 1
                if text[i][obj_json] == "SUBJECT":
                    count = count + 1
                    subject = subject + 1
                if text[i][obj_json] == "LITERAL":
                    count = count + 1
                    literal = literal + 1
    count1 = 0
    count2 = 0
    flag_object = 0
    with open(owl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.find("<owl:Class") != -1 or line.find("<owl:ObjectProperty") != -1 or line.find(
                    "<owl:DatatypeProperty") != -1:
                count1 = count1 + 1
    with open(owl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.find("<owl:NamedIndividual") != -1:
                flag_object = 1
            if flag_object == 1:
                count2 = count2 + 1
            if line.find("</owl:NamedIndividual") != -1 and count2 != 3:
                break
            if line.find("</owl:NamedIndividual") != -1 and count2 == 3:
                count2 = 0
                flag_object = 0
    count2 = count2 - 2 + categorical
    precision = count2 / count
    recall = count2 / count1
    f1 = (2 * precision * recall) / (precision + recall)
    print(json_path)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1: ", f1)

    count_individual = 0
    with open(owl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.find("<owl:NamedIndividual") != -1:
                count_individual = count_individual + 1
    count_individual1 = count2 + categorical
    precision1 = count_individual / count_individual1
    print("Precision: ", precision1)
    with open(json_path3, 'r', encoding='utf-8') as f:
        text = json.load(f)
        i = 0
        categorical_individual = 0
        subject_individual = 0
        for str_json in text:
            for obj_json in str_json:
                if text[i][obj_json] == "CATEGORICAL":
                    categorical_individual = categorical_individual + 1
                if text[i][obj_json] == "SUBJECT":
                    subject_individual = subject_individual + 1
            i = i + 1
    count_individual2 = (subject_individual + categorical_individual) * k
    recall1 = count_individual2 / count_individual1
    f11 = (2 * precision1 * recall1) / (precision1 + recall1)
    print("Recall: ", recall1)
    print("F1: ", f11)
