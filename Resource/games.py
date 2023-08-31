from flask import Flask,Blueprint, render_template, abort,jsonify, request
from json import JSONEncoder
from Auth.twAuth import twit_auth
import json
from flask_session import Session
import numpy as np
import os
import pandas as pd
import requests
from flask import session
from queries.queries import *
import matplotlib.pyplot as plt
import io
from flask import Flask, send_file
import base64
import io
import json

# Blueprint Configuration
games_blueprint = Blueprint('games', __name__)

@games_blueprint.route('/', methods=['GET'])
def hi_there():
    try:
        twich_key = twit_auth()
        token = twich_key['access_token']
        session['twich_key'] = str(token)
        print(twich_key)
        return 'twich_key'
    except Exception as e:
        return json.dumps({'error': str(e)})

@games_blueprint.route('/popular-engines', methods=['GET'])
def popular_engines():
    obj = {
        'Client-ID': os.environ.get('TWITCH_CLIENT_ID'),
        'Authorization': 'Bearer ' + session['twich_key'],
    }
    data = 'fields name,involved_companies	;'
    response = requests.post("https://api.igdb.com/v4/games", headers=obj, data=data)
    print(response.json())
    return response.json()

@games_blueprint.route('/genres_by_platform', methods=['GET'])
def popular_games_by_plataform():
    obj = {
        'Client-ID': os.environ.get('TWITCH_CLIENT_ID'),
        'Authorization': 'Bearer ' + session['twich_key'],
    }
    try:
        query = game_by_region + genre_query + plataform
        response = requests.post("https://api.igdb.com/v4/multiquery", headers=obj, data=query)
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
        platform_counts = [0] * len(platforms)

        for game in games:
            if genre in game['genres']:

                for i, platform in enumerate(platforms):
                    platform_counts[i] += game['platforms'].count(platform)

        genre_means[genre] = tuple(platform_counts)

    x = np.arange(len(platforms))
    fig, ax = plt.subplots()
    width = 0.1
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
        'platforms': platforms,
        "image": plot_url,
        "genre_means": genre_means

    }
    return jsonify(body)