import sqlite3
import random
import string
import datetime



class Game:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "games"
    
    def initialize_games_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    name TEXT UNIQUE,
                    link TEXT UNIQUE,
                    created TIMESTAMP,
                    finished TIMESTAMP
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, name = None, id = None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if id != None:
                query = f'SELECT * from games WHERE id = "{id}";'
            elif name != None:
                query = f'SELECT * from games WHERE name = "{name}";'

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

    def create_game(self, game_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            game_id = random.randint(0, 9223372036854775807) #non-negative range of SQLITE3 INTEGER
            unique = False
            while unique != True:
                if (game_id in cursor.execute("SELECT * FROM games;").fetchall()):
                    game_id = random.randint(0, 9223372036854775807)
                else:
                    unique = True

            dateToday = datetime.datetime.now()
            game_info["created"] = dateToday
            game_info["finished"] = dateToday
            print(dateToday)
            
            if any(string.punctuation[i] in game_info["link"] for i in range(len(game_info["link"]))) or len(game_info["link"]) == 0:
                return {"result":"error",
                    "message": "link uses invalid characters"}
            if any(string.punctuation[i] in game_info["name"] for i in range(len(game_info["name"]))) or len(game_info["name"]) == 0:
                return {"result":"error",
                    "message": "name uses invalid characters"}
            

            user_data = (game_id, game_info["name"], game_info["link"], game_info["created"], game_info["finished"])
            #are you sure you have all data in the correct format?
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?, ?);", user_data)
            db_connection.commit()
            return {"result": "success",
                    "message": {"id": game_id, "name": game_info["name"], "link" : game_info["link"], "created": game_info["created"], "finished": game_info["finished"]}
                    }
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def get_game(self, name = None, id = None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if id != None:
                query = f'SELECT * from games WHERE games.id = {id};'
            elif name != None:
                query = f'SELECT * from games WHERE games.name = "{name}";'

            results = cursor.execute(query)
            game = results.fetchone()
            if game is None:
                return {"result":"error",
                    "message":"game doesnt exist in get game"}
            dictGame = self.to_dict(game)

            return {"result": "success",
                    "message": dictGame
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def get_games(self):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            cursor.execute(f"SELECT * FROM games")

            game_list = cursor.fetchall()
            print(game_list)
            print([self.to_dict(game) for game in game_list])
            return {"result": "success",
                    "message": [self.to_dict(game) for game in game_list]
                    }
            
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def update_game(self, game_info):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            game = self.get_game(id=game_info["id"])

            if game["message"] == "game doesnt exist in get game":
                return {"result": "error",
                        "message": "game doesn't exist in update"}

            # Update the game's details
            query = f"UPDATE {self.table_name} SET name=?, link=?, finished=? WHERE id=?"
            cursor.execute(query, (game_info["name"], game_info["link"], game_info["finished"], game_info["id"]))
            db_connection.commit()

            # Fetch the updated game and return it
            updatedGame = self.get_game(id=game_info["id"])["message"]

            return {"result": "success",
                    "message": updatedGame}

        except sqlite3.Error as error:
            return {"result": "error for update",
                    "message": error}

        finally:
            db_connection.close()

    def remove_game(self, gameName):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            gameDeleted = cursor.execute(f"SELECT * from {self.table_name} WHERE {self.table_name}.name = '{gameName}';").fetchone()
            query = f"DELETE from {self.table_name} WHERE {self.table_name}.name = '{gameName}';"
            if gameDeleted is None:
                return {"result":"error",
                    "message":"Game doesnt exist"}
            dictedGame = self.to_dict(gameDeleted)
            cursor.execute(query)
            db_connection.commit()
            return {"result": "success",
                    "message": dictedGame
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def to_dict(self, game_tuple):
        return{
            "id" : game_tuple[0],
            "name" : game_tuple[1],
            "link" : game_tuple[2],
            "created" : game_tuple[3],
            "finished" : game_tuple[4]
        }
