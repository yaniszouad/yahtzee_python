from flask import jsonify
from flask import request
import os
from models.UsersModel import User
from models.ScorecardsModel import Scorecard
from models.GamesModel import Game

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
        user_objects = users.get_users()
        
        return user_objects['message']
    
    elif request.method == "POST":
        user_object = users.create_user(request.data)
        
        return user_object
    
    else:
        return {"error:" "Invalid request"}

def update_delete_return_one_user(user_name):
    #Getting information via the path portion of a URL
    print(f"request.url={request.url}")
    print(f"request.url={request.query_string}")
    if request.method == "GET":
        user = users.get_user(user_name)
        return jsonify(user)
    
    elif request.method == "PUT":
        user_object = users.update_user(request.data)
        return jsonify(user_object)

    elif request.method == "DELETE":
        user_object = users.remove_user(request.data)
        return jsonify(user_object)
    else:
        return {"error:" "Invalid request"}
            

def games_for_user(user_name):
    #Getting information via the path portion of a URL
    print(f"request.url={request.url}")
    print(f"request.url={request.query_string}")

    all_scorecards = Scorecard.get_scorecards()
    user = users.get_user(user_name)
    games = Game.get_game(user)

    return jsonify(games)