import fileinput
import glob
import os


def unifier(path):
    """
    Создание единой онтологии на основе созданных онтологий из каждого файла.
    :param path: Путь к файлам, где хранятся онтологии
    :return: Файл единой онтологии
    """
    list_files = []
    for dirs, folder, files in os.walk(path):
        for element in glob.glob(dirs + '\*.owl'):
            list_files.append(element)
    new_file = 'TotalOntology.owl'
    class_set = set()
    flag_object = 0
    key = ""
    named_individual_dictionary = dict()
    flag_datatype = 0
    flag_individual = 0
    object_dictionary = dict()
    datatype_dictionary = dict()
    if list_files:
        with fileinput.FileInput(files=list_files, openhook=fileinput.hook_encoded("utf-8")) as fr:
            for line in fr:
                if line.find("<owl:Class") != -1:
                    class_set.add(line)

                if line.find("<owl:ObjectProperty") != -1:
                    key = line
                    flag_object = 1
                    object_dictionary.setdefault(line, [])
                if flag_object == 1:
                    if line.find("<owl:ObjectProperty") == -1:
                        object_dictionary[key].append(line)
                if line.find("</owl:ObjectProperty") != -1:
                    object_dictionary[key].pop()
                    object_dictionary[key] = list(set(object_dictionary[key]))
                    flag_object = 0

                if line.find("<owl:DatatypeProperty") != -1:
                    key = line
                    flag_datatype = 1
                    datatype_dictionary.setdefault(line, [])
                if flag_datatype == 1:
                    if line.find("<owl:DatatypeProperty") == -1:
                        datatype_dictionary[key].append(line)
                if line.find("</owl:DatatypeProperty") != -1:
                    datatype_dictionary[key].pop()
                    datatype_dictionary[key] = list(set(datatype_dictionary[key]))
                    flag_datatype = 0

                if line.find("<owl:NamedIndividual") != -1:
                    flag_individual = 1
                    key = line
                    named_individual_dictionary.setdefault(line, [])
                if flag_individual == 1:
                    if line.find("<owl:NamedIndividual") == -1:
                        named_individual_dictionary[key].append(line)
                if line.find("</owl:NamedIndividual") != -1:
                    named_individual_dictionary[key].pop()
                    named_individual_dictionary[key] = list(set(named_individual_dictionary[key]))
                    flag_individual = 0
    with open(new_file, 'w', encoding='utf-8') as fw:
        fw.write(
            '<?xml version="1.0" ?>' + "\n" +
            '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:xsd="http://www.w3.org/2001'
            '/XMLSchema" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:owl="http://www.w3.org/2002/07/owl#" '
            'xmlns:base="http://test.org/onto.owl" xmlns="http://test.org/onto.owl#">' + "\n"
            + "\t" + '<owl:Ontology rdf:about="http://test.org/onto.owl"/>' + "\n")
        for element in class_set:
            fw.write(element)
        for key, elements in object_dictionary.items():
            fw.write(key)
            object_dictionary[key].append("\t</owl:ObjectProperty>\n")
            for element in elements:
                fw.write(element)
        for key, elements in datatype_dictionary.items():
            fw.write(key)
            datatype_dictionary[key].append("\t</owl:DatatypeProperty>\n")
            for element in elements:
                fw.write(element)
        for key, elements in named_individual_dictionary.items():
            fw.write(key)
            named_individual_dictionary[key].append("\t</owl:NamedIndividual>\n")
            for element in elements:
                fw.write(element)
        fw.write("</rdf:RDF>")
    return new_file
