import sqlite3
import json


# Для этого задания, как пример: connection_file('netflix.db', """SELECT * FROM netflix""")
def connection_file(filename, key):
    """
    Функция, которая открывает файл, берет необходимую информацию и возвращает словарь из подходящих данных.
    :param filename: Название файла, с которого будет браться информация.
    :param key: Указывает что и откуда берем из файла.
    :return: Возвращает список с подходящими данными.
    """
    with sqlite3.connect(filename) as connection:
        cursor = connection.cursor()
        query = key
        cursor.execute(query)
        return cursor.fetchall()


# Для этого задания, как пример: sorted_lines(list_of_movies, 2)
def sorted_lines(lines, sorted_by, reverse=False):
    """
    Функция, которая возвращает отсортированный список по какому-то ключу.
    :param reverse: Отвечает за переворот текста. По умолчанию стоит False
    :param lines: Список, который нужно отсортировать по какому-то ключу.
    :param sorted_by: Ключ, по которому надо сортировать
    :return: Сортированный список по ключу
    """
    return sorted(lines, key=lambda x: x[sorted_by], reverse=reverse)


# Для этого задания, как пример: create_json(connection_file('netflix.db', """SELECT title, country, release_year, listed_in, description FROM netflix"""))
def create_json(line):
    """
    Функция, которая превращает данные в json формат.
    :param line: Данные, которые надо превратить в json.
    :return: Данные в формате json.
    """
    return json.dumps(line, indent=4)


# Достает и возвращает уникальные жанры, нужно для вывода в шаблоне html
def unique_genres():
    list_genres = []
    data = connection_file('netflix.db', """SELECT DISTINCT listed_in FROM netflix""")
    for i in data:
        i = ''.join(list(i)).split(', ')
        for j in i:
            if j not in list_genres:
                list_genres.append(j)
    return list_genres


# Берет двух актеров и выводит список актеров
def get_actors(actor1, actor2):
    """
    Функция, которая принимает двух актеров и выводит список тех, кто играет с ними в паре больше 2 раз
    :param actor1: Актер номер 1
    :param actor2: Актер номер 2
    :return: Список тех, кто играет с ними в паре больше 2 раз
    """
    key_connection = f""" SELECT netflix.cast FROM netflix WHERE netflix.cast LIKE '%{actor1}%{actor2}%'"""
    actors = connection_file('netflix.db', key_connection)
    list_actors = {}
    for actor in actors:
        for i in actor[0].split(', '):
            if i in list_actors.keys():
                list_actors[i] += 1
            else:
                list_actors[i] = 1
    result = []
    for k, v in list_actors.items():
        if v >= 2:
            result.append(k)
    return result


def get_movie_range(years):
    try:
        year1, year2 = years.split(', ')
    except:
        return 0
    key_connection = f"""SELECT title, release_year, description FROM netflix WHERE release_year BETWEEN {year1} AND {year2}"""
    movies = connection_file('netflix.db', key_connection)
    movies = sorted_lines(movies, 1, True)
    return movies


def search_list(list_search):
    list_select = 'title, rating, release_year, description'
    if type(list_search) is list:
        key_connection = f"""SELECT {list_select} FROM netflix WHERE rating in {tuple(list_search)}"""
    else:
        key_connection = f"""SELECT {list_select} FROM netflix WHERE rating = '{list_search}'"""
    movies = connection_file('netflix.db', key_connection)
    return movies


def step_6(type_of_movie, release_year, genres):
    list_movies = []
    key_connection = f"""SELECT title, description FROM netflix WHERE type = '{type_of_movie}' AND release_year = {release_year} AND listed_in LIKE  '%{genres}%'"""
    movies = connection_file('netflix.db', key_connection)
    for movie in movies:
        list_movies.append({'title': movie[0], 'description': movie[1]})
    return list_movies
