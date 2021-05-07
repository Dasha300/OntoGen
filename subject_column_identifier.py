import operator
import collections
from math import sqrt


CATEGORICAL_COLUMN = "CATEGORICAL"  # Categorical column type
LITERAL_COLUMN = "LITERAL"  # Literal column type
SUBJECT_COLUMN = "SUBJECT"  # Subject column type


def is_float(string):
    """
    Определение является ли строка числовым значением.
    :param string: исходная строка
    :return: True - если строка является числом, False - в противном случае
    """
    try:
        float(string.replace(",", "."))
        return True
    except ValueError:
        return False


def get_empty_cell_fraction(source_table, classified_table):
    """
    Получение доли пустых ячеек для категориальных столбцов.
    :param source_table: исходный словарь (таблица) состоящий из объектов: ключ и упоминание сущности (значение ячейки)
    :param classified_table: словарь (таблица) с типизированными столбцами
    :return: словарь c оценкой для каждого столбца
    """
    result_list = dict()
    # Вычисление общего количества ячеек в столбце
    cell_number = len(source_table)
    # Обход типов столбцов
    for column_key, column_type in classified_table.items():
        if column_type == CATEGORICAL_COLUMN:
            # Вычисление количества пустых ячеек в столбце
            empty_cell_number = 0
            for row in source_table:
                for key, mention_entity in row.items():
                    if column_key == key and not mention_entity:
                        empty_cell_number += 1
            # Вычисление доли пустых ячеек в столбце
            result_list[column_key] = empty_cell_number / cell_number

    return result_list


def get_unique_content_cell_fraction(source_table, classified_table):
    """
    Получение доли ячеек с уникальным содержимым для категориальных столбцов.
    :param source_table: исходный словарь (таблица) состоящий из объектов: ключ и упоминание сущности (значение ячейки)
    :param classified_table: словарь (таблица) с типизированными столбцами
    :return: словарь c оценкой для каждого столбца
    """
    result_list = dict()
    # Вычисление общего количества ячеек в столбце
    cell_number = len(source_table)
    # Обход типов столбцов
    for column_key, column_type in classified_table.items():
        if column_type == CATEGORICAL_COLUMN:
            # Вычисление количества ячеек с уникальным содержимым
            col = collections.Counter()
            for row in source_table:
                for key, mention_entity in row.items():
                    if column_key == key:
                        col[mention_entity] += 1
            # Вычисление доли ячеек с уникальным содержимым в столбце
            result_list[column_key] = len(col) / cell_number

    return result_list


def get_distance_from_first_ne_column(classified_table):
    """
    Получение расстояния от первого сущностного столбца для категориальных столбцов.
    :param classified_table: словарь (таблица) с типизированными столбцами
    :return: словарь c оценкой для каждого столбца
    """
    result_list = dict()
    column_number = 0
    for column_key, column_type in classified_table.items():
        if column_type == CATEGORICAL_COLUMN:
            result_list[column_key] = column_number
        column_number += 1

    return result_list


def get_average_word_number(source_table, classified_table):
    """
    Получение среднего количества слов для категориальных столбцов.
    :param source_table: исходный словарь (таблица) состоящий из объектов: ключ и упоминание сущности (значение ячейки)
    :param classified_table: словарь (таблица) с типизированными столбцами
    :return: словарь c оценкой для каждого столбца
    """
    result_list = dict()
    # Вычисление общего количества ячеек в столбце
    cell_number = len(source_table)
    # Обход типов столбцов
    for column_key, column_type in classified_table.items():
        if column_type == CATEGORICAL_COLUMN:
            # Подсчет количества слов в ячейках
            total_word_number = 0
            for row in source_table:
                for key, mention_entity in row.items():
                    if column_key == key and mention_entity:
                        total_word_number += len(mention_entity.split())
            # Вычисление среднего количества слов в ячейках столбца
            result_list[column_key] = total_word_number / cell_number

    return result_list


def define_subject_column(source_table, classified_table, index=None):
    """
    Определение сущностного (тематического) столбца на основе эвристических оценок.
    :param source_table: исходный словарь (таблица) состоящий из объектов: ключ и упоминание сущности (значение ячейки)
    :param classified_table: словарь (таблица) с типизированными столбцами
    :param index: явное указание на номер сущностного (тематического) столбца
    :return: словарь (таблица) с отмеченным сущностным (тематическим) столбцом
    """
    result_list = dict()
    # Если явно указан номер столбца, то данный столбец назначается сущностным (тематическим)
    if is_float(str(index)) and 0 <= index <= len(classified_table):
        i = 0
        for key, type_column in classified_table.items():
            if i == index:
                result_list[key] = SUBJECT_COLUMN
            else:
                result_list[key] = type_column
            i += 1
    else:
        sub_col = dict()
        # Получение доли пустых ячеек
        empty_cell_fraction = get_empty_cell_fraction(source_table, classified_table)
        # Получение доли ячеек с уникальным содержимым
        unique_content_cell_fraction = get_unique_content_cell_fraction(source_table, classified_table)
        # Получение расстояния от первого сущностного столбца
        distance_from_first_ne_column = get_distance_from_first_ne_column(classified_table)
        # Получение среднего количества слов
        average_word_number = get_average_word_number(source_table, classified_table)
        # Агрегация оценки
        for key, type_column in classified_table.items():
            if type_column == CATEGORICAL_COLUMN:
                sub_col[key] = (2 * unique_content_cell_fraction[key] + average_word_number[key] -
                                empty_cell_fraction[key]) / sqrt(distance_from_first_ne_column[key] + 1)
        # Определение ключа столбца с максимальной оценкой
        subject_key = max(sub_col.items(), key=operator.itemgetter(1))[0]
        # Формирование словаря с определенным сущностным (тематическим) столбцом
        for key, type_column in classified_table.items():
            if key == subject_key:
                result_list[key] = SUBJECT_COLUMN
            else:
                result_list[key] = type_column

    return result_list
