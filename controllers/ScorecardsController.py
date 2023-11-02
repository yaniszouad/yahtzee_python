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

def ten_score_objects():
    gamesList = games.get_games()["message"]
    singleScore = []
    for game in gamesList:
        result = scorecards.get_game_scorecards(game["id"])
        for scorecard in result["message"]:
            singleScore.append(scorecard["score"])

    singleScore = sorted(singleScore)
    singleScore = reversed(singleScore)
    scores = []
    for score in singleScore:
        result = scorecards.get_scorecards()
        for scorecard in result["message"]:
            game = games.get_game(id =scorecard["game_id"])["message"]
            game_name = game["name"]
            if score == scorecard["score"]:
                username = users.get_user(id = scorecard["user_id"])["message"]["username"]
                scores.append({"score": scorecard["score"],
                               "game_name":game_name, 
                               "username": username})
    
    newScores = scores

    if len(scores) > 10:
        print("ITSS TOOOOOOO MUCHHHHHH")
        newScores = []
        for i in range(10):
            newScores.append(scores[i])

    ionevenknow = list(reversed(newScores))
    for score in ionevenknow:
        if ionevenknow.count(score) > 1:
            ionevenknow.remove(score)

    return list(reversed(ionevenknow))

def all_scorecards(user_name):
    user = users.get_user(username=user_name)["message"]
    user_id = user["id"]
    scorecards_list = scorecards.get_scorecards()["message"]
   
    user_scorecards = [sc for sc in scorecards_list if sc["user_id"] == user_id]
   
    sorted_scorecards = sorted(user_scorecards, key=lambda sc: sc["score"], reverse=True)
   
    game_names = {}

    scores = []
    for scorecard in sorted_scorecards:
        if scorecard["game_id"] not in game_names:
            game = games.get_game(id=scorecard["game_id"])["message"]
            game_names[scorecard["game_id"]] = game["name"]
       
        score_info = {
            "score": scorecard["score"],
            "game_name": game_names[scorecard["game_id"]]
        }
       
        if score_info not in scores:
            scores.append(score_info)

    print("Scores", scores)
    return scores

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
            scorecard_object = scorecards.create_scorecard(data["game_id"], data["user_id"], data["turn_order"])
            return jsonify(scorecard_object["message"])
        else:
            return {}
    else:
        return {"error:" "Invalid request"}

def update_delete_return_one_scorecard(scorecard_name):
    #Getting information via the path portion of a URL
    if request.method == "GET":
        scorecard = scorecards.get_scorecard(scorecard_name)
        if scorecard["message"] == "Scorecard doesnt exist in get scorecard":
            print("scorecard no exist")
            return {}
        return jsonify(scorecard["message"])
    
    elif request.method == "PUT":
        data = request.json
        scorecard = scorecards.get_scorecard(scorecard_name)["message"]
        if scorecard == "Scorecard doesnt exist in get scorecard":
            return {}
        scorecard_object = scorecards.update_scorecard(scorecard["id"],data)
        if scorecard_object["message"] == "Scorecard doesnt exist in get scorecard":
            return {}
        return jsonify(scorecard_object["message"])

    elif request.method == "DELETE":
        
        scorecard = scorecards.get_scorecard(scorecard_name)["message"]
        if scorecard == "Scorecard doesnt exist in get scorecard":
            return {}
        oldScorecard = scorecards.get_scorecard(scorecard_name)["message"]
        scorecard_object = scorecards.remove_scorecard(scorecard_name)
        return jsonify(oldScorecard)
    else:
        return {"error:" "Invalid request"}
            
def info_of_a_game(scorecard_id):
    #Getting information via the path portion of a URL
    scorecard = scorecards.get_scorecard(scorecard_id)["message"]
    if scorecard == "Scorecard doesnt exist in get scorecard":
        print("scorecard no exist")
        return {}
    game_id = scorecard["game_id"]
    print(game_id)
    game = games.get_game(id = game_id)["message"]
    return game
    
    
