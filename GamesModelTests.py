import unittest
import sqlite3
import os
import datetime

from GamesModel import Game

yahtzee_db_name=f"{os.getcwd()}/yahtzeeDB.db"
table_name = "games"

games = Game(yahtzee_db_name)

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
games_data = [
    (1, "ourGame1", "1234abcd", datetime.datetime.now()),
    (2, "ourGame2", "2234abcd", datetime.datetime.now()),
    (3, "ourGame3", "3234abcd", datetime.datetime.now()),
    (4, "ourGame4", "4234abcd", datetime.datetime.now())
]

class TestgameModel(unittest.TestCase):
    def test_1(self):
        """GamesModel: create_game w/ 1 game"""
        games.initialize_games_table()
        results = games.create_game(game_1)
        self.assertEqual(results["result"], "success", "Creating a game should return success")
        self.assertEqual(results["message"]["name"], f"{game_1['name']}", "name of returned game should match name of added game")
        self.assertEqual(results["message"]["link"], f"{game_1['link']}", "link of returned game should match link of added game") 
        self.assertIn("created", results["message"], "All games should have a created attribute")
        self.assertIn("finished", results["message"], "All games should have a finished attribute")
        self.assertEqual(results["message"]["created"], results["message"]["finished"], "Games should be created with the same finish time as start time")

        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {table_name};"
            results = cursor.execute(query)
            all_games = []
            for game in results.fetchall():
                all_games.append(game)
            self.assertEqual(len(all_games), 1, "Creating a single game should result in a table with 1 game")
            self.assertEqual(all_games[0][1], f"{game_1['name']}", "Data of returned game should match data of added game")
            self.assertEqual(all_games[0][2], f"{game_1['link']}", "Data of returned game should match data of added game")    

        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()
    
    def test_2(self):
        """GamesModel: create_game w/ 4 games"""
        games.initialize_games_table()
        games.create_game(game_1)
        games.create_game(game_2)
        games.create_game(game_3)
        games.create_game(game_4)
        
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {table_name} ORDER BY name;"
            results = cursor.execute(query)
            all_games = []
            for game in results.fetchall():
                all_games.append(game)
            self.assertEqual(len(all_games), 4, "Creating 4 games should result in a table with 4 games")
            self.assertEqual(all_games[0][1], f"{game_1['name']}", "name of returned game should match name of added game")
            self.assertEqual(all_games[1][1], f"{game_2['name']}", "name of returned game should match name of added game")
            self.assertEqual(all_games[2][2], f"{game_3['link']}", "link of returned game should match link of added game")
            self.assertEqual(all_games[3][2], f"{game_4['link']}", "link of returned game should match link of added game")    
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()

    def test_3(self):
        """GamesModel: create_game w/ already taken link or name"""
        games.initialize_games_table()
        results = games.create_game(game_1)
        game_1_name={
            "name":"ourGame1", #same as game_1
            "link":"asdf31234", #unique
        }
        results = games.create_game(game_1_name)
        self.assertEqual(results["result"], "error", "Creating a game with the same name should result in an error")

        game_1_link={
            "name":"ourGameasdf2", #unique
            "link":"1234abcd", #same as game_1
        }
        results = games.create_game(game_1_link)
        self.assertEqual(results["result"], "error", "Creating a game with the same link should result in an error")

    def test_4(self):
        """GamesModel: create_game w/ data in incorrect format"""
        games.initialize_games_table()
        game_incorrect_name_1={
            "name":"test.game", # includes "."
            "link":"testgame",  # ok
        }
        results = games.create_game(game_incorrect_name_1)
        self.assertEqual(results["result"], "error", "Creating a game with invalid name should return error")
        
        game_incorrect_name_2={
            "name":"our-game",  # includes "-"
            "link":"testgameasd323",  # ok
        }
        results = games.create_game(game_incorrect_name_2)
        self.assertEqual(results["result"], "error", "Creating a game with invalid name should return error")
        
        game_incorrect_link_1={
            "name":"ourGame123",
            "link":"ourGame123@!345",
        }
        results = games.create_game(game_incorrect_link_1)
        self.assertEqual(results["result"], "error", "Creating a game with invalid link should return error")
        
        game_incorrect_link_2={
            "name":"ourGame123",
            "link":"ourGame123 345",
        }
        results = games.create_game(game_incorrect_link_2)
        self.assertEqual(results["result"], "error", "Creating a game with invalid link should return error")
    
    def test_5(self):
        """GamesModel: exists w/ link and id"""
        games.initialize_games_table()
        u1=games.create_game(game_1)
        u2=games.create_game(game_2)
        u3=games.create_game(game_3)
        
        result_gamename = games.exists(name=u3["message"]["name"])  
        self.assertEqual(result_gamename["result"], "success", "Should return success")
        self.assertEqual(result_gamename["message"], True, "name that exists should return True")

        result_id = games.exists(id=u2["message"]["id"])
        self.assertEqual(result_id["result"], "success", "Should return success")
        self.assertEqual(result_id["message"], True, "id that exists should return True")
    
    def test_6(self):
        """GamesModel: doesn't exist w/ link and id"""
        games.initialize_games_table()
        u1=games.create_game(game_1)
        u2=games.create_game(game_2)
        u3=games.create_game(game_3)
        
        result_gamename = games.exists(name="princessZZZZZZZ")
        self.assertEqual(result_gamename["result"], "success", "Should return success for link that doesn't exist")
        self.assertEqual(result_gamename["message"], False, "name that exists should return False")

        result_id = games.exists(id=-1234567890)
        self.assertEqual(result_id["result"], "success", "Should return success for id that doesn't exist")
        self.assertEqual(result_id["message"], False, "id that exists should return False")
    
    def test_7(self):
        """GamesModel: get_game that exists w/ link and id"""
        games.initialize_games_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO games VALUES(?, ?, ?, ?, NULL);", games_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()
        
        game = games.get_game(name=game_4["name"])
        self.assertEqual(game["result"], "success", "getting an existing game by link should return success")
        self.assertEqual(game["message"]["name"], game_4["name"], "Data should match - name")
        self.assertEqual(game["message"]["link"], game_4["link"], "Data should match - link")

        game = games.get_game(id=3)
        self.assertEqual(game["result"], "success", "getting an existing game by id should return success")
        self.assertEqual(game["message"]["name"], game_3["name"], "Data should match - name")
        self.assertEqual(game["message"]["link"], game_3["link"], "Data should match - link")
    
    def test_8(self):
        """GamesModel: get_game that doesn't exist w/ link and id"""
        games.initialize_games_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO games VALUES(?, ?, ?, ?, NULL);", games_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()
        
        game = games.get_game(name="something")
        self.assertEqual(game["result"], "error", "getting a game that does't exist by link should return error")
  
        game = games.get_game(id=175)
        self.assertEqual(game["result"], "error", "getting a game that does't exist by id should return error")
 
    def test_9(self):
        """GamesModel: get_games with multiple games"""
        games.initialize_games_table()
        u1=games.create_game(game_1)
        u2=games.create_game(game_2)
        u3=games.create_game(game_3)

        all_games = games.get_games()
        
        self.assertEqual(all_games["result"], "success", "Askings for all games when 3 games exists should return success")
        self.assertEqual(len(all_games["message"]), 3, "The length of the list of games returned by get_games() should be 3")
        self.assertIn(u1["message"], all_games["message"], "Data of returned game should match data of added game")
        self.assertIn(u2["message"], all_games["message"], "Data of returned game should match data of added game")
        self.assertIn(u3["message"], all_games["message"], "Data of returned game should match data of added game")

    def test_10(self):
        """GamesModel: get_games with no games"""
        games.initialize_games_table()
        all_games = games.get_games()

        self.assertEqual(all_games["result"], "success", "Askings for all games when no games exists should return success")
        self.assertEqual(len(all_games["message"]), 0, "The length of an empty list should be 0")

    def test_11(self):
        """GamesModel: get_games with 1 game"""
        games.initialize_games_table()
        u1=games.create_game(game_1)

        all_games = games.get_games()

        self.assertEqual(all_games["result"], "success", "Askings for all games when 1 game exists should return success")
        self.assertEqual(len(all_games["message"]), 1, "The length of the list of games returned by get_games() should be 1")
        self.assertEqual(u1["message"], all_games["message"][0], "Data of returned game should match data of added game")

    def test_12(self):
        """GamesModel: update_game with 1 change, finished is not included"""
        games.initialize_games_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO games VALUES(?, ?, ?, ?, NULL);", games_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()

        new_game = {
            "id":4,
            "name":"princessZ", 
            "link":"4234abcd"
        }

        changed_game = games.update_game(new_game)
        print(changed_game)
        retrieved_used = games.get_game(id=new_game["id"])
        self.assertEqual(changed_game["result"], "success", "updating a game should return success")
        self.assertEqual(changed_game["message"]["name"], new_game["name"], "name of changed game returned by update_game should match data of added game")
        self.assertEqual(changed_game["message"]["link"], new_game["link"], "link of changed game returned by update_game should match data of added game")    
        self.assertEqual(retrieved_used["message"]["name"], new_game["name"], "name of changed game in database should match data of added game")
        self.assertEqual(retrieved_used["message"]["link"], new_game["link"], "link of changed game in database should match data of added game")    
        
    def test_13(self):
        """GamesModel: update_game with multiple changes, including finished"""
        games.initialize_games_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO games VALUES(?, ?, ?, ?, NULL);", games_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()

        new_game = {
            "id":3,
            "name":"princessZ123", 
            "link":"princessZzzzzzz",
            "finished": str(datetime.datetime.now())
        }
        print(new_game)
        changed_game = games.update_game(new_game)
        print(changed_game)
        retrieved = games.get_game(id=new_game["id"])
        print(retrieved)
        self.assertEqual(changed_game["result"], "success", "updating a game should return success")
        self.assertEqual(changed_game["message"]["name"], new_game["name"], "name of changed game returned by update_game should match data of added game")
        self.assertEqual(changed_game["message"]["link"], new_game["link"], "link of changed game returned by update_game should match data of added game")    
        self.assertEqual(changed_game["message"]["finished"], new_game["finished"], "finished of changed game returned by update_game should match data of added game")    
        self.assertEqual(retrieved["message"]["name"], new_game["name"], "name of changed game in database should match data of added game")
        self.assertEqual(retrieved["message"]["link"], new_game["link"], "link of changed game in database should match data of added game")    
        self.assertEqual(retrieved["message"]["finished"], new_game["finished"], "finished of changed game in database should match data of added game")    

    def test_14(self):
        """GamesModel: update_game that doesn't exist"""
        games.initialize_games_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO games VALUES(?, ?, ?, ?, NULL);", games_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()

        new_game = {
            "id":8,
            "name":"asdfasdf@trinityschoolnyc.org", 
            "link":"asdfasdf"
        }

        changed_game = games.update_game(new_game)
        self.assertEqual(changed_game["result"], "error", "updating a game that doesn't exist should return error")

    def test_15(self):
        """GamesModel: delete_game that exists"""
        
        games.initialize_games_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO games VALUES(?, ?, ?, ?, NULL);", games_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()
        
        old_game =games.remove_game(game_4["name"])
        all_games = games.get_games()

        self.assertEqual(all_games["result"], "success", "Removing a game that exists should return success")
        self.assertEqual(len(all_games["message"]), 3, "4 games were added. 1 was deleted. 3 games should be in the database")
        self.assertEqual(old_game["message"]["name"], game_4["name"], "Returned game should include an name")
        self.assertEqual(old_game["message"]["link"], game_4["link"], "Returned game should include an link")
        self.assertIn("id", old_game["message"],  "Returned game should include an id")

    def test_16(self):
        """GamesModel: delete_game that doesn't exist"""
        games.initialize_games_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO games VALUES(?, ?, ?, ?, NULL);", games_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()
        
        old_game=games.remove_game("DonkeyKong")
        print(old_game)
        self.assertEqual(old_game["result"], "error", "Trying to delete a game that doesn't exist should result in an error")

    def test_17(self):

        """TODOGamesModel: is_finished - both finished and unfinished games"""
        
        self.assertEqual(True, False, "This test hasn't been implmented yet")

TestgameModel.test_1