import unittest
import requests
import os
import sys

fpath = os.path.join(os.path.dirname(__file__), 'controllers')
sys.path.append(fpath)
fpath = os.path.join(os.path.dirname(__file__), 'models')
sys.path.append(fpath)
yahtzee_db_name=f"{os.getcwd()}/models/yahtzeeDB.db"
print("test_UsersController DB location:", yahtzee_db_name)

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

class TestUserController(unittest.TestCase):
    def setUp(self):
        User.initialize_users_table()
        Game.initialize_games_table()
        Scorecard.initialize_scorecards_table()
    '''
    def test_GET_users_no_users(self):
        """1.1) UsersController: GET /users with no users"""
        response = requests.get("http://127.0.0.1:5000/users")
        self.assertEqual(response.json(), [], "GET request for all users before DB is seeded should return []")
    
    def test_POST_users(self):
        """1.2) UsersController: POST /users returns posted user"""
        response = requests.post("http://127.0.0.1:5000/users", json=user1)
        self.assertEqual(response.json()["username"], user1["username"], "username of returned user should match POSTed user")
        self.assertEqual(response.json()["email"], user1["email"], "email of returned user should match POSTed user")
        self.assertEqual(response.json()["password"], user1["password"], "password of returned user should match POSTed user")

    def test__GET_users_one_user(self):
        """1.3) UsersController: GET /users with one user"""
        # create 1 user
        requests.post("http://127.0.0.1:5000/users", json=user2)
       
        # ask for all users
        response = requests.get("http://127.0.0.1:5000/users")

        self.assertEqual(len(response.json()), 1, "length of returned list should be 1")
        self.assertEqual(response.json()[0]["username"], user2["username"], "username of returned user should match POSTed user")
        self.assertEqual(response.json()[0]["email"], user2["email"], "email of returned user should match POSTed user")
        self.assertEqual(response.json()[0]["password"], user2["password"], "password of returned user should match POSTed user")

    def test__GET_users_many_users(self):
        """1.4) UsersController: GET /users with many users"""
        # create 4 users
        requests.post("http://127.0.0.1:5000/users", json=user1)
        requests.post("http://127.0.0.1:5000/users", json=user2)
        requests.post("http://127.0.0.1:5000/users", json=user3)
        requests.post("http://127.0.0.1:5000/users", json=user4)
        
        # ask for all users
        response = requests.get("http://127.0.0.1:5000/users")
        all_users = sorted(response.json(), key=lambda user: user["username"])

        self.assertEqual(len(response.json()), 4, "length of returned list should be 4")
        self.assertEqual(all_users[0]["username"], user1["username"], "username of returned user should match POSTed user")
        self.assertEqual(all_users[0]["email"], user1["email"], "email of returned user should match POSTed user")
        self.assertEqual(all_users[0]["password"], user1["password"], "password of returned user should match POSTed user")
        self.assertEqual(all_users[1]["username"], user2["username"], "username of returned user should match POSTed user")
        self.assertEqual(all_users[1]["email"], user2["email"], "email of returned user should match POSTed user")
        self.assertEqual(all_users[1]["password"], user2["password"], "password of returned user should match POSTed user")
        self.assertEqual(all_users[2]["username"], user3["username"], "username of returned user should match POSTed user")
        self.assertEqual(all_users[2]["email"], user3["email"], "email of returned user should match POSTed user")
        self.assertEqual(all_users[2]["password"], user3["password"], "password of returned user should match POSTed user")
        self.assertEqual(all_users[3]["username"], user4["username"], "username of returned user should match POSTed user")
        self.assertEqual(all_users[3]["email"], user4["email"], "email of returned user should match POSTed user")
        self.assertEqual(all_users[3]["password"], user4["password"], "password of returned user should match POSTed user")
    def test_GET_user_by_username_exists(self):
        """1.5) UsersController: GET /users/<user_name> w/ user that exists"""
        # create 4 users
        requests.post("http://127.0.0.1:5000/users", json=user1)
        requests.post("http://127.0.0.1:5000/users", json=user2)
        requests.post("http://127.0.0.1:5000/users", json=user3)
        requests.post("http://127.0.0.1:5000/users", json=user4)
        
        # ask for princessOfficial
        response = requests.get("http://127.0.0.1:5000/users/princessOfficial")

        self.assertEqual(response.json()["username"], user3["username"], "username of returned user should match POSTed user")
        self.assertEqual(response.json()["email"], user3["email"], "email of returned user should match POSTed user")
        self.assertEqual(response.json()["password"], user3["password"], "password of returned user should match POSTed user")

    def test_GET_user_by_username_DNE(self):
        """1.6) UsersController: GET /users/<user_name> w/ user that doesn't exist"""
        # create 4 users
        requests.post("http://127.0.0.1:5000/users", json=user1)
        requests.post("http://127.0.0.1:5000/users", json=user2)
        requests.post("http://127.0.0.1:5000/users", json=user3)
        requests.post("http://127.0.0.1:5000/users", json=user4)
        
        # ask for bowserOfficial
        response = requests.get("http://127.0.0.1:5000/users/bowserOfficial")

        self.assertEqual(response.json(), {}, "GETing a user that DNE exist should return {}")

    def test_PUT_user_by_username_exists(self):
        """1.7) UsersController: PUT /users/<user_name> w/ user that exists"""
         # create 4 users
        requests.post("http://127.0.0.1:5000/users", json=user1)
        requests.post("http://127.0.0.1:5000/users", json=user2)
        requests.post("http://127.0.0.1:5000/users", json=user3)
        requests.post("http://127.0.0.1:5000/users", json=user4)
        
        response = requests.get("http://127.0.0.1:5000/users/princessOfficial")
        
        new_user3_info ={
            "id": response.json()["id"],
            "email":"princeZZZZZ@trinityschoolnyc.org",
            "username":"princeZZZOfficial1",
            "password":"123TriniTea"
        }

        # ask to update pricessOfficial info
        response = requests.put("http://127.0.0.1:5000/users/princessOfficial", json=new_user3_info)

        self.assertEqual(response.json()["username"], new_user3_info["username"], "username of returned user should match POSTed user")
        self.assertEqual(response.json()["email"], new_user3_info["email"], "email of returned user should match POSTed user")
        self.assertEqual(response.json()["password"], new_user3_info["password"], "password of returned user should match POSTed user")
   

    def test_PUT_user_by_username_DNE(self):
        """1.8) UsersController: PUT /users/<user_name> w/ user that doesn't exist"""
        # create 4 users
        requests.post("http://127.0.0.1:5000/users", json=user1)
        requests.post("http://127.0.0.1:5000/users", json=user2)
        requests.post("http://127.0.0.1:5000/users", json=user3)
        requests.post("http://127.0.0.1:5000/users", json=user4)
                
        new_user3_info ={
            "id": 12345,
            "email":"bowZZZZZer@trinityschoolnyc.org",
            "username":"bowZZZerOfficial1",
            "password":"123TriniTea"
        }

        # ask to update bowserOfficial info
        response = requests.put("http://127.0.0.1:5000/users/bowserOfficial", json=new_user3_info)

        self.assertEqual(response.json(), {}, "Updating a user that DNE should return {}")
 
'''
    def test_DELETE_user_by_username_exists(self):
        """1.9) UsersController: DELETE /users/<user_name> w/ user that exists"""
          # create 4 users
        requests.post("http://127.0.0.1:5000/users", json=user1)
        requests.post("http://127.0.0.1:5000/users", json=user2)
        requests.post("http://127.0.0.1:5000/users", json=user3)
        requests.post("http://127.0.0.1:5000/users", json=user4)
        
        response = requests.get("http://127.0.0.1:5000/users")
        original_list_of_users = response.json()
        self.assertEqual(len(response.json()), 4, "4 users should initially be in DB")

        # ask to delete pricessOfficial info
        response = requests.delete("http://127.0.0.1:5000/users/princessOfficial")

        self.assertEqual(response.json()["username"], user3["username"], "username of returned user should match DELETEd user")
        self.assertEqual(response.json()["email"], user3["email"], "email of returned user should match DELETEd user")
        self.assertEqual(response.json()["password"], user3["password"], "password of returned user should match DELETEd user")
        
        response = requests.get("http://127.0.0.1:5000/users")
        self.assertEqual(len(response.json()), 3, "3 users should be in DB after the delete")
        for user in response.json():
            self.assertNotEqual(user["username"], "princessOfficial", "3 users should be in DB after the delete")
