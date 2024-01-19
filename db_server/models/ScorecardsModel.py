
import sqlite3
import random
import json

class Scorecard:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "scorecards"
    
    def initialize_scorecards_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    game_id INTEGER,
                    user_id INTEGER,
                    score_info TEXT,
                    turn_order INTEGER,
                    score INTEGER
                ) WITHOUT ROWID;
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, username = None, id = None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if id != None:
                query = f'SELECT * from users WHERE id = "{id}";'
            elif username != None:
                query = f'SELECT * from users WHERE username = "{username}";'

            result = cursor.execute(query)
            needThat = result.fetchone()

            if needThat is None:
                return {"result": "success",
                        "message": False}
            else:
                return {"result": "success",
                        "message": True}

        
        except sqlite3.Error as error:
            return {"result":"success",
                    "message":error}
        
        finally:
            db_connection.close()

    def create_scorecard(self, game_id, user_id, turn_order):
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            scorecard_id = random.randint(0, 9007199254740991) #non-negative range of SQLITE3 INTEGER
            unique = False
            while unique != True:
                if (scorecard_id in cursor.execute("SELECT * FROM scorecards;").fetchall()):
                    scorecard_id = random.randint(0, 9007199254740991)
                else:
                    unique = True

            score_info_dict = self.create_blank_card()
            score_info = json.dumps(score_info_dict)

            results = cursor.execute(f"SELECT * FROM scorecards WHERE user_id = {user_id};").fetchall()
            if results != []:
                if results[0][1] == game_id:
                    return {"result": "error", "message": "User already has a scorecard for this game."}


            results = cursor.execute(f"SELECT COUNT(*) FROM scorecards WHERE game_id = {game_id};")
            if results.fetchone()[0] >= 4:
                return {"result": "error", "message": "Game already has four scorecards."}
            
            cursor.execute("INSERT INTO scorecards (id, game_id, user_id, score_info, turn_order, score) VALUES (?, ?, ?, ?, ?, ?);", (scorecard_id, game_id, user_id, score_info, turn_order, 0))
            connection.commit()
            
            new_scorecard = cursor.execute(f"SELECT * FROM scorecards WHERE id = {scorecard_id};").fetchone()
            dicted_scorecard = self.dict_transformer(new_scorecard)
            return {"result": "success", 
                    "message": dicted_scorecard}
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            connection.close()
    
    def get_scorecard(self, id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            results = cursor.execute(f'SELECT * from scorecards WHERE id = {id};')
            scorecard = results.fetchone()

            if scorecard is None:
                return {"result":"error",
                    "message":"Scorecard doesnt exist in get scorecard"}
            
            dictScorecard = self.dict_transformer(scorecard)

            return {"result": "success",
                    "message": dictScorecard
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def get_scorecards(self):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            cursor.execute(f"SELECT * FROM {self.table_name}")

            scorecard_list = cursor.fetchall()

            return {"result": "success",
                    "message": [self.dict_transformer(scorecard) for scorecard in scorecard_list]
                    }
            
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def get_game_scorecards(self, game_id):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            cursor.execute(f"SELECT * FROM {self.table_name} WHERE game_id = {game_id};")
            scorecard_list = cursor.fetchall()
            return {"result": "success", 
                    "message": [self.dict_transformer(scorecard) for scorecard in scorecard_list]}
        
        except sqlite3.Error as error:
            return {"result": "error", 
                    "message": error}
        finally:
            db_connection.close()

    def update_scorecard(self, id, score_info):
        try:
            score = self.tally_score(score_info)
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            score_info_str = json.dumps(score_info)  
            query = f"UPDATE {self.table_name} SET score_info=?, score=? WHERE id=?"
            cursor.execute(query, (score_info_str, score, id))
            if cursor.rowcount == 0:
                return {"result": "error", 
                        "message": "scorecard does not exist"}      
            db_connection.commit()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id={id}")
            updated_scorecard = cursor.fetchone()

            if updated_scorecard is None:
                return {"result": "error", 
                        "message": "Scorecard does not exist"}
            return {"result": "success", 
                    "message": self.dict_transformer(updated_scorecard)}
                
        except sqlite3.Error as error:
            return {"result": "error", 
                    "message": error}
            
        finally:
            db_connection.close()

    def remove_scorecard(self, id):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = {id};")
            game = cursor.fetchone()
            if game is None:
                return {"result":"error", 
                        "message": "Scorecard does not exist"}
                
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id = {id};")
            db_connection.commit()

            return {"result": "success", 
                    "message": "Scorecard has been deleted"}
        
        except sqlite3.Error as error:
            return {"result": "error", 
                    "message": error}
        
        finally:
            db_connection.close()

    def dict_transformer(self, user_tuple):
        return{
            "id" : user_tuple[0],
            "game_id" : user_tuple[1],
            "user_id" : user_tuple[2],
            "score_info" : json.loads(user_tuple[3]),
            "turn_order" : user_tuple[4],
            "score" : user_tuple[5]
        }

    def create_blank_card(self):
        return {
            'dice_rolls': 0,
            'upper': {
                'ones': -1,
                'twos': -1,
                'threes': -1,
                'fours': -1,
                'fives': -1,
                'sixes': -1
            },
            'lower': {
                'three_of_a_kind': -1,
                'four_of_a_kind': -1,
                'full_house': -1,
                'small_straight': -1,
                'large_straight': -1,
                'yahtzee': -1,
                'chance': -1
            }
        }

    def tally_score(self, score_info):
        total_score = 0
        for category, scores in score_info.items():
            if isinstance(scores, dict):
                allscores = []
                for score in scores.values():
                    if score != -1:
                        allscores.append(score)
                total_score += sum(allscores)
                        
        return total_score
