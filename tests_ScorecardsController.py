import unittest
import requests
import os
import sys

fpath = os.path.join(os.path.dirname(__file__), 'controllers')
sys.path.append(fpath)
fpath = os.path.join(os.path.dirname(__file__), 'models')
sys.path.append(fpath)
yahtzee_db_name=f"{os.getcwd()}/models/yahtzeeDB.db"
print("test_ScorecardsController DB location:", yahtzee_db_name)

import models.UsersModel as Userr
import models.GamesModel as Gamess
import models.ScorecardsModel as Scoress
User = Userr.User(yahtzee_db_name)
Game = Gamess.Game(yahtzee_db_name)
Scorecard = Scoress.Scorecard(yahtzee_db_name)


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
game6={
    "name":"game6",
    "link":"link6"
}
game7={
    "name":"game7",
    "link":"link7"
}
game8={
    "name":"game8",
    "link":"link8"
}
game9={
    "name":"game9",
    "link":"link9"
}
game10={
    "name":"game10",
    "link":"link10"
}
game11={
    "name":"game11",
    "link":"link11"
}
game12={
    "name":"game12",
    "link":"link12"
}
    
def get_blank_scorecard():
    return {
            "dice_rolls":0,
            "upper":{
                "ones":-1,
                "twos":-1,
                "threes":-1,
                "fours":-1,
                "fives":-1,
                "sixes":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }

class TestScorcardController(unittest.TestCase):
    def setUp(self):
        User.initialize_users_table()
        Game.initialize_games_table()
        Scorecard.initialize_scorecards_table()
    '''
    def test_GET_scorecards_no_scorecards(self):
        """3.1) ScorecardsController: GET /scorecards with no scorecards"""
        response = requests.get("http://127.0.0.1:5000/scorecards")
        self.assertEqual(response.json(), [], "GET request for all scorecards before DB is seeded should return []")
    
    def test_POST_scorecard(self):
        """3.2) ScorecardsController: POST /scorecards returns posted scorecard and adds to DB"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        scorecard_1_1={
            "game_id":game1_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        returned_card = requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_1).json()
        self.assertEqual(returned_card["game_id"], scorecard_1_1["game_id"], "game_id of returned scorecard should match POSTed scorecard ")
        self.assertEqual(returned_card["user_id"], scorecard_1_1["user_id"], "user_id of returned scorecard should match POSTed scorecard ")
        self.assertEqual(returned_card["turn_order"], scorecard_1_1["turn_order"], "turn_order of returned scorecard should match POSTed scorecard ")
        self.assertEqual(returned_card["score"], 0, "score of returned scorecard should match POSTed scorecard ")
        self.assertIn("id", returned_card, "id of returned scorecard should should be included ")
        self.assertIn("score_info", returned_card, "score_info of returned scorecard should be included ")

        get_card = requests.get("http://127.0.0.1:5000/scorecards").json()[0]
        self.assertEqual(returned_card["game_id"], get_card["game_id"], "game_id of returned scorecard should match GET scorecard ")
        self.assertEqual(returned_card["user_id"], get_card["user_id"], "user_id of returned scorecard should match GET scorecard ")
        self.assertEqual(returned_card["turn_order"], get_card["turn_order"], "turn_order of returned scorecard should match GET scorecard ")
        self.assertEqual(returned_card["score"], get_card["score"], "score of returned scorecard should match GET scorecard ")
        self.assertEqual(returned_card["id"], get_card["id"], "id of returned scorecard should match GET scorecard ")
        self.assertEqual(returned_card["score_info"], get_card["score_info"], "score_info of returned scorecard should match GET scorecard ")
    
    def test_GET_scorecard_exists(self):
        """3.3) ScorecardsController: GET /scorecards/<scorecard_id> w/ scorecard that exists"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        scorecard_1_1={
            "game_id":game1_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        posted_card = requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_1).json()
        returned_card = requests.get(f'http://127.0.0.1:5000/scorecards/{posted_card["id"]}').json()
       
        self.assertEqual(returned_card["id"], posted_card["id"], "id of returned scorecard should match POSTed scorecard ")
        self.assertEqual(returned_card["game_id"], posted_card["game_id"], "game_id of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_card["user_id"], posted_card["user_id"], "user_id of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_card["turn_order"], posted_card["turn_order"], "turn_order of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_card["score_info"], posted_card["score_info"], "score_info of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_card["score"], posted_card["score"], "score of returned scorecard  should match POSTed scorecard ")
    
    def test_GET_scorecard_exists_many(self):
        """3.4) ScorecardsController: GET /scorecards/<scorecard_id> w/ scorecard that exists"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        game2_info = requests.post("http://127.0.0.1:5000/games", json=game2).json()
        game3_info = requests.post("http://127.0.0.1:5000/games", json=game3).json()

        scorecard_1_1={
            "game_id":game1_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        posted_card1 = requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_1).json()
        scorecard_1_2={
            "game_id":game1_info["id"],
            "user_id":user2_info["id"],
            "turn_order":2
        }
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_2)
        
        scorecard_2_1={
            "game_id":game2_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard_2_2={
            "game_id":game2_info["id"],
            "user_id":user3_info["id"],
            "turn_order":2
        }
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_2_1)
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_2_2)

        scorecard_3_2={
            "game_id":game3_info["id"],
            "user_id":user2_info["id"],
            "turn_order":1
        }
        scorecard_3_3={
            "game_id":game3_info["id"],
            "user_id":user3_info["id"],
            "turn_order":2
        }
        posted_card2=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_3_2).json()
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_3_3)

        returned_game1 = requests.get(f'http://127.0.0.1:5000/scorecards/{posted_card1["id"]}').json()
        returned_game2 = requests.get(f'http://127.0.0.1:5000/scorecards/{posted_card2["id"]}').json()

        self.assertEqual(returned_game1["id"], posted_card1["id"], "id of returned scorecard should match POSTed scorecard ")
        self.assertEqual(returned_game1["game_id"], posted_card1["game_id"], "game_id of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_game1["user_id"], posted_card1["user_id"], "user_id of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_game1["turn_order"], posted_card1["turn_order"], "turn_order of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_game1["score_info"], posted_card1["score_info"], "score_info of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_game1["score"], posted_card1["score"], "score of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_game2["id"], posted_card2["id"], "id of returned scorecard should match POSTed scorecard ")
        self.assertEqual(returned_game2["game_id"], posted_card2["game_id"], "game_id of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_game2["user_id"], posted_card2["user_id"], "user_id of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_game2["turn_order"], posted_card2["turn_order"], "turn_order of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_game2["score_info"], posted_card2["score_info"], "score_info of returned scorecard  should match POSTed scorecard ")
        self.assertEqual(returned_game2["score"], posted_card2["score"], "score of returned scorecard should match POSTed scorecard ")
    
    def test_GET_scorecard_DNE(self):
        """3.5) ScorecardsController: GET /scorecards/<scorecard_id> w/ scorecard that doesn't exist"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        game2_info = requests.post("http://127.0.0.1:5000/games", json=game2).json()
        game3_info = requests.post("http://127.0.0.1:5000/games", json=game3).json()

        scorecard_1_1={
            "game_id":game1_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_1) 
        scorecard_1_2={
            "game_id":game1_info["id"],
            "user_id":user2_info["id"],
            "turn_order":2
        }
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_2)
        
        scorecard_2_1={
            "game_id":game2_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard_2_2={
            "game_id":game2_info["id"],
            "user_id":user3_info["id"],
            "turn_order":2
        }
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_2_1)
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_2_2)

        scorecard_3_2={
            "game_id":game3_info["id"],
            "user_id":user2_info["id"],
            "turn_order":1
        }
        scorecard_3_3={
            "game_id":game3_info["id"],
            "user_id":user3_info["id"],
            "turn_order":2
        }
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_3_2) 
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_3_3)
        
        response = requests.get("http://127.0.0.1:5000/scorecards/-12344534")
        self.assertEqual(response.json(), {}, "GETing a scorecard that DNE exist should return {}")
    
    def test_PUT_scorecard_exists(self):
        """3.6) ScorecardsController: PUT /scorecards/<scorecard_id> w/ scorecard that exists"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        game3_info = requests.post("http://127.0.0.1:5000/games", json=game3).json()

        scorecard_1_1={
            "game_id":game1_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_1) 
        scorecard_1_2={
            "game_id":game1_info["id"],
            "user_id":user2_info["id"],
            "turn_order":2
        }
        original_card=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_2).json()
        
        scorecard_3_2={
            "game_id":game3_info["id"],
            "user_id":user2_info["id"],
            "turn_order":1
        }
        scorecard_3_3={
            "game_id":game3_info["id"],
            "user_id":user3_info["id"],
            "turn_order":2
        }
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_3_2) 
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_3_3)

        new_score_info=get_blank_scorecard()
        new_score_info["lower"]["full_house"]=25
        new_score_info["upper"]["ones"]=2
        updated_card_returned = requests.put(f"http://127.0.0.1:5000/scorecards/{original_card['id']}", json=new_score_info).json()
        updated_card_GET = requests.get(f"http://127.0.0.1:5000/scorecards/{original_card['id']}").json()

        self.assertEqual(original_card["id"], updated_card_returned["id"], "id of original scorecard should match returned scorecard ")
        self.assertEqual(updated_card_GET["id"], updated_card_returned["id"], "id of returned scorecard should match GETed scorecard ")
        self.assertEqual(updated_card_GET["game_id"], updated_card_returned["game_id"], "game_id of returned scorecard  should match GETed scorecard ")
        self.assertEqual(updated_card_GET["user_id"], updated_card_returned["user_id"], "user_id of returned scorecard  should match GETed scorecard ")
        self.assertEqual(updated_card_GET["turn_order"], updated_card_returned["turn_order"], "turn_order of returned scorecard  should match GETed scorecard ")
        self.assertEqual(updated_card_GET["score_info"], updated_card_returned["score_info"], "score_info of returned scorecard  should match GETed scorecard ")
        self.assertEqual(updated_card_GET["score"], updated_card_returned["score"], "score of returned scorecard  should match GETed scorecard ")
        self.assertEqual(updated_card_GET["score_info"], new_score_info, "score_info of GETed scorecard should match the updated score_info")
    
    def test_PUT_scorecard_DNE(self):
        """3.7) ScorecardsController: PUT /scorecards/<scorecard_id> w/ scorecard that doesn't exist"""
        score_info=get_blank_scorecard()
        score_info["lower"]["full_house"]=25
        score_info["upper"]["ones"]=2
        response = requests.put("http://127.0.0.1:5000/scorecards/-123456", json=score_info).json()
        self.assertEqual(response, {}, "PUTing a scorecard that DNE exist should return {}")
    
    def test_DELETE_scorecard_exists(self):
        """3.8) ScorecardsController: DELETE /scorecards/<scorecard_id> w/ scorecard that exists"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        game2_info = requests.post("http://127.0.0.1:5000/games", json=game2).json()

        scorecard_1_1={
            "game_id":game1_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_1) 
        scorecard_1_2={
            "game_id":game1_info["id"],
            "user_id":user2_info["id"],
            "turn_order":2
        }
        card_to_delete=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_2).json()
        
        scorecard_2_1={
            "game_id":game2_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard_2_2={
            "game_id":game2_info["id"],
            "user_id":user3_info["id"],
            "turn_order":2
        }
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_2_1)
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_2_2)

        all_cards_before_delete = requests.get("http://127.0.0.1:5000/scorecards").json()
        deleted_card = requests.delete(f"http://127.0.0.1:5000/scorecards/{card_to_delete['id']}").json()
        all_cards_after_delete = requests.get("http://127.0.0.1:5000/scorecards").json()

        self.assertEqual(len(all_cards_before_delete), 4, "Should be 4 cards before the delete")
        self.assertEqual(len(all_cards_after_delete), 3, "Should be 3 cards before the delete")
        self.assertEqual(deleted_card["id"], card_to_delete["id"], "id of returned scorecard should match DELETEed scorecard ")
        self.assertEqual(deleted_card["game_id"], card_to_delete["game_id"], "game_id of returned scorecard  should match DELETEed scorecard ")
        self.assertEqual(deleted_card["user_id"], card_to_delete["user_id"], "user_id of returned scorecard  should match DELETEed scorecard ")
        self.assertEqual(deleted_card["turn_order"], card_to_delete["turn_order"], "turn_order of returned scorecard  should match DELETEed scorecard ")
        self.assertEqual(deleted_card["score_info"], card_to_delete["score_info"], "score_info of returned scorecard  should match DELETEed scorecard ")
        self.assertEqual(deleted_card["score"], card_to_delete["score"], "score of returned scorecard  should match DELETEed scorecard ")
        for card in all_cards_after_delete:
            self.assertNotIn(deleted_card["id"], card, "The id of the deleted card should not match any cards still in the DB")
    
    def test_DELETE_scorecard_DNE(self):
        """3.9) ScorecardsController: DELETE /scorecards/<scorecard_id> w/ scorecard that doesn't exist"""
        response = requests.delete("http://127.0.0.1:5000/scorecards/-123456").json()
        self.assertEqual(response, {}, "DELETEing a scorecard that DNE exist should return {}")
    
    def test_GET_game_from_scorecard(self):
        """3.10) ScorecardsController: GET /scorecards/game/<scorecard_id> """
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        game2_info = requests.post("http://127.0.0.1:5000/games", json=game2).json()

        scorecard_1_1={
            "game_id":game1_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        card1=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_1).json() 
        scorecard_1_2={
            "game_id":game1_info["id"],
            "user_id":user2_info["id"],
            "turn_order":2
        }
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_2)
        
        scorecard_2_1={
            "game_id":game2_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard_2_2={
            "game_id":game2_info["id"],
            "user_id":user3_info["id"],
            "turn_order":2
        }
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_2_1)
        requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_2_2)

        
        response = requests.get(f"http://127.0.0.1:5000/scorecards/game/{card1['id']}").json()
        self.assertEqual(response["id"], game1_info["id"], "id of returned game should match scorecard")
        self.assertIn("name", response, "returned game should contain a name")
        self.assertIn("name", response, "returned game should contain a name")
        self.assertIn("created", response, "returned game should contain a created")
        self.assertIn("finished", response, "returned game should contain a finished")
    
    def test_GET_game_from_scorecard_DNE(self):
        """3.11) ScorecardsController: GET /scorecards/game/<scorecard_id> w/ scorecard that doesn't exist"""
        response = requests.get("http://127.0.0.1:5000/scorecards/game/-1234567").json()
        self.assertEqual(response, {}, "GETing a game with a scorecard that DNE exist should return {}")
    
    def test_GET_all_scores_none(self):
        """3.12) ScorecardsController: GET /scores w/ no scores"""
        response = requests.get("http://127.0.0.1:5000/scores").json()
        self.assertEqual(response, [], "GETing all scores with no scores should return []")
    def test_GET_all_scores_more_than_10(self):
        """3.13) TODO- ScorecardsController: GET /scores w/ more than 10 scores"""
        self.assertEqual(True, False, "Test not implemented yet")
    '''
    def test_GET_all_scores_fewer_than_10(self):
        """3.14) ScorecardsController: GET /scores w/ fewer than 10 scores scores"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        game2_info = requests.post("http://127.0.0.1:5000/games", json=game2).json()
        game3_info = requests.post("http://127.0.0.1:5000/games", json=game3).json()

        scorecard_1_1={
            "game_id":game1_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard_1_1_info = requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_1).json()
        scorecard_1_2={
            "game_id":game1_info["id"],
            "user_id":user2_info["id"],
            "turn_order":2
        }
        scorecard_1_2_info = requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_1_2).json()
        new_score_info11=get_blank_scorecard()
        new_score_info11["upper"]["ones"]=4
        new_score_info11["upper"]["twos"]=6
        new_score_info11["upper"]["threes"]=9
        updated_1_1 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard_1_1_info['id']}", json=new_score_info11).json()
        new_score_info12=get_blank_scorecard()
        new_score_info12["upper"]["ones"]=2
        new_score_info12["upper"]["twos"]=8
        new_score_info12["upper"]["threes"]=12
        updated_1_2 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard_1_2_info['id']}", json=new_score_info12).json()

        scorecard_2_1={
            "game_id":game2_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard_2_2={
            "game_id":game2_info["id"],
            "user_id":user3_info["id"],
            "turn_order":2
        }
        scorecard_2_1_info = requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_2_1).json()
        scorecard_2_2_info = requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_2_2).json()

        new_score_info21=get_blank_scorecard()
        new_score_info21["lower"]["three_of_a_kind"]=24
        new_score_info21["lower"]["four_of_a_kind"]=23
        new_score_info21["lower"]["full_house"]=25
        new_score_info21["lower"]["yahtzee"]=50
        new_score_info21["lower"]["chance"]=10
        updated_2_1 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard_2_1_info['id']}", json=new_score_info21).json()
        new_score_info22=get_blank_scorecard()
        new_score_info22["lower"]["three_of_a_kind"]=20
        new_score_info22["lower"]["four_of_a_kind"]=18
        new_score_info22["lower"]["full_house"]=25
        new_score_info22["lower"]["yahtzee"]=50
        new_score_info22["lower"]["chance"]=24
        updated_2_2 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard_2_2_info['id']}", json=new_score_info22).json()

        scorecard_3_2={
            "game_id":game3_info["id"],
            "user_id":user2_info["id"],
            "turn_order":1
        }
        scorecard_3_3={
            "game_id":game3_info["id"],
            "user_id":user3_info["id"],
            "turn_order":2
        }
        scorecard_3_2_info = requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_3_2).json()
        scorecard_3_3_info = requests.post("http://127.0.0.1:5000/scorecards", json=scorecard_3_3).json()
        new_score_info32=get_blank_scorecard()
        new_score_info32["lower"]["three_of_a_kind"]=20
        new_score_info32["lower"]["yahtzee"]=50
        new_score_info32["lower"]["chance"]=24
        updated_3_2 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard_3_2_info['id']}", json=new_score_info32).json()
        new_score_info33=get_blank_scorecard()
        new_score_info33["lower"]["three_of_a_kind"]=26
        new_score_info33["lower"]["yahtzee"]=50
        new_score_info33["lower"]["chance"]=18
        updated_3_3 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard_3_3_info['id']}", json=new_score_info33).json()
    
        high_scores = requests.get(f"http://127.0.0.1:5000/scores").json()

        self.assertEqual(len(high_scores), 6, "The user should have 6 scores")  
        self.assertEqual(high_scores[0]["score"], 137, "The 1st score should be 109")  
        self.assertEqual(high_scores[1]["score"], 132, "The 2nd score should be 27")  
        self.assertEqual(high_scores[2]["score"], 94, "The 3rd score should be 2")  
        self.assertEqual(high_scores[3]["score"], 94, "The 4th score should be 0")
        self.assertEqual(high_scores[4]["score"], 22, "The 5th score should be 0")
        self.assertEqual(high_scores[5]["score"], 19, "The 6th score should be 0")
        game_name = Game.get_game(id=scorecard_2_2_info["game_id"])["message"]["name"]
        self.assertEqual(high_scores[0]["game_name"], game_name, "The correct game_id should be included with the score")
        username = User.get_user(id=user1_info['id'])["message"]['username']
        self.assertEqual(high_scores[5]["username"], username, "The correct username should be included with the score")
    '''
    def test_GET_username_scores_none(self):
        """3.15) ScorecardsController: GET /scores/<username> w/ fewer than 10 scores scores""" 
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        user2_info = requests.post("http://127.0.0.1:5000/users", json=user2).json()
        user3_info = requests.post("http://127.0.0.1:5000/users", json=user3).json()
        response = requests.get(f"http://127.0.0.1:5000/scores/{user1_info['username']}").json()
        self.assertEqual(response, [], "GETing all scores with no scores should return []")  
    
    def test_GET_username_scores_more_than_10(self):
        """3.16) ScorecardsController: GET /scores/<username> w/ more than 10 scores scores"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        game2_info = requests.post("http://127.0.0.1:5000/games", json=game2).json()
        game3_info = requests.post("http://127.0.0.1:5000/games", json=game3).json()
        game4_info = requests.post("http://127.0.0.1:5000/games", json=game4).json()
        game5_info = requests.post("http://127.0.0.1:5000/games", json=game5).json()
        game6_info = requests.post("http://127.0.0.1:5000/games", json=game6).json()
        game7_info = requests.post("http://127.0.0.1:5000/games", json=game7).json()
        game8_info = requests.post("http://127.0.0.1:5000/games", json=game8).json()
        game9_info = requests.post("http://127.0.0.1:5000/games", json=game9).json()
        game10_info = requests.post("http://127.0.0.1:5000/games", json=game10).json()
        game11_info = requests.post("http://127.0.0.1:5000/games", json=game11).json()
        game12_info = requests.post("http://127.0.0.1:5000/games", json=game12).json()
        scorecard1={
            "game_id":game1_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard1_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard1).json() 
        scorecard2={
            "game_id":game2_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard2_info= requests.post("http://127.0.0.1:5000/scorecards", json=scorecard2).json()  
        scorecard3={
            "game_id":game3_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard3_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard3).json() 
        scorecard4={
            "game_id":game4_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard4_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard4).json() 
        scorecard5={
            "game_id":game5_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard5_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard5).json() 
        scorecard6={
            "game_id":game6_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard6_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard6).json() 
        scorecard7={
            "game_id":game7_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard7_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard7).json() 
        scorecard8={
            "game_id":game8_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard8_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard8).json() 
        scorecard9={
            "game_id":game9_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard9_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard9).json() 
        scorecard10={
            "game_id":game10_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard10_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard10).json() 
        scorecard11={
            "game_id":game11_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard11_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard11).json()
        scorecard12={
            "game_id":game12_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard12_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard12).json()  
        new_score_info1=get_blank_scorecard()
        new_score_info1["upper"]["ones"]=2
        new_score_info1["upper"]["twos"]=8
        new_score_info1["upper"]["threes"]=12
        new_score_info1["upper"]["fours"]=16
        new_score_info1["upper"]["fives"]=25
        new_score_info1["upper"]["sixes"]=12
        new_score_info1["lower"]["three_of_a_kind"]=24
        new_score_info1["lower"]["four_of_a_kind"]=23
        new_score_info1["lower"]["full_house"]=25
        new_score_info1["lower"]["yahtzee"]=50
        new_score_info1["lower"]["chance"]=10
        updated_1 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard1_info['id']}", json=new_score_info1).json()
        new_score_info2=get_blank_scorecard()
        new_score_info2["upper"]["ones"]=2 
        new_score_info2["lower"]["full_house"]=25
        updated_2 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard2_info['id']}", json=new_score_info2).json()
        new_score_info3=get_blank_scorecard()
        new_score_info3["lower"]["full_house"]=2
        updated_3 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard3_info['id']}", json=new_score_info3).json()
        new_score_info5=get_blank_scorecard()
        new_score_info5["upper"]["ones"]=2
        new_score_info5["upper"]["twos"]=8
        new_score_info5["upper"]["threes"]=12
        new_score_info5["upper"]["fours"]=16
        new_score_info5["upper"]["fives"]=25
        new_score_info5["upper"]["sixes"]=12
        new_score_info5["lower"]["three_of_a_kind"]=24
        new_score_info5["lower"]["four_of_a_kind"]=23
        new_score_info5["lower"]["full_house"]=25
        new_score_info5["lower"]["yahtzee"]=50
        updated_5 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard5_info['id']}", json=new_score_info5).json()
        new_score_info6=get_blank_scorecard()
        new_score_info6["upper"]["ones"]=2
        new_score_info6["upper"]["twos"]=8
        new_score_info6["upper"]["threes"]=12
        new_score_info6["upper"]["fours"]=16
        new_score_info6["lower"]["three_of_a_kind"]=24
        new_score_info6["lower"]["four_of_a_kind"]=23
        new_score_info6["lower"]["full_house"]=25
        new_score_info6["lower"]["yahtzee"]=50
        updated_6 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard6_info['id']}", json=new_score_info6).json()
        new_score_info10=get_blank_scorecard()
        new_score_info10["upper"]["ones"]=2
        new_score_info10["upper"]["twos"]=8
        new_score_info10["upper"]["threes"]=12
        new_score_info10["upper"]["fours"]=16
        new_score_info10["lower"]["three_of_a_kind"]=24
        new_score_info10["lower"]["four_of_a_kind"]=23
        new_score_info10["lower"]["yahtzee"]=50
        updated_10 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard10_info['id']}", json=new_score_info10).json()
        new_score_info11=get_blank_scorecard()
        new_score_info11["upper"]["ones"]=2
        new_score_info11["upper"]["twos"]=8
        updated_11 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard11_info['id']}", json=new_score_info11).json()

        user_scores = requests.get(f"http://127.0.0.1:5000/scores/{user1_info['username']}").json()
        self.assertEqual(len(user_scores), 12, "The user should have 12 scores")  
        self.assertEqual(user_scores[0]["score"], 207, "The 1st score should be 109")  
        self.assertEqual(user_scores[1]["score"], 197, "The 2nd score should be 27")  
        self.assertEqual(user_scores[2]["score"], 160, "The 3rd score should be 2")  
        self.assertEqual(user_scores[3]["score"], 135, "The 4th score should be 0")
        self.assertEqual(user_scores[4]["score"], 27, "The 5th score should be 0")
        self.assertEqual(user_scores[5]["score"], 10, "The 6th score should be 0")
        self.assertEqual(user_scores[6]["score"], 2, "The 7th score should be 0")
        self.assertEqual(user_scores[7]["score"], 0, "The 8th score should be 0")
        self.assertEqual(user_scores[8]["score"], 0, "The 9th score should be 0")
        self.assertEqual(user_scores[9]["score"], 0, "The 10th score should be 0") 
        game_name = Game.get_game(id=game1_info["id"])["message"]["name"]
        self.assertEqual(user_scores[0]["game_name"], game_name, "The correct game_id should be included with the score")
    
    def test_GET_username_scores_fewer_than_10(self):
        """3.17) ScorecardsController: GET /scores/<username> w/ fewer than 10 scores scores"""
        user1_info = requests.post("http://127.0.0.1:5000/users", json=user1).json()
        game1_info = requests.post("http://127.0.0.1:5000/games", json=game1).json()
        game2_info = requests.post("http://127.0.0.1:5000/games", json=game2).json()
        game3_info = requests.post("http://127.0.0.1:5000/games", json=game3).json()
        game4_info = requests.post("http://127.0.0.1:5000/games", json=game4).json()

        scorecard1={
            "game_id":game1_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard1_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard1).json() 
        scorecard2={
            "game_id":game2_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard2_info= requests.post("http://127.0.0.1:5000/scorecards", json=scorecard2).json()  
        scorecard3={
            "game_id":game3_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard3_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard3).json() 
        scorecard4={
            "game_id":game4_info["id"],
            "user_id":user1_info["id"],
            "turn_order":1
        }
        scorecard4_info=requests.post("http://127.0.0.1:5000/scorecards", json=scorecard4).json() 

        new_score_info1=get_blank_scorecard()
        new_score_info1["upper"]["ones"]=2
        new_score_info1["upper"]["twos"]=8
        new_score_info1["lower"]["full_house"]=25
        new_score_info1["lower"]["three_of_a_kind"]=24
        new_score_info1["lower"]["yahtzee"]=50
        updated_1 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard1_info['id']}", json=new_score_info1).json()
        new_score_info2=get_blank_scorecard()
        new_score_info2["upper"]["ones"]=2 
        new_score_info2["lower"]["full_house"]=25
        updated_2 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard2_info['id']}", json=new_score_info2).json()
        new_score_info3=get_blank_scorecard()
        new_score_info3["lower"]["full_house"]=2
        updated_3 = requests.put(f"http://127.0.0.1:5000/scorecards/{scorecard3_info['id']}", json=new_score_info3).json()

        user_scores = requests.get(f"http://127.0.0.1:5000/scores/{user1_info['username']}").json()
        self.assertEqual(len(user_scores), 4, "The user should have 4 scores")  
        self.assertEqual(user_scores[0]["score"], 109, "The first score should be 109")  
        self.assertEqual(user_scores[1]["score"], 27, "The second score should be 27")  
        self.assertEqual(user_scores[2]["score"], 2, "The third score should be 2")  
        self.assertEqual(user_scores[3]["score"], 0, "The fourth score should be 0")  
        game_name = Game.get_game(id=game1_info["id"])["message"]["name"]
        self.assertEqual(user_scores[0]["game_name"], game_name, "The correct game_id should be included with the score")
    '''
   
if __name__ == "__main__":
      unittest.main()