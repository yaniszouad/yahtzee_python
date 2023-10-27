import unittest
import requests
import os
import sys

fpath = os.path.join(os.path.dirname(__file__), 'controllers')
sys.path.append(fpath)
fpath = os.path.join(os.path.dirname(__file__), 'models')
sys.path.append(fpath)
yahtzee_db_name=f"{os.getcwd()}/models/yahtzeeDB.db"
print("test_GamesController DB location:", yahtzee_db_name)

import UsersModel, GamesModel, ScorecardsModel
User = UsersModel.User(yahtzee_db_name)
Game = GamesModel.Game(yahtzee_db_name)
Scorecard = ScorecardsModel.Scorecard(yahtzee_db_name)

user1 ={
    "email":"luigi@trinityschoolnyc.org",
    "username":"luigiOfficial",
    "password":"123TriniT"
}
user2 ={
    "email":"mario@trinityschoolnyc.org",
    "username":"marioOfficial",
    "password":"123TriniT"
}
user3 ={
    "email":"princess@trinityschoolnyc.org",
    "username":"princessOfficial",
    "password":"123TriniT"
}
user4 ={
    "email":"toad@trinityschoolnyc.org",
    "username":"toadOfficial",
    "password":"123TriniT"
}
game1={
    "name":"game1",
    "link":"link1"
}
game2={
    "name":"game2",
    "link":"link2"
}
game3={
    "name":"game3",
    "link":"link3"
}
game4={
    "name":"game4",
    "link":"link4"
}
game5={
    "name":"game5",
    "link":"link5"
}

