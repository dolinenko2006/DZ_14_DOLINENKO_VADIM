from flask import Flask, jsonify
from utils import get_one, get_all, search_by_cast


app = Flask(__name__)

@app.get('/movie/<title>')                     # работает # http://127.0.0.1:5000/movie/zoom
def get_by_title(title:str):
    query = f"""
    SELECT * 
    FROM netflix
    WHERE title LIKE '%{title}%'
    ORDER BY date_added DESC
    """

    query_result = get_one(query)

    if query_result is None:
        return jsonify(status=404)

    movie = {
        'title': query_result['title'],
        'country': query_result['country'],
        'release_year': query_result['release_year'],
        'genre': query_result['listed_in'],
        'description': query_result['description'],
    }
    return jsonify(movie)


@app.get('/movie/<year1>/to/<year2>')                # не работает   # http://127.0.0.1:5000/movie/2010/to/2011
def get_movie_by_year(year1: str, year2: str):
    query = f"""
    SELECT * 
    FROM netflix
    WHERE release_year BETWEEN {year1} AND {year2}
    LIMIT 100
    """
    result = []
    for item in get_all(query):
        result.append({
            'title': item['title'],
            'result_year': item['release_year'],
        })
    return result

@app.get('/movie/rating/<value>')                 # работает       # http://127.0.0.1:5000/movie/rating/family
def get_movie_by_rating(value:str):
    query = """
    SELECT *
    FROM netflix"""

    if value == 'children':
        query += ' WHERE rating = "G"'
    elif value == 'family':
        query += ' WHERE rating="G" OR rating="PG" OR rating="PG=13"'
    elif value == 'adult':
        query += ' WHERE rating="R" OR rating="NC=17"'
    else:
        return jsonify(status=400)

    result = []
    for item in get_all(query):
        result.append({
            'title': item['title'],
            'rating': item['rating'],
            'description': item['description'],
        })

    return jsonify(result)

@app.get('/genre/<genre>')                  # не работает    # http://127.0.0.1:5000/gerne/comedies
def get_movie_by_genre(genre: str):
    query = f"""
    SELECT * 
    FROM netflix
    WHERE listed_in LIKE '%{genre}%'
    ORDER BY date_added DESC 
    LIMIT 10
    """

    result = []
    for item in get_all(query):
        result.append({
            'title': item['title'],
            'description': item['description'],
            })
    return jsonify(result)

app.run()