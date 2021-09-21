def write_statistic(owl_path):
    text = "statistic.txt"
    with open(owl_path, 'r', encoding='utf-8') as f:
        count_individual = 0
        count_class = 0
        count_object_prop = 0
        count_datatype_prop = 0
        for line in f:
            if line.find("<owl:NamedIndividual") != -1:
                count_individual = count_individual + 1
            if line.find("<owl:Class") != -1:
                count_class = count_class + 1
            if line.find("<owl:ObjectProperty") != -1:
                count_object_prop = count_object_prop + 1
            if line.find("<owl:DatatypeProperty") != -1:
                count_datatype_prop = count_datatype_prop + 1
    with open(text, 'a', encoding='utf-8') as f:
        print("Number of classes: ", count_class)
        print("Number of object properties: ", count_object_prop)
        print("Number of datatype properties: ", count_datatype_prop)
        print("Number of Named individuals: ", count_individual)
        f.write("Number of classes: " + str(count_class) + "\n")
        f.write("Number of object properties: " + str(count_object_prop) + "\n")
        f.write("Number of datatype properties: " + str(count_datatype_prop) + "\n")
        f.write("Number of Named individuals: " + str(count_individual) + "\n" + "\n")
    return text
