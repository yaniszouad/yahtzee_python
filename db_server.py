from flask import Flask
from flask import request

import controllers.GamesController as Games
import controllers.UsersController as Users
import controllers.ScorecardsController as Scorecards

app = Flask(__name__, static_url_path='', static_folder='static')

app.add_url_rule('/games', view_func=Games.all_games_and_create_games , methods = ["POST", "GET"])
app.add_url_rule('/games/<game_name>', view_func=Games.update_delete_return_one_game, methods = ["GET", "PUT", "DELETE"])
app.add_url_rule('/games/scorecards/<game_name>', view_func=Games.scorecards_for_game)

app.add_url_rule('/users', view_func=Users.all_users_and_create_users , methods = ["POST", "GET"])
app.add_url_rule('/users/<user_name>', view_func=Users.update_delete_return_one_user, methods = ["GET", "PUT", "DELETE"])
app.add_url_rule('/users/games/<user_name>', view_func=Users.games_for_user)
"""
app.add_url_rule('/scores', view_func=Scorecards.ten_score_objects , methods = ["POST", "GET"])
app.add_url_rule('/scores/<scorecard_name>', view_func=Scorecards.all_scorecards, methods = ["GET", "PUT", "DELETE"])
app.add_url_rule('/scorecards', view_func=Scorecards.all_scorecards_and_create_scorecard , methods = ["POST", "GET"])
app.add_url_rule('/scorecards/<scorecard_name>', view_func=Scorecards.update_delete_return_one_scorecard, methods = ["GET", "PUT", "DELETE"])
app.add_url_rule('/scorecards/game/<game_name>', view_func=Scorecards.info_of_a_game)"""


app.run(debug=True, port=5000)