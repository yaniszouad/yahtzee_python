import os

import UsersModel, GamesModel, ScorecardsModel

print(os.getcwd())
yahtzee_db_name=f"{os.getcwd()}/yahtzeeDB.db"
print(yahtzee_db_name)
UsersModel.User(yahtzee_db_name).initialize_users_table()
GamesModel.Game(yahtzee_db_name).initialize_games_table()
ScorecardsModel.Scorecard(yahtzee_db_name).initialize_scorecards_table()