'''  
    def test_DELETE_user_by_username_DNE(self):
        """1.10) UsersController: DELETE /users/<user_name> w/ user that doesn't exist"""
        # create 4 users
        requests.post("http://127.0.0.1:5000/users", json=user1)
        requests.post("http://127.0.0.1:5000/users", json=user2)
        requests.post("http://127.0.0.1:5000/users", json=user3)
        requests.post("http://127.0.0.1:5000/users", json=user4)
                
        # ask to update bowserOfficial info
        response = requests.delete("http://127.0.0.1:5000/users/bowserOfficial")

        self.assertEqual(response.json(), {}, "DELETEing a user that DNE should return {}")
    
    def test_GET_games_user_exists_0_games(self):
        """1.11) UsersController: GET /users/games/:user_name w/ user that exists and no games"""
        # create 4 users
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        user4_info = requests.post("http://127.0.0.1:5000/users", json=user4).json()

        game1_info=Game.create_game(game1)["message"]
        game2_info=Game.create_game(game2)["message"]
        game3_info=Game.create_game(game3)["message"]
        game4_info=Game.create_game(game4)["message"]

        Scorecard.create_scorecard(game1_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game1_info["id"],user2_info["id"], 2)

        Scorecard.create_scorecard(game2_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game2_info["id"],user2_info["id"], 2)

        Scorecard.create_scorecard(game3_info["id"],user2_info["id"], 1)
        Scorecard.create_scorecard(game3_info["id"],user3_info["id"], 2)

        Scorecard.create_scorecard(game4_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game4_info["id"],user3_info["id"], 2)

        response = requests.get(f"http://127.0.0.1:5000/users/games/{user4_info['username']}")

        self.assertEqual(response.json(), [], "GETing games for a user with no games return []")

   

    def test_GET_games_user_exists_1_games(self):
        """1.12) UsersController: GET /users/games/:user_name w/ user that exists and 1 game"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        user4_info = requests.post("http://127.0.0.1:5000/users", json=user4).json()

        game1_info=Game.create_game(game1)["message"]
        game2_info=Game.create_game(game2)["message"]
        game3_info=Game.create_game(game3)["message"]
        game4_info=Game.create_game(game4)["message"]

        Scorecard.create_scorecard(game1_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game1_info["id"],user2_info["id"], 2)

        Scorecard.create_scorecard(game2_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game2_info["id"],user2_info["id"], 2)

        Scorecard.create_scorecard(game3_info["id"],user2_info["id"], 1)
        Scorecard.create_scorecard(game3_info["id"],user3_info["id"], 2)

        Scorecard.create_scorecard(game4_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game4_info["id"],user3_info["id"], 2)
        Scorecard.create_scorecard(game4_info["id"],user4_info["id"], 3)

        response = requests.get(f"http://127.0.0.1:5000/users/games/{user4_info['username']}")
    
        self.assertEqual(len(response.json()), 1, "GETing games for a user with 1 game should return a list of length 1")
        self.assertEqual(response.json()[0]["id"], game4_info["id"], "GETing games for a user with 1 game should return the id of the correct game")

    
    def test_GET_games_user_exists_many_games(self):
        """1.13) UsersController: GET /users/games/:user_name w/ user that exists and many games"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        user4_info = requests.post("http://127.0.0.1:5000/users", json=user4).json()

        game1_info=Game.create_game(game1)["message"]
        game2_info=Game.create_game(game2)["message"]
        game3_info=Game.create_game(game3)["message"]
        game4_info=Game.create_game(game4)["message"]

        Scorecard.create_scorecard(game1_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game1_info["id"],user2_info["id"], 2)

        Scorecard.create_scorecard(game2_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game2_info["id"],user2_info["id"], 2)

        Scorecard.create_scorecard(game3_info["id"],user2_info["id"], 1)
        Scorecard.create_scorecard(game3_info["id"],user3_info["id"], 2)

        Scorecard.create_scorecard(game4_info["id"],user1_info["id"], 1)
        Scorecard.create_scorecard(game4_info["id"],user3_info["id"], 2)
        Scorecard.create_scorecard(game4_info["id"],user4_info["id"], 3)

        response = requests.get(f"http://127.0.0.1:5000/users/games/{user1_info['username']}")
        returned_games = sorted(response.json(), key = lambda game: game["name"])
        self.assertEqual(len(response.json()), 3, "GETing games for a user with 3 games should return a list of length 3")
        self.assertEqual(returned_games[0]["name"], game1_info["name"], "GETing games for a user with 1 game should return the id of the correct game")
        self.assertEqual(returned_games[1]["name"], game2_info["name"], "GETing games for a user with 1 game should return the id of the correct game")
        self.assertEqual(returned_games[2]["name"], game4_info["name"], "GETing games for a user with 1 game should return the id of the correct game")

    def test_GET_games_user_DNE(self):
        """1.14) UsersController: GET /users/games/:user_name w/ user that doesn't exist"""
         # create 4 users
        requests.post("http://127.0.0.1:5000/users", json=user1)
        requests.post("http://127.0.0.1:5000/users", json=user2)
        requests.post("http://127.0.0.1:5000/users", json=user3)
        requests.post("http://127.0.0.1:5000/users", json=user4)

        response = requests.get("http://127.0.0.1:5000/users/games/bowserOfficial")

        self.assertEqual(response.json(), [], "GETing games for a user that DNE exist should return []")
'''

if __name__ == "__main__":
      unittest.main()