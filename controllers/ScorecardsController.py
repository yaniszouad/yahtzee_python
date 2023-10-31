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
def bubbleSort(arr):
    n = len(arr)
    # optimize code, so if the array is already sorted, it doesn't need
    # to go through the entire process
    swapped = False
    # Traverse through all array elements
    for i in range(n-1):
        # range(n) also work but outer loop will
        # repeat one time more than needed.
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr["score"][j] > arr["score"][j + 1]:
                swapped = True
                arr["score"][j], arr["score"][j + 1] = arr["score"][j + 1], arr["score"][j]
         
        if not swapped:
            # if we haven't needed to make a single swap, we 
            # can just exit the main loop.
            return
 

def ten_score_objects():
    if request.method == "GET":
        game_objects = games.get_games()
        print(game_objects)
        result = bubbleSort(game_objects["message"])
        print(result)
        return result[0:9]

def all_scorecards(scorecard_name):
    if request.method == "GET":
        game_objects = games.get_games()
        return game_objects['message']

def all_scorecards_and_create_scorecard():
    #Getting information via the query string portion of a URL
    # curl "http://127.0.0.1:5000/fruit/"
    # curl "http://127.0.0.1:5000/fruit?index=0"
    if request.method == "GET":
        scorecard = scorecards.get_scorecards()
        return scorecard['message']
    
    elif request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
            print("look at thisssssssss:",data)
            scorecard_object = scorecards.create_scorecard(data["game_id"], data["user_id"], data["turn_order"])
            print(scorecard_object)
            return jsonify(scorecard_object["message"])
        else:
            return {}
    else:
        return {"error:" "Invalid request"}

def update_delete_return_one_scorecard(game_name):
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
            
def info_of_a_game(game_name):
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