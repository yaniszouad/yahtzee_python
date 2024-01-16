import unittest
import sqlite3
import os
import datetime
import json

from ScorecardsModel import Scorecard
from UsersModel import User
from GamesModel import Game

yahtzee_db_name=f"{os.getcwd()}/yahtzeeDB.db"
table_name = "scorecards"

# initialize all three tables
users = User(yahtzee_db_name)
games = Game(yahtzee_db_name)
scorecards = Scorecard(yahtzee_db_name)


# test data
game_1={
    "name":"ourGame1",
    "link":"1234abcd"
}
game_2={
    "name":"ourGame2",
    "link":"2234abcd"
}
game_3={
    "name":"ourGame3",
    "link":"3234abcd"
}
game_4={
    "name":"ourGame4",
    "link":"4234abcd"
}
time1 = datetime.datetime.now()
time2 = datetime.datetime.now()
time3 = datetime.datetime.now()
time4 = datetime.datetime.now()

games_data = [
    (1, "ourGame1", "1234abcd", time1, time1),
    (2, "ourGame2", "2234abcd", time2, time2),
    (3, "ourGame3", "3234abcd", time3, time3),
    (4, "ourGame4", "4234abcd", time4, time4)
]
user_1={
    "email":"cookie.monster@trinityschoolnyc.org",
    "username":"cookieM",
    "password":"123TriniT"
}
user_2={
    "email":"justin.gohde@trinityschoolnyc.org",
    "username":"justingohde",
    "password":"123TriniT"
}
user_3={
    "email":"zelda@trinityschoolnyc.org",
    "username":"princessZ",
    "password":"123TriniT"
}
user_4={
    "email":"test.user@trinityschoolnyc.org",
    "username":"testuser",
    "password":"123TriniT"
}
user_5={
    "email":"test.user.2@trinityschoolnyc.org",
    "username":"testuser2",
    "password":"123TriniT"
}
users_data = [
    (1, "cookie.monster@trinityschoolnyc.org", "cookieM", "123TriniT"),
    (2, "justin.gohde@trinityschoolnyc.org", "justingohde", "123TriniT"),
    (3, "zelda@trinityschoolnyc.org", "princessZ", "123TriniT"),
    (4, "test.user@trinityschoolnyc.org", "testuser", "123TriniT")
]

blank_card={
            "dice_rolls":3,
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

class TestScorecardsModel(unittest.TestCase):
    def test_1(self):
        """ScorecardsModel: create_scorecard w/ 1 scorecard"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        results = users.create_user(user_1)
        u1 = results["message"]  

        results = games.create_game(game_1)
        g1 = results["message"]

        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj = results["message"]

        # verify all fields are present in the object and the score_info object is correct
        self.assertEqual(results["result"], "success", "Creating a scorecard should return success")
        self.assertEqual(card_obj["game_id"], g1["id"] , "game_id of returned scorecard should match")
        self.assertEqual(card_obj["user_id"], u1["id"], "user_id of returned scorecard should match")
        self.assertEqual(card_obj["score_info"], blank_card, "score_info of returned scorecard should match blank card dictionary")
        self.assertEqual(card_obj["turn_order"], 1, "turn_order of returned scorecard should be 1")
        self.assertEqual(card_obj["score"], 0, "score of returned scorecard should be 0")

        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {table_name};"
            results = cursor.execute(query)
            all_cards = []
            for card in results.fetchall():
                all_cards.append(card)

            self.assertEqual(len(all_cards), 1, "Creating a single scorecard should result in a table with 1 scorecard")
            self.assertEqual(all_cards[0][1], g1['id'], "game_id of scorecard in DB should match data of added scorecard")
            self.assertEqual(all_cards[0][2], u1['id'], "user_id of scorecard in DB should match data of added scorecard")    
            self.assertEqual(json.loads(all_cards[0][3]), blank_card, "score_info of scorecard in DB should match data of added scorecard")    
            self.assertEqual(all_cards[0][4], 1, "turn_order of scorecard in DB should match data of added scorecard")    
            self.assertEqual(all_cards[0][5], 0, "score of scorecard in DB should match data of added scorecard")    

        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()

    def test_2(self):
        """ScorecardsModel: create_scorecard w/ 4 scorecards in same game"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        u2 = results["message"] 
        results = users.create_user(user_3)
        u3 = results["message"] 
        results = users.create_user(user_4)
        u4 = results["message"] 

        results = games.create_game(game_1)
        g1 = results["message"]
        
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
        self.assertEqual(results["result"], "success", "Creating four scorecards for the same game should return success")
        results = scorecards.create_scorecard(g1["id"], u2["id"], 2)
        card_obj_2 = results["message"]
        self.assertEqual(results["result"], "success", "Creating four scorecards for the same game should return success")
        results = scorecards.create_scorecard(g1["id"], u3["id"], 3)
        card_obj_3 = results["message"]
        self.assertEqual(results["result"], "success", "Creating four scorecards for the same game should return success")
        results = scorecards.create_scorecard(g1["id"], u4["id"], 4)
        card_obj_4 = results["message"]
        self.assertEqual(results["result"], "success", "Creating four scorecards for the same game should return success")
        
        self.assertEqual(card_obj_1["game_id"], g1["id"] , "game_id of returned scorecard 1 should match")
        self.assertEqual(card_obj_2["game_id"], g1["id"] , "game_id of returned scorecard 2 should match")
        self.assertEqual(card_obj_3["game_id"], g1["id"] , "game_id of returned scorecard 3 should match")
        self.assertEqual(card_obj_4["game_id"], g1["id"] , "game_id of returned scorecard 4 should match")
        self.assertEqual(card_obj_1["user_id"], u1["id"], "user_id of returned scorecard 1 should match")
        self.assertEqual(card_obj_2["user_id"], u2["id"], "user_id of returned scorecard 2 should match")
        self.assertEqual(card_obj_3["user_id"], u3["id"], "user_id of returned scorecard 3 should match")
        self.assertEqual(card_obj_4["user_id"], u4["id"], "user_id of returned scorecard 4 should match")
        self.assertEqual(card_obj_1["score_info"], blank_card, "score_info of returned scorecard 1 should match blank card dictionary")
        self.assertEqual(card_obj_2["score_info"], blank_card, "score_info of returned scorecard 2 should match blank card dictionary")
        self.assertEqual(card_obj_3["score_info"], blank_card, "score_info of returned scorecard 3 should match blank card dictionary")
        self.assertEqual(card_obj_4["score_info"], blank_card, "score_info of returned scorecard 4 should match blank card dictionary")
        self.assertEqual(card_obj_1["turn_order"], 1, "turn_order of returned scorecard 1 should be 1")
        self.assertEqual(card_obj_2["turn_order"], 2, "turn_order of returned scorecard 2 should be 2")
        self.assertEqual(card_obj_3["turn_order"], 3, "turn_order of returned scorecard 3 should be 3")
        self.assertEqual(card_obj_4["turn_order"], 4, "turn_order of returned scorecard 4 should be 4")
        self.assertEqual(card_obj_1["score"], 0, "score of returned scorecard 1 should be 0")
        self.assertEqual(card_obj_2["score"], 0, "score of returned scorecard 2 should be 0")
        self.assertEqual(card_obj_3["score"], 0, "score of returned scorecard 3 should be 0")
        self.assertEqual(card_obj_4["score"], 0, "score of returned scorecard 4 should be 0")
      
    def test_3(self):
        """ScorecardsModel: create_scorecard w/ 5 scorecards"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        u2 = results["message"] 
        results = users.create_user(user_3)
        u3 = results["message"] 
        results = users.create_user(user_4)
        u4 = results["message"] 
        results = users.create_user(user_5)
        u5 = results["message"] 

        results = games.create_game(game_1)
        g1 = results["message"]

        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u2["id"], 2)
        card_obj_2 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u3["id"], 3)
        card_obj_3 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u4["id"], 4)
        card_obj_4 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u5["id"], 5)
        card_obj_5 = results["message"]

        self.assertEqual(results["result"], "error", "Creating five scorecards for the same game should return error")
   
    def test_4(self):
        """ScorecardsModel: create_scorecard w/ 1 user on two scorecards for the same game"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()
        
        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        
        results = games.create_game(game_1)
        g1 = results["message"]
        
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u1["id"], 2)
        card_obj_2 = results["message"]
        self.assertEqual(results["result"], "error", "Creating a second scorecard for a user in the same game should return error")
          
    def test_5(self):
        """ScorecardsModel: create_scorecard w/ 1 user on two scorecards for different games"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        
        results = games.create_game(game_1)
        g1 = results["message"]

        results = games.create_game(game_2)
        g2 = results["message"]
        
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
        results = scorecards.create_scorecard(g2["id"], u1["id"], 2)
        card_obj_2 = results["message"]
        self.assertEqual(results["result"], "success", "Creating two scorecards for a user in two different games should return success")

    def test_6(self):
        """ScorecardsModel: get_scorecard that exists"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()
        
        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        u2 = results["message"] 
        results = users.create_user(user_3)
        u3 = results["message"] 

        results = games.create_game(game_1)
        g1 = results["message"]
        
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u2["id"], 2)
        card_obj_2 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u3["id"], 3)
        card_obj_3 = results["message"]

        results = scorecards.get_scorecard(card_obj_2["id"])

        self.assertEqual(results["result"], "success", "Getting a scorecard that exists should return success")
        self.assertEqual(results["message"]["game_id"], g1["id"] , "game_id of returned scorecard should match")

        self.assertEqual(results["message"]["user_id"], u2["id"], "user_id of returned scorecard should match")
        self.assertEqual(results["message"]["score_info"], blank_card, "score_info of returned scorecard should match blank card dictionary")
        self.assertEqual(results["message"]["turn_order"], 2, "turn_order of returned scorecard should be 2")
 
    def test_7(self):
        """ScorecardsModel: get_scorecard that doesn't exist"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()
        
        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        u2 = results["message"] 
        results = users.create_user(user_3)
        u3 = results["message"] 

        results = games.create_game(game_1)
        g1 = results["message"]
        
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u2["id"], 2)
        card_obj_2 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u3["id"], 3)
        card_obj_3 = results["message"]

        results = scorecards.get_scorecard(-12345)
        self.assertEqual(results["result"], "error", "Getting a scorecard that doesn't exist should return error")

    def test_8(self):
        """ScorecardsModel: get_scorecards with no scorecards"""
        scorecards.initialize_scorecards_table()
        all_cards = scorecards.get_scorecards()

        self.assertEqual(all_cards["result"], "success", "Askings for all games when no games exists should return success")
        self.assertEqual(len(all_cards["message"]), 0, "The length of an empty list should be 0")

    def test_9(self):
        """ScorecardsModel: get_scorecards with multiple scorecards"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        u2 = results["message"] 
        results = users.create_user(user_3)
        u3 = results["message"] 

        results = games.create_game(game_1)
        g1 = results["message"]
        
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u2["id"], 2)
        card_obj_2 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u3["id"], 3)
        card_obj_3 = results["message"]

        results = scorecards.get_scorecards()
        self.assertEqual(results["result"], "success", "Getting a scorecard that exists should return success")
        self.assertEqual(len(results["message"]), 3, "Should return a length of 3 for a table with three scorecards")
        self.assertIn(card_obj_1, results["message"], f"{u1} should be in the list of scorecards returned")
        self.assertIn(card_obj_2, results["message"], f"{u2} should be in the list of scorecards returned")
        self.assertIn(card_obj_3, results["message"], f"{u3} should be in the list of scorecards returned")

    def test_10(self):
        """ScorecardsModel: get_game_scorecards with no scorecards"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        u2 = results["message"] 
        results = users.create_user(user_3)
        u3 = results["message"] 

        results = games.create_game(game_1)
        g1 = results["message"]

        results = games.create_game(game_2)
        g2 = results["message"]
        
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u2["id"], 2)
        card_obj_2 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u3["id"], 3)
        card_obj_3 = results["message"]

        results = scorecards.get_game_scorecards(g2["id"])

        self.assertEqual(results["result"], "success", "Getting scorecards from an existing game with no scorecards should return success")
        self.assertEqual(len(results["message"]), 0, "The number of scorecards returned should be 0")

    def test_11(self):
        """ScorecardsModel: get_game_scorecards with 1 scorecard"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        u2 = results["message"] 
        results = users.create_user(user_3)
        u3 = results["message"] 

        results = games.create_game(game_1)
        g1 = results["message"]

        results = games.create_game(game_2)
        g2 = results["message"]
        
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
        results = scorecards.create_scorecard(g2["id"], u2["id"], 1)
        card_obj_2 = results["message"]
        results = scorecards.create_scorecard(g2["id"], u3["id"], 2)
        card_obj_3 = results["message"]

        results = scorecards.get_game_scorecards(g1["id"])
        returned_card = results["message"][0]
        self.assertEqual(results["result"], "success", "Getting scorecards from an existing game with 1 scorecard should return success")
        self.assertEqual(len(results["message"]), 1, "The number of scorecards returned should be 1")
        self.assertEqual(returned_card["id"], card_obj_1["id"], "The id of the scorecard returned should match the id of the scorecard added to the game")
  
    def test_12(self):
        """get_game_scorecards with multiple scorecards"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        u2 = results["message"] 
        results = users.create_user(user_3)
        u3 = results["message"] 

        results = games.create_game(game_1)
        g1 = results["message"]

        results = games.create_game(game_2)
        g2 = results["message"]
        
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
        results = scorecards.create_scorecard(g2["id"], u2["id"], 1)
        card_obj_2 = results["message"]
        results = scorecards.create_scorecard(g2["id"], u3["id"], 2)
        card_obj_3 = results["message"]
        results = scorecards.create_scorecard(g2["id"], u1["id"], 3)
        card_obj_4 = results["message"]

        results = scorecards.get_game_scorecards(g2["id"])
        returned_cards = results["message"]
        all_ids =[]
        for card in returned_cards:
            all_ids.append(card["id"])

        self.assertEqual(results["result"], "success", "Getting scorecards from an existing game with multiple scorecards should return success")
        self.assertEqual(len(results["message"]), 3, "The number of scorecards returned should be 3")
        self.assertIn(card_obj_2["id"], all_ids, "The id of the first scorecard should appear in the list of ids returned")
        self.assertIn(card_obj_3["id"], all_ids, "The id of the first scorecard should appear in the list of ids returned")
        self.assertIn(card_obj_4["id"], all_ids, "The id of the first scorecard should appear in the list of ids returned")

    def test_13(self):
        """ScorecardsModel: update_scorecard with 1 entry in score_info"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        new_card={
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
                "full_house":25,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }

        results = users.create_user(user_1)
        u1 = results["message"]  
        results = games.create_game(game_1)
        g1 = results["message"]
 
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
  
        results=scorecards.update_scorecard(card_obj_1["id"], new_card);
        card = results["message"]
        self.assertEqual(results["result"], "success", "Updating a scorecard should result in success")
        self.assertEqual(card["id"], card_obj_1["id"], "Scorecard id returned should be the same as the id of the card that was changed")
        self.assertEqual(card["game_id"], card_obj_1["game_id"], "Scorecard game_id returned should be the same as the game_id of the card that was changed")
        self.assertEqual(card["user_id"], card_obj_1["user_id"], "Scorecard user_id returned should be the same as the user_id of the card that was changed")
        self.assertEqual(card["score_info"], new_card, "score_info returned should be the same as the score_info that was changed")
        self.assertEqual(card["turn_order"], card_obj_1["turn_order"], "turn_order returned should be the same as the turn_order that was changed")
        self.assertEqual(card["score"], 25, "score returned should be 25")

        results=scorecards.get_scorecard(card_obj_1["id"]);
        card = results["message"]
        self.assertEqual(card["id"], card_obj_1["id"], "Scorecard id in DB should be the same as the id of the card that was changed")
        self.assertEqual(card["game_id"], card_obj_1["game_id"], "Scorecard game_id in DB should be the same as the game_id of the card that was changed")
        self.assertEqual(card["user_id"], card_obj_1["user_id"], "Scorecard user_id in DB should be the same as the user_id of the card that was changed")
        self.assertEqual(card["score_info"], new_card, "score_info in DB should be the same as the score_info that was changed")
        self.assertEqual(card["turn_order"], card_obj_1["turn_order"], "turn_order in DB should be the same as the turn_order that was changed")
        self.assertEqual(card["score"], 25, "score in DB should be 25")

    def test_14(self):
        """ScorecardsModel: update_scorecard with multiple entries in score_info"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        new_card={
            "dice_rolls":0,
            "upper":{
                "ones":4,
                "twos":-1,
                "threes":-1,
                "fours":16,
                "fives":0,
                "sixes":6
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":25,
                "small_straight":-1,
                "large_straight":40,
                "yahtzee":50,
                "chance":-1
            }
        }
        
        results = users.create_user(user_1)
        u1 = results["message"]  
        results = games.create_game(game_1)
        g1 = results["message"]
 
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
  
        results=scorecards.update_scorecard(card_obj_1["id"], new_card);
        card = results["message"]
        self.assertEqual(results["result"], "success", "Updating a scorecard should result in success")
        self.assertEqual(card["id"], card_obj_1["id"], "Scorecard id returned should be the same as the id of the card that was changed")
        self.assertEqual(card["game_id"], card_obj_1["game_id"], "Scorecard game_id returned should be the same as the game_id of the card that was changed")
        self.assertEqual(card["user_id"], card_obj_1["user_id"], "Scorecard user_id returned should be the same as the user_id of the card that was changed")
        self.assertEqual(card["score_info"], new_card, "score_info returned should be the same as the score_info that was changed")
        self.assertEqual(card["turn_order"], card_obj_1["turn_order"], "turn_order returned should be the same as the turn_order that was changed")
        self.assertEqual(card["score"], 141, "score returned should be 25")

        results=scorecards.get_scorecard(card_obj_1["id"]);
        card = results["message"]
        self.assertEqual(card["id"], card_obj_1["id"], "Scorecard id in DB should be the same as the id of the card that was changed")
        self.assertEqual(card["game_id"], card_obj_1["game_id"], "Scorecard game_id in DB should be the same as the game_id of the card that was changed")
        self.assertEqual(card["user_id"], card_obj_1["user_id"], "Scorecard user_id in DB should be the same as the user_id of the card that was changed")
        self.assertEqual(card["score_info"], new_card, "score_info in DB should be the same as the score_info that was changed")
        self.assertEqual(card["turn_order"], card_obj_1["turn_order"], "turn_order in DB should be the same as the turn_order that was changed")
        self.assertEqual(card["score"], 141, "score in DB should be 25")
                
    def test_15(self):
        """ScorecardsModel: update_scorecard that doesn't exist"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        u2 = results["message"] 
        results = users.create_user(user_3)
        u3 = results["message"] 

        results = games.create_game(game_1)
        g1 = results["message"]
 
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
 
        results = scorecards.create_scorecard(g1["id"], u2["id"], 2)
        card_obj_2 = results["message"]
 
        results = scorecards.create_scorecard(g1["id"], u3["id"], 3)
        card_obj_3 = results["message"]
 
        results = scorecards.update_scorecard(-234455, blank_card)
        self.assertEqual(results["result"], "error", "Updating a scorecard that doesn't exist should return error")

    def test_16(self):
        """ScorecardsModel: delete_scorecard that exists"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        u2 = results["message"] 
        results = users.create_user(user_3)
        u3 = results["message"] 

        results = games.create_game(game_1)
        g1 = results["message"]
        results = games.create_game(game_2)
        g2 = results["message"]
        
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
        results = scorecards.create_scorecard(g2["id"], u2["id"], 1)
        card_obj_2 = results["message"]
        results = scorecards.create_scorecard(g2["id"], u3["id"], 2)
        card_obj_3 = results["message"]
        results = scorecards.create_scorecard(g2["id"], u1["id"], 3)
        card_obj_4 = results["message"]

        scorecards.remove_scorecard(card_obj_4["id"])
        results = scorecards.get_game_scorecards(g2["id"])
        returned_cards = results["message"]
        all_ids =[]
        for card in returned_cards:
            all_ids.append(card["id"])

        self.assertEqual(results["result"], "success", "Getting scorecards from an existing game with multiple scorecards should return success")
        self.assertEqual(len(results["message"]), 2, "The number of scorecards returned should be 2")
        self.assertIn(card_obj_2["id"], all_ids, "The id of the first scorecard should appear in the list of ids returned")
        self.assertIn(card_obj_3["id"], all_ids, "The id of the first scorecard should appear in the list of ids returned")
        
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {table_name} WHERE {table_name}.game_id = {g2['id']};"
            results = cursor.execute(query)

            all_card_ids = []
            for card in results.fetchall():
                all_card_ids.append(card[0])

            self.assertEqual(len(all_card_ids), 2, "The number of scorecards in the DB should be 2")
            self.assertIn(card_obj_2["id"], all_card_ids, "The id of the first scorecard should appear in the DB")
            self.assertIn(card_obj_3["id"], all_card_ids, "The id of the first scorecard should appear in the DB")
            self.assertNotIn(card_obj_4["id"], all_card_ids, "The id of the deleted scorecard should not appear in the DB")

        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()

    def test_17(self):
        """ScorecardsModel: delete_scorecard that doesn't exist"""
        users.initialize_users_table()
        games.initialize_games_table()
        scorecards.initialize_scorecards_table()

        results = users.create_user(user_1)
        u1 = results["message"]  
        results = users.create_user(user_2)
        u2 = results["message"] 
        results = users.create_user(user_3)
        u3 = results["message"] 

        results = games.create_game(game_1)
        g1 = results["message"]
        
        results = scorecards.create_scorecard(g1["id"], u1["id"], 1)
        card_obj_1 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u2["id"], 2)
        card_obj_2 = results["message"]
        results = scorecards.create_scorecard(g1["id"], u3["id"], 3)
        card_obj_3 = results["message"]

        results = scorecards.remove_scorecard(-234455)
        self.assertEqual(results["result"], "error", "Updating a scorecard that doesn't exist should return error")


TestScorecardsModel().test_5()