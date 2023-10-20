from flask import jsonify
from flask import request
import os
from models.UsersModel import User
from models.ScorecardsModel import Scorecard

yahtzee_db_name=f"{os.getcwd()}/models/yahtzeeDB.db"
table_name = "users"

users = User(yahtzee_db_name)


def all_users_and_create_users():
    #Getting information via the query string portion of a URL
    # curl "http://127.0.0.1:5000/fruit/"
    # curl "http://127.0.0.1:5000/fruit?index=0"

    print(f"request.url={request.url}")
    print(f"request.url={request.query_string}")
    if request.method == "GET":
        game_objects = User.get_games()
        return jsonify(game_objects)
    
    elif request.method == "POST":
        game_object = User.create_game(request.data)
        return jsonify(game_object)
    
    else:
        return {"error:" "Invalid request"}

def update_delete_return_one_user(game_name):
    #Getting information via the path portion of a URL
    print(f"request.url={request.url}")
    print(f"request.url={request.query_string}")
    if request.method == "GET":
        game = User.get_game(game_name)
        return jsonify(game)
    
    elif request.method == "PUT":
        game_object = User.update_game(request.data)
        return jsonify(game_object)

    elif request.method == "DELETE":
        game_object = User.remove_game(request.data)
        return jsonify(game_object)
    else:
        return {"error:" "Invalid request"}
            

def games_for_user(game_name):
    #Getting information via the path portion of a URL
    print(f"request.url={request.url}")
    print(f"request.url={request.query_string}")
    
    game = User.get_game(game_name)
    scorecards = Scorecard.get_game_scorecards["id"]

    return jsonify(scorecards)