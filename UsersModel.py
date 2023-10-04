import sqlite3
import random
import string

def check_email(new_email):
    return new_email
def check_password(new_password):
    return new_password
def check_email(new_email):
    return new_email

class User:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "users"
    
    def initialize_users_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    email TEXT UNIQUE,
                    username TEXT UNIQUE,
                    password TEXT
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

    def create_user(self, user_details):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            user_id = random.randint(0, 9223372036854775807) #non-negative range of SQLITE3 INTEGER
            unique = False
            while unique != True:
                if (user_id in cursor.execute("SELECT * FROM users;").fetchall()):
                    user_id = random.randint(0, 9223372036854775807)
                else:
                    unique = True
            
            if user_details["email"] in cursor.execute("SELECT * FROM users;").fetchall():
                print("email already exists")
                return {"result":"error",
                    "message":"email already exists"}
            if "@" not in user_details["email"]:
                print
                print("need an @ symbol")
                return {"result":"error",
                    "message":"need an @ symbol"}
            print('here?')
            if "." not in user_details["email"].split("@")[1]:
                print("need a valid domain")
                return {"result":"error",
                    "message":"need a valid domain"}
            if (user_details["username"] in cursor.execute("SELECT * FROM users;").fetchall()):
                print("username already exists")
                return {"result":"error",
                    "message": "username already exists"}
            print("yo?")
            passwordTemp = str(user_details["password"])
            goodPassword = "none"

            if len(passwordTemp) >= 8:
                print("and here?")
                if any(char.isdigit() for char in passwordTemp):
                    print("here?")
                    passwordTemp2 = "".join(filter(str.isalpha,passwordTemp))
                    if passwordTemp2.islower() == False or passwordTemp2.isupper() == False:
                        print("e")
                        goodPassword = passwordTemp
                    else:
                        print("tough e")
                        return {"result":"error",
                    "message": "must have one uppercase and one lowercase"}
                else:
                    return {"result":"error",
                    "message": "must have at least 1 #"}
            else:
                return {"result":"error",
                    "message": "must be 8 chars at least"}
            
            new_email = user_details["email"]
            new_username = user_details["username"]

            user_data = (user_id, new_email, new_username, goodPassword)
            #are you sure you have all data in the correct format?
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
            db_connection.commit()
            return {"result": "success",
                    "message": {"id": user_id, "email": user_details["email"], "username" : user_details["username"], "password": user_details["password"]}
                    }
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def get_user(self, username = None, id = None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if id != None:
                query = f'SELECT * from users WHERE users.id = {id};'
            elif username != None:
                query = f'SELECT * from users WHERE users.username = "{username}";'

            results = cursor.execute(query)
            user = results.fetchone()
            if user is None:
                print("User doesnt exist")
                return {"result":"error",
                    "message":"User doesnt exist"}
            dictUser = self.dict_transformer(user)

            return {"result": "success",
                    "message": dictUser
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def get_users(self):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            cursor.execute(f"SELECT * FROM {self.table_name}")

            user_list = cursor.fetchall()

            return {"result": "success",
                    "message": [self.dict_transformer(user) for user in user_list]
                    }
            
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def update_user(self, user_details):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            user = self.get_user(id = user_details["id"]) # already in dictionary format
            
            if user["message"] == "User doesnt exist":
                return {"result":"error",
                    "message":"User doesn't exist"}
                
            newUser = user["message"]
            print("before updating: " , user["message"])

            newUser["email"] = user_details["email"]
            newUser["username"] = user_details["username"]
            newUser["password"] = user_details["password"]
            print("after updating: " , newUser)
            finalUser = newUser
            db_connection.commit()
            return {"result": "success",
                    "message": finalUser
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def remove_user(self, user_id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            userDeleted = cursor.execute(f"SELECT * from {self.table_name} WHERE {self.table_name}.username = '{user_id}';").fetchone()
            query = f"DELETE from {self.table_name} WHERE {self.table_name}.username = '{user_id}';"
            print(userDeleted)
            if userDeleted is None:
                print("User doesnt exist")
                return {"result":"error",
                    "message":"User doesnt exist"}
            dictedUser = self.dict_transformer(userDeleted)
            cursor.execute(query)
            db_connection.commit()
            return {"result": "success",
                    "message": dictedUser
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def dict_transformer(self, user_tuple):
        return{
            "id" : user_tuple[0],
            "email" : user_tuple[1],
            "username" : user_tuple[2],
            "password" : user_tuple[3]
        }