class TestGameController(unittest.TestCase):
    def setUp(self):
        User.initialize_users_table()
        Game.initialize_games_table()
        Scorecard.initialize_scorecards_table()

    def test_GET_games_no_games(self):
        """2.1) GamesController: GET /games with no games"""
        response = requests.get("http://127.0.0.1:5000/games")
        self.assertEqual(response.json(), [], "GET request for all games before DB is seeded should return []")
    
    def test_POST_games(self):
        """2.2) GamesController: POST /games returns posted game"""
        response = requests.post("http://127.0.0.1:5000/games", json=game1)
        self.assertEqual(response.json()["name"], game1["name"], "name of returned user should match POSTed game")
        self.assertEqual(response.json()["link"], game1["link"], "link of returned user should match POSTed game")
        self.assertIn("id", response.json(), "id of returned game should match POSTed game")
        self.assertIn("created", response.json(), "created of returned game should match POSTed game")
        self.assertIn("finished", response.json(), "finished of returned game should match POSTed game")
    
    def test__GET_games_one_game(self):
        """2.3) GamesController: GET /games with one game"""
        # create 1 game
        requests.post("http://127.0.0.1:5000/games", json=game2)
       
        # ask for all games
        response = requests.get("http://127.0.0.1:5000/games")

        self.assertEqual(len(response.json()), 1, "length of returned list should be 1")
        self.assertEqual(response.json()[0]["name"], game2["name"], "name of returned user should match POSTed game")
        self.assertEqual(response.json()[0]["link"], game2["link"], "link of returned user should match POSTed game")
        self.assertIn("id", response.json()[0], "id of returned game should match POSTed game")
        self.assertIn("created", response.json()[0], "created of returned game should match POSTed game")
        self.assertIn("finished", response.json()[0], "finished of returned game should match POSTed game")

    def test__GET_games_many_games(self):
        """2.4) GamesController: GET /games with many game"""
        # create 4 games
        requests.post("http://127.0.0.1:5000/games", json=game1)
        requests.post("http://127.0.0.1:5000/games", json=game2)
        requests.post("http://127.0.0.1:5000/games", json=game3)
        requests.post("http://127.0.0.1:5000/games", json=game4)
        
        # ask for all games
        response = requests.get("http://127.0.0.1:5000/games")
        all_games = sorted(response.json(), key=lambda game: game["name"])

        self.assertEqual(len(response.json()), 4, "length of returned list should be 4")
        self.assertEqual(all_games[0]["name"], game1["name"], "name of returned user should match POSTed game")
        self.assertEqual(all_games[0]["link"], game1["link"], "link of returned user should match POSTed game")
        self.assertIn("id", all_games[0], "id of returned game should match POSTed game")
        self.assertIn("created", all_games[0], "created of returned game should match POSTed game")
        self.assertIn("finished", all_games[0], "finished of returned game should match POSTed game")
        self.assertEqual(all_games[1]["name"], game2["name"], "name of returned user should match POSTed game")
        self.assertEqual(all_games[1]["link"], game2["link"], "link of returned user should match POSTed game")
        self.assertIn("id", all_games[1], "id of returned game should match POSTed game")
        self.assertIn("created", all_games[1], "created of returned game should match POSTed game")
        self.assertIn("finished", all_games[1], "finished of returned game should match POSTed game")
        self.assertEqual(all_games[2]["name"], game3["name"], "name of returned user should match POSTed game")
        self.assertEqual(all_games[2]["link"], game3["link"], "link of returned user should match POSTed game")
        self.assertIn("id", all_games[2], "id of returned game should match POSTed game")
        self.assertIn("created", all_games[2], "created of returned game should match POSTed game")
        self.assertIn("finished", all_games[2], "finished of returned game should match POSTed game")
        self.assertEqual(all_games[3]["name"], game4["name"], "name of returned user should match POSTed game")
        self.assertEqual(all_games[3]["link"], game4["link"], "link of returned user should match POSTed game")
        self.assertIn("id", all_games[3], "id of returned game should match POSTed game")
        self.assertIn("created", all_games[3], "created of returned game should match POSTed game")
        self.assertIn("finished", all_games[3], "finished of returned game should match POSTed game")
    def test_GET_game_by_name_exists(self):
        """2.5) GamesController: GET /games/<game_name> w/ game that exists"""
        # create 4 games
        requests.post("http://127.0.0.1:5000/games", json=game1)
        requests.post("http://127.0.0.1:5000/games", json=game2)
        requests.post("http://127.0.0.1:5000/games", json=game3)
        response = requests.post("http://127.0.0.1:5000/games", json=game4)
        posted_game = response.json()

        # ask for game4
        response = requests.get("http://127.0.0.1:5000/games/game4")
        returned_game = response.json()

        self.assertEqual(returned_game["id"], posted_game["id"], "id of returned game should match POSTed game")
        self.assertEqual(returned_game["name"], posted_game["name"], "name of returned game should match POSTed game")
        self.assertEqual(returned_game["link"], posted_game["link"], "link of returned game should match POSTed game")
        self.assertEqual(returned_game["finished"], posted_game["finished"], "finished of returned game should match POSTed game")
        self.assertEqual(returned_game["created"], posted_game["created"], "created of returned game should match POSTed game")
    
    def test_GET_game_by_name_DNE(self):
        """2.6) GamesController: GET /games/<game_name> w/ game that doesn't exist"""
        # create 4 games
        requests.post("http://127.0.0.1:5000/games", json=game1)
        requests.post("http://127.0.0.1:5000/games", json=game2)
        requests.post("http://127.0.0.1:5000/games", json=game3)
        requests.post("http://127.0.0.1:5000/games", json=game4)
        
        # ask for bowserGame
        response = requests.get("http://127.0.0.1:5000/games/bowserGame")

        self.assertEqual(response.json(), {}, "GETing a user that DNE exist should return {}")
  
    def test_PUT_game_by_name_exists(self):
        """2.7) GamesController: PUT /games/<game_name> w/ game that exists"""
        # create 4 games
        requests.post("http://127.0.0.1:5000/games", json=game1)
        requests.post("http://127.0.0.1:5000/games", json=game2)
        requests.post("http://127.0.0.1:5000/games", json=game3)
        requests.post("http://127.0.0.1:5000/games", json=game4)
        
        response = requests.get("http://127.0.0.1:5000/games/game3")
        original_game = response.json()

        new_game3_info ={
            "id": original_game["id"],
            "name": "GAME3333333333",
            "link": "GAME3333333333"
        }

        # ask to update game3 info
        response = requests.put("http://127.0.0.1:5000/games/game3", json=new_game3_info)
        updated_game = response.json()

        self.assertEqual(updated_game["id"], original_game["id"], "id of returned game should match originally POSTed game")
        self.assertEqual(updated_game["name"], new_game3_info["name"], "name of returned game should match new game info")
        self.assertEqual(updated_game["link"], new_game3_info["link"], "link of returned game should match new game info")
        self.assertEqual(updated_game["finished"], original_game["finished"], "finished of returned game should match originally POSTed game")
        self.assertEqual(updated_game["created"], original_game["created"], "created of returned game should match originally POSTed game")
         
    def test_PUT_game_by_gamename_DNE(self):
        """2.8) GamesController: PUT /games/<game_name> w/ game that doesn't exist"""
        # create 4 games
        requests.post("http://127.0.0.1:5000/games", json=game1)
        requests.post("http://127.0.0.1:5000/games", json=game2)
        requests.post("http://127.0.0.1:5000/games", json=game3)
        requests.post("http://127.0.0.1:5000/games", json=game4)
                
        new_game3_info ={
            "id": 12345,
            "name":"bowZZZZZerZGame",
            "link":"bowZZZZZerZGame"
        }

        # ask to update bowsersGame info
        response = requests.put("http://127.0.0.1:5000/games/bowsersGame", json=new_game3_info)

        self.assertEqual(response.json(), {}, "Updating a game that DNE should return {}")
 
  
    def test_DELETE_game_by_gamename_exists(self):
        """2.9) GamesController: DELETE /games/<game_name> w/ user that exists"""
        # create 4 games
        requests.post("http://127.0.0.1:5000/games", json=game1)
        response = requests.post("http://127.0.0.1:5000/games", json=game2)
        original_game = response.json()
        requests.post("http://127.0.0.1:5000/games", json=game3)
        requests.post("http://127.0.0.1:5000/games", json=game4)

        response = requests.get("http://127.0.0.1:5000/games")
        original_list_of_games = response.json()
        self.assertEqual(len(original_list_of_games), 4, "4 games should initially be in DB")

        # ask to delete game2 info
        response = requests.delete("http://127.0.0.1:5000/games/game2")
        deleted_game = response.json()
        self.assertEqual(deleted_game["name"], game2["name"], "name of returned game should match DELETEd game")
        self.assertEqual(deleted_game["link"], game2["link"], "link of returned game should match DELETEd game")
        self.assertEqual(deleted_game["id"], original_game["id"], "id of returned game should match originally POSTed game")
        self.assertEqual(deleted_game["finished"], original_game["finished"], "finished of returned game should match originally POSTed game")
        self.assertEqual(deleted_game["created"], original_game["created"], "created of returned game should match originally POSTed game")
        
        response = requests.get("http://127.0.0.1:5000/games")
        self.assertEqual(len(response.json()), 3, "3 games should be in DB after the delete")
        for game in response.json():
            self.assertNotEqual(game["name"], "game2", "game2 should not be in DB after the delete")

    def test_DELETE_game_by_gamename_DNE(self):
        """2.10) GamesController: DELETE /games/<game_name> w/ user that doesn't exist"""
        # create 4 games
        requests.post("http://127.0.0.1:5000/games", json=game1)
        requests.post("http://127.0.0.1:5000/games", json=game2)
        requests.post("http://127.0.0.1:5000/games", json=game3)
        requests.post("http://127.0.0.1:5000/games", json=game4)
                
        # ask to update bowsersGame info
        response = requests.delete("http://127.0.0.1:5000/games/bowsersGame")

        self.assertEqual(response.json(), {}, "DELETEing a game that DNE should return {}")
    
    def test_GET_games_scorecards_exists_0_scorecards(self):
        """2.11) GamesController: GET /games/scorecards/<game_name> w/ game that exists and no scorecards"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        user4_info = requests.post("http://127.0.0.1:5000/users", json=user4).json()
 
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        game2_info = requests.post("http://127.0.0.1:5000/games", json=game2).json()
        game3_info = requests.post("http://127.0.0.1:5000/games", json=game3).json()
        game4_info = requests.post("http://127.0.0.1:5000/games", json=game4).json()
        game5_info = requests.post("http://127.0.0.1:5000/games", json=game5).json()

        Scorecard.create_scorecard(game1_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game1_info["id"],user2_info["id"], 2)

        Scorecard.create_scorecard(game2_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game2_info["id"],user2_info["id"], 2)

        Scorecard.create_scorecard(game3_info["id"],user2_info["id"], 1)
        Scorecard.create_scorecard(game3_info["id"],user3_info["id"], 2)

        Scorecard.create_scorecard(game4_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game4_info["id"],user3_info["id"], 2)

        response = requests.get(f"http://127.0.0.1:5000/games/scorecards/{game5_info['name']}")

        self.assertEqual(response.json(), [], "GETing scorecards for a game with no scorecards should return []")

    def test_GET_games_scorecards_exists_1_scorecard(self):
        """2.12) GamesController: GET /games/scorecards/<game_name> w/ game that exists and 1 scorecard"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        user4_info = requests.post("http://127.0.0.1:5000/users", json=user4).json()
        
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        game2_info = requests.post("http://127.0.0.1:5000/games", json=game2).json()
        game3_info = requests.post("http://127.0.0.1:5000/games", json=game3).json()
        game4_info = requests.post("http://127.0.0.1:5000/games", json=game4).json()
        game5_info = requests.post("http://127.0.0.1:5000/games", json=game5).json()

        Scorecard.create_scorecard(game1_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game1_info["id"],user2_info["id"], 2)

        Scorecard.create_scorecard(game2_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game2_info["id"],user2_info["id"], 2)

        Scorecard.create_scorecard(game3_info["id"],user2_info["id"], 1)
        Scorecard.create_scorecard(game3_info["id"],user3_info["id"], 2)

        Scorecard.create_scorecard(game4_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game4_info["id"],user3_info["id"], 2)

        scorecard_info = Scorecard.create_scorecard(game5_info["id"],user3_info["id"], 1)["message"]
        
        game_info = Game.get_game(id=scorecard_info["game_id"])["message"]
        response = requests.get(f"http://127.0.0.1:5000/games/scorecards/{game_info['name']}")
    
        self.assertEqual(len(response.json()), 1, "GETing scorecards for a game with 1 scorecard should return a list of length 1")
        self.assertEqual(response.json()[0]["id"], scorecard_info["id"], "GETing scorecard for a game with 1 scorecard should return the id of the correct scorecard")
        self.assertEqual(response.json()[0]["game_id"], scorecard_info["game_id"], "GETing scorecard for a game with 1 scorecard should return the game_id of the correct game")
        self.assertEqual(response.json()[0]["user_id"], scorecard_info["user_id"], "GETing scorecard for a game with 1 scorecard should return the user_id of the correct user")
    def test_GET_games_scorecards_exists_many_scorecards(self):
        """2.13) GamesController: GET /games/scorecards/<game_name> w/ game that exists and many scorecards"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        user4_info = requests.post("http://127.0.0.1:5000/users", json=user4).json()
        
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        game2_info = requests.post("http://127.0.0.1:5000/games", json=game2).json()
        game3_info = requests.post("http://127.0.0.1:5000/games", json=game3).json()
        game4_info = requests.post("http://127.0.0.1:5000/games", json=game4).json()
        game5_info = requests.post("http://127.0.0.1:5000/games", json=game5).json()

        Scorecard.create_scorecard(game1_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game1_info["id"],user2_info["id"], 2)

        Scorecard.create_scorecard(game2_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game2_info["id"],user2_info["id"], 2)

        scorecard_info_1 = Scorecard.create_scorecard(game3_info["id"],user2_info["id"], 1)["message"]
        scorecard_info_2 = Scorecard.create_scorecard(game3_info["id"],user3_info["id"], 2)["message"]
        scorecard_info_3 = Scorecard.create_scorecard(game3_info["id"],user4_info["id"], 3)["message"]

        Scorecard.create_scorecard(game4_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game4_info["id"],user3_info["id"], 2)

        game_info = Game.get_game(id=scorecard_info_1["game_id"])["message"]
        response = requests.get(f"http://127.0.0.1:5000/games/scorecards/{game_info['name']}")

        self.assertEqual(len(response.json()), 3, "GETing games for a game with 3 scorecards should return a list of length 3")
        # check to see all 3 scorecard id's are in the list of dictionaries
        returned_scorecard_ids=[]
        for scorecard in response.json():
            returned_scorecard_ids.append(scorecard["id"])
        
        self.assertIn(scorecard_info_1["id"], returned_scorecard_ids, "GETing scorecards for a game with 3 scorecards should return all ids of the correct scorecards")
        self.assertIn(scorecard_info_2["id"], returned_scorecard_ids,  "GETing scorecards for a game with 3 scorecards should return all ids of the correct scorecards")
        self.assertIn(scorecard_info_3["id"], returned_scorecard_ids,  "GETing scorecards for a game with 3 scorecards should return all ids of the correct scorecards")
   
    def test_GET_games_scorecard_DNE(self):
        """2.14) GamesController: GET /games/scorecards/<game_name> w/ game that DNE exists"""
         # create 4 game
        requests.post("http://127.0.0.1:5000/games", json=game1)
        requests.post("http://127.0.0.1:5000/games", json=game2)
        requests.post("http://127.0.0.1:5000/games", json=game3)
        requests.post("http://127.0.0.1:5000/games", json=game4)

        response = requests.get("http://127.0.0.1:5000/games/scorecards/bowserGame")

        self.assertEqual(response.json(), [], "GETing scorecards for a game that DNE exist should return []")
        
if __name__ == "__main__":
      unittest.main()