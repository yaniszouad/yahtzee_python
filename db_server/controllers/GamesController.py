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


def all_games_and_create_games():
    #Getting information via the query string portion of a URL
    # curl "http://127.0.0.1:5000/fruit/"
    # curl "http://127.0.0.1:5000/fruit?index=0"
    if request.method == "GET":
        game_objects = games.get_games()
        return game_objects['message']
    
    elif request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
            game_object = games.create_game(data)
            return jsonify(game_object["message"])
        else:
            return {}
    else:
        return {"error:" "Invalid request"}

def update_delete_return_one_game(game_name):
    #Getting information via the path portion of a URL
    if request.method == "GET":
        game = games.get_game(game_name)
        if game["message"] == "game doesnt exist in get game":
            print("game no exist")
            return {}
        return jsonify(game["message"])
    
    elif request.method == "PUT":
        data = request.json
        game_object = games.update_game(data)
        if game_object["message"] == "game doesn't exist in update":
            return {}
        return jsonify(game_object["message"])

    elif request.method == "DELETE":
        game_object = games.remove_game(game_name)
        if game_object["message"] == "Game doesnt exist":
            return {}
        return jsonify(game_object["message"])
    else:
        return {"error:" "Invalid request"}
            
def scorecards_for_game(game_name):
    #Getting information via the path portion of a URL
    if games.get_game(name = game_name)["message"] == "game doesnt exist in get game":
        return []
    game_id = games.get_game(name = game_name)["message"]["id"]
    print(games.get_game(name = game_name)["message"])
    print(game_id)
    if scorecards.get_scorecards()["message"] == []:
        return []
    listScorecards = scorecards.get_scorecards()["message"]
    gamesForUser = []
    for scorecard in listScorecards:
        if game_id == scorecard["game_id"]:
            gamesForUser.append(scorecard)

    return gamesForUser