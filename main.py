from flask import Flask, jsonify
from utils import get_one, get_all, search_by_cast

app = Flask(__name__)

@app.get('/movie/<title>')
def get_by_title(title:str):
    query = f"""
    SELECT * 
    FROM netflix
    where title = '%{title}%'
    order by date_added decs
    """

    query_result = get_one(query)

    if query_result is None:
        return jsonify(status=404)

    movie = {
        'title': query_result['title'],
        'country': query_result['country'],
        'release_year': query_result['release_year'],
        'genre': query_result['listed_in'],
        'discription': query_result['discription'],
    }
    return jsonify(movie)


@app.get('/movie/<year1>/to/<year2>')
def get_movie_by_year(year1:str,year2:str):
    query = f"""
    SELECT * 
    FROM netflix
    where release_year between {year1} and {year2}
    limit 100
    """
    result = []
    for item in get_all(query):
        result.append({
            'title':item['title'],
            'result_year': item['release_year'],
        })
    return result

@app.get('/movie/rating/<value>')
def get_movie_by_rating(value:str):
    query = """
    SELECT *
    FROM netflix"""

    if value == 'children':
        query += 'where rating = "G"'
    elif value == 'family':
        query += 'where rating="G" or rating="PG" or rating="PG=13"'
    elif value == 'adult':
        query += 'where rating="R" or rating="NC=17"'
    else:
        return jsonify(status=400)

    result = []
    for item in get_all(query):
        result.append({
            'title':item['title'],
            'rating':item['rating'],
            'description':item['description'],
        })

    return jsonify(result)

@app.get('/genre/<genre>')
def get_movie_by_gerne(genre:str):
    query = f"""
    select * 
    from netflix
    where listed_in like '%{gerne}%'
    order by date_added desc 
    limit 10
    """

    result = []
    for item in get_all(query):
        result.append({
            'title':item['title'],
            'description': item['description'],
            })
    return jsonify(result)

app.run()