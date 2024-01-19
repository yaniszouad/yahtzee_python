#Yanis Zouad, 11/1/2023, Adv. Topic, Section B


from flask import jsonify
import json
from flask import request
import os
from models.UsersModel import User
from models.ScorecardsModel import Scorecard
from models.GamesModel import Game

yahtzee_db_name=f"{os.getcwd()}/models/yahtzeeDB.db"
users = User(yahtzee_db_name)
games = Game(yahtzee_db_name)
scorecards = Scorecard(yahtzee_db_name)


def all_users_and_create_users():
    #Getting information via the query string portion of a URL
    # curl "http://127.0.0.1:5000/fruit/"
    # curl "http://127.0.0.1:5000/fruit?index=0"
    if request.method == "GET":
        user_objects = users.get_users()
        return user_objects['message']
    
    elif request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
            user_object = users.create_user(data)
            if user_object["result"] == "error":
                return {"result":"error"}
            if "UNIQUE constraint failed" in user_object["message"]:
                return {"error:" "Invalid Username"} # CHECK THIS AGAIN LOOK BACK AT IT !!!!!!
            return jsonify(user_object["message"])
        else:
            return {}
    else:
        return {"error:" "Invalid request"}

def update_delete_return_one_user(user_name):
    #Getting information via the path portion of a URL
    if request.method == "GET":
        user = users.get_user(user_name)
        if user["message"] == "User doesnt exist in get user":
            return {}
        return jsonify(user["message"])
    
    elif request.method == "PUT":
        data = request.json
        user_object = users.update_user(data)
        if user_object["message"] == "User doesn't exist in update":
            return {}
        return jsonify(user_object["message"])

    elif request.method == "DELETE":
        user_object = users.remove_user(user_name)
        if user_object["message"] == "User doesnt exist":
            return {}
        return jsonify(user_object["message"])
    else:
        return {"error:" "Invalid request"}
            
def games_for_user(user_name):
    #Getting information via the path portion of a URL

    if users.get_user(username = user_name)["message"] == "User doesnt exist in get user":
        return []
    user_id = users.get_user(username = user_name)["message"]["id"]
    listScorecards = scorecards.get_scorecards()["message"]
    gamesForUser = []
    for scorecard in listScorecards:
        if user_id == scorecard["user_id"]:
            gameToPlant = games.get_game(id=scorecard["game_id"])["message"]
            gamesForUser.append(gameToPlant)

    return gamesForUser