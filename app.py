from flask import Flask, render_template, request
from utils import *

app = Flask(__name__)


# Главная страница - вывод в таблице, поиск
@app.route('/')
@app.route('/movie/main/')
def index1():
    return render_template('index.html', movies=connection_file('netflix.db', """SELECT title, country, release_year, listed_in, description FROM netflix"""), genres=unique_genres())


# Вывод в json информации всех фильмов
@app.route('/movie/json/')
def json_list_movies():
    return render_template('json_list.html', data=create_json(connection_file('netflix.db', """SELECT title, country, release_year, listed_in, description FROM netflix""")))


# Страница поиска фильма по названию
@app.route('/movie/search/name/', methods=['POST'])
def movie_by_name():
    title_name = request.form.get('title_name')
    query = f"""SELECT title, country, release_year, listed_in, description FROM netflix WHERE netflix.title LIKE '%{title_name}%'"""
    list_of_movies = connection_file('netflix.db', query)
    films = sorted_lines(list_of_movies, 2)
    if len(films) == 1:
        movie = films[0]
        return render_template('film_by_name.html', text=f'Нашелся один фильм по запросу "{title_name}"', movie=movie, movies='')
    elif len(films) > 1:
        movie = films[-1]
        movies = films[:-1]
        return render_template('film_by_name.html', text=f'Нашлось несколько фильмов по запросу "{title_name}"', text1='Самый свежий фильм по запросу', movie=movie, movies=movies, request_title=title_name)
    else:
        return render_template('film_by_name.html', text=f'У-упс! Фильма, содержащего "{title_name}" нету', movie='')


# Страница поиска фильма по диапазону лет
@app.route('/movie/search/years/', methods=['POST'])
def movie_by_years():
    years = request.form.get('years')
    movies = get_movie_range(years)
    if movies != 0:
        return render_template("film_by_time.html", movie=movies, text=f'Нашлось что то по запросу {years}', text1=f'Количество: {len(movies)}')
    else:
        return render_template("film_by_time.html", movie='', text=f'Не нашлось ни одного фильма в диапазоне {years}')


# Страница поиска фильма по возрасту
@app.route('/movie/search/rating/', methods=['GET'])
def movie_by_rating():
    rating_movies = request.args.get("rating")
    if rating_movies == 'children':
        return render_template('film_by_rating.html', movie=search_list('G'), text='детей', text1='G')
    elif rating_movies == 'family':
        return render_template('film_by_rating.html', movie=search_list(['G', 'PG', 'PG-13']), text='семьи', text1="'G', 'PG', 'PG-13'")
    elif rating_movies == 'adult':
        return render_template('film_by_rating.html', movie=search_list(['R', 'NC-17']), text='взрослых', text1="'R', 'NC-17'")


# Страница поиска фильма по жанру
@app.route('/movie/search/genre/', methods=['GET'])
def movie_by_genre():
    movies = []
    list_genres = request.args.getlist("genre")

    key_connection = """SELECT title, release_year, listed_in, description FROM netflix"""
    movies_list = connection_file('netflix.db', key_connection)
    for genre in list_genres:
        for movie in movies_list:
            if not movie in movies and genre in movie[2]:
                movies.append(movie)
    return movies


# Страница поиска актеров
@app.route('/movie/search/cast/', methods=['POST'])
def movie_by_cast():
    actor1 = request.form.get('actor1')
    actor2 = request.form.get('actor2')
    actors = get_actors(actor1, actor2)
    if len(actors) >= 3:
        return actors[2:]
    else:
        return actors


if __name__ == '__main__':
    app.run(debug=True)
