import base64
import base64
import io
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import requests
from flask import Flask, send_file
from flask import session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from json import JSONEncoder
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from Auth.twAuth import twit_auth
from db import cur
from flask_session import Session
from queries.queries import *

app = Flask(__name__)
db = SQLAlchemy()

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgres@{os.environ.get("POSTGRES_HOST")}:5432/{os.environ.get("POSTGRES_DB")}'
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Session(app)


@app.route('/', methods=['GET'])
def hi_there():
    try:
        twich_key = twit_auth()
        token = twich_key['access_token']
        session['twich_key'] = str(token)
        print(twich_key)
        return 'twich_key'
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/popular-engines', methods=['GET'])
def popular_engines():
    obj = {
        'Client-ID': os.environ.get('TWITCH_CLIENT_ID'),
        'Authorization': 'Bearer ' + session['twich_key'],
    }
    data = 'fields name,involved_companies	;'
    response = requests.post("https://api.igdb.com/v4/games", headers=obj, data=data)
    print(response.json())
    return response.json()


@app.route('/multi-query', methods=['GET'])
def popular_games_by_plataform():
    obj = {
        'Client-ID': os.environ.get('TWITCH_CLIENT_ID'),
        'Authorization': 'Bearer ' + session['twich_key'],
    }
    try:

        query = game_by_region + genre_query + plataform
        # data='fields name,involved_companies	;'
        response = requests.post("https://api.igdb.com/v4/multiquery", headers=obj, data=query)
        # app.logger.info(response.json())
        # return response.json()
        games = response.json()[0]['result']
        genres_data = [genres_data['name'] for genres_data in response.json()[1]['result']]
        platforms = [plataformName['name'] for plataformName in response.json()[2]['result']]
        genre_means = []
    except Exception as e:
        return json.dumps({'error': str(e)})

    for i in range(len(games)):
        game_genres = games[i]['genres']
        game_genres_names = [genre['name'] for genre in game_genres]
        games[i]['genres'] = game_genres_names

        game_platforms = games[i]['platforms']
        game_platforms_names = [platform['name'] for platform in game_platforms]
        games[i]['platforms'] = game_platforms_names

    genre_means = {}
    for genre in genres_data:
        # Initialize the genre counts for this genre
        platform_counts = [0] * len(platforms)

        for game in games:
            if genre in game['genres']:
                # Update the platform counts for the current game
                for i, platform in enumerate(platforms):
                    platform_counts[i] += game['platforms'].count(platform)

        # Store the results in the dictionary
        genre_means[genre] = tuple(platform_counts)

        # Debug output
        print(f'Genre: {genre}, Platform Counts: {platform_counts}')

    # df = pd.DataFrame(games)

    x = np.arange(len(platforms))
    fig, ax = plt.subplots()
    width = 0.1  # the width of the bars
    multiplier = 0

    for attribute, measurement in genre_means.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=20)
        multiplier += 1

    ax.set_ylabel('Platforms')
    ax.set_title('Occurrence of platforms by genre')
    ax.set_xticks(x + width, platforms)
    ax.legend(loc='best', ncols=2)

    img = io.BytesIO()

    plt.savefig(img, format='png', dpi=199)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    body = {
        "image": plot_url,
    }
    return f'<img src="data:image/png;base64,{plot_url}">'
    # return response.json()


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)
    data = twit_auth()
