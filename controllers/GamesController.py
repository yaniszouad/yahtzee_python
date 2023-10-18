from flask import jsonify
from flask import request
import os
from models.GamesModel import Game
from models.ScorecardsModel import Scorecard

yahtzee_db_name=f"{os.getcwd()}/models/yahtzeeDB.db"
table_name = "games"

games = Game(yahtzee_db_name)


def all_game_objects():
    #Getting information via the query string portion of a URL
    # curl "http://127.0.0.1:5000/fruit/"
    # curl "http://127.0.0.1:5000/fruit?index=0"

    print(f"request.url={request.url}")
    print(f"request.url={request.query_string}")
    
    game_objects = Game.get_games()

    return jsonify(game_objects)

def info_of_game(game_name):
    #Getting information via the path portion of a URL
    print(f"request.url={request.url}")
    print(f"request.url={request.query_string}")
    
    game = Game.get_game(game_name)

    return jsonify(game)
            

def scorecards_for_game(game_name):
    #Getting information via the path portion of a URL
    print(f"request.url={request.url}")
    print(f"request.url={request.query_string}")
    
    game = Game.get_game(game_name)
    scorecards = Scorecard.get_game_scorecards["id"]

    return jsonify(scorecards)