from flask import jsonify
from flask import request
import os
from models.GamesModel import Game
from models.ScorecardsModel import Scorecard

yahtzee_db_name=f"{os.getcwd()}/models/yahtzeeDB.db"
table_name = "games"

games = Game(yahtzee_db_name)


def all_games_and_create_games():
    #Getting information via the query string portion of a URL
    # curl "http://127.0.0.1:5000/fruit/"
    # curl "http://127.0.0.1:5000/fruit?index=0"

    print(f"request.url={request.url}")
    print(f"request.url={request.query_string}")
    if request.method == "GET":
        game_objects = Game.get_games()
        return jsonify(game_objects)
    
    elif request.method == "POST":
        game_object = Game.create_game(request.data)
        return jsonify(game_object)
    
    else:
        return {"error:" "Invalid request"}

def update_delete_return_one_game(game_name):
    #Getting information via the path portion of a URL
    print(f"request.url={request.url}")
    print(f"request.url={request.query_string}")
    if request.method == "GET":
        game = Game.get_game(game_name)
        return jsonify(game)
    
    elif request.method == "PUT":
        game_object = Game.update_game(request.data)
        return jsonify(game_object)

    elif request.method == "DELETE":
        game_object = Game.remove_game(request.data)
        return jsonify(game_object)
    else:
        return {"error:" "Invalid request"}
            

def scorecards_for_game(game_name):
    #Getting information via the path portion of a URL
    print(f"request.url={request.url}")
    print(f"request.url={request.query_string}")
    
    game = Game.get_game(game_name)
    scorecards = Scorecard.get_game_scorecards["id"]

    return jsonify(scorecards)