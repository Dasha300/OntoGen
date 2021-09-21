import fileinput
import glob
import os


# каталог текстовых файлов
# измените на свой
def unifier(path):
    # паттерн поиска файлов по расширению
    pattern = '*.owl'

    list_files = []
    for dirs, folder, files in os.walk(path):
        for element in glob.glob(dirs + '\*.owl'):
            list_files.append(element)
    # расширение нового файла установим как '.all'
    new_file = 'new_file.owl'
    new_file1 = 'new_file1.owl'

    if list_files:
        # открываем список файлов 'list_files' на чтение
        # и новый общий файл 'new_file' на запись
        with fileinput.FileInput(files=list_files, openhook=fileinput.hook_encoded("utf-8")) as fr, open(new_file, 'w', encoding='utf-8') as fw:
            fw.write(
                '<?xml version="1.0" ?>' + "\n" + '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"xmlns:xsd="http://www.w3.org/2001/XMLSchema"xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:owl="http://www.w3.org/2002/07/owl#" xmlns:base="http://test.org/onto.owl"xmlns="http://test.org/onto.owl#">' + "\n" + "\t" + '<owl:Ontology rdf:about="http://test.org/onto.owl"/>' + "\n")
            # читаем данные построчно
            for line in fr:
                # определяем первую строку нового файла
                if line.find('xmlns') != -1:
                    line = ""
                if line.find('owl:Ontology') != -1:
                    line = ""
                if line.find('</rdf:RDF>') != -1:
                    line = ""
                if fr.isfirstline():
                    # название читаемого файла
                    file_name = fr.filename()
                    line = ""
                    # дописываем строку с названием файла
                    # fw.write(f'\n\n------------ {file_name}\n\n')

                # если нужно, то здесь обрабатываем каждую строку 'line'
                """
                if line == "<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:owl="http://www.w3.org/2002/07/owl#" xmlns:base="http://test.org/onto.owl" xmlns="http://test.org/onto.owl#">
    ":
                    line = ","
                    """
                # после обработки дописываем в общий файл
                fw.write(line)
            fw.write("</rdf:RDF>")
    with open(new_file, 'r', encoding='utf-8') as f, open(new_file1, 'w', encoding='utf-8') as fw:
        class_set = set()
        flag_object = 0
        text1 = ""
        text2 = ""
        object_set = set()
        datatype_set = set()
        individual_set = set()
        flag_datatype = 0
        flag_individual = 0
        t = 0
        list1 = []
        for line in f:
            if line.find("<owl:Class") != -1:
                k = len(class_set)
                class_set.add(line)
                if k == len(class_set):
                    line = ""
            if line.find("<owl:ObjectProperty") != -1:
                flag_object = 1
            if flag_object == 1:
                text1 = text1 + line
            if line.find("</owl:ObjectProperty") != -1:
                flag_object = 0
                l_object = len(object_set)
                object_set.add(text1)
                if l_object != len(object_set):
                    fw.write(text1)
                    text1 = ""

            if line.find("<owl:DatatypeProperty") != -1:
                text2 = ""
                flag_datatype = 1
            if flag_datatype == 1:
                text2 = text2 + line
            if line.find("</owl:DatatypeProperty") != -1:
                flag_datatype = 0
                l_datatype = len(datatype_set)
                datatype_set.add(text2)
                if l_datatype != len(datatype_set):
                    fw.write(text2)
                    text2 = ""

            if line.find("<owl:NamedIndividual") != -1:
                text3 = ""
                flag_individual = 1
            if flag_individual == 1:
                if line.find("</owl:NamedIndividual") == -1:
                    text3 = text3 + line
            if line.find("</owl:NamedIndividual") != -1:
                flag_individual = 0
                l_individual = len(individual_set)
                individual_set.add(text3)
                if l_individual != len(individual_set):
                    list1.append(text3)
                    text3 = ""
            if flag_object != 0 or flag_datatype != 0 or flag_individual != 0 or line.find(
                    "</owl:ObjectProperty") != -1 or line.find("</owl:DatatypeProperty") != -1 or line.find(
                "</owl:NamedIndividual") != -1 or line == "</rdf:RDF>":
                continue
            fw.write(line)
        list1.sort()
        list2 = set()
        list3 = set()
        for elements in list1:
            list3.add(elements)
            for another in list1:
                if len(elements) > len(another):
                    if elements.find(another) != -1:
                        list2.add(another)
                elif len(another) > len(elements):
                    if another.find(elements) != -1:
                        list2.add(elements)
        list4 = list3.difference(list2)
        for elements in list4:
            fw.write(elements)
            fw.write("\t" + "</owl:NamedIndividual>" + "\n")
        fw.write("</rdf:RDF>")
    return new_file1, new_file
