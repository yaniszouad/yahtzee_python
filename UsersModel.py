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
    
    def exists(self, username = "", id = ""):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if id != "":
                query = f'SELECT * from users WHERE id = "{id}";'
            elif username != "":
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
                return "email already exists"   
            if "@" not in user_details["email"]:
                print("need an @ symbol")
                return "need an @ symbol"
            if "." not in user_details["email"].split("@")[1]:
                print("need a valid domain")
                return "need a valid domain"
            if (user_details["username"] in cursor.execute("SELECT * FROM users;").fetchall()):
                print("username already exists")
                return "username already exists"
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
                        return "must have one uppercase and one lowercase"
                else:
                    return "must have at least 1 #"
            else:
                return "must be 8 chars at least"
            
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
    
    def get_user(self, username = None, user_id = None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if user_id != None:
                query = f"SELECT * from {self.table_name} WHERE {self.table_name}.id = {user_id};"
            else:
                query = f"SELECT * from {self.table_name} WHERE {self.table_name}.username = {username};"
            print(query)
            results = cursor.execute(query)
            db_connection.commit()
            return {"result": "success",
                    "message": results.fetchone()
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
                    "message": [self.to_dict(user) for user in user_list]
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

            query = f"SELECT * from {self.table_name} WHERE {self.table_name}.id = {user_details.emails};"
            print(query)
            results = cursor.execute(query)
            db_connection.commit()
            return {"result": "success",
                    "message": results.fetchone()
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

            query = f"DELETE * from {self.table_name} WHERE {self.table_name}.id = {user_id};"
            print(query)
            results = cursor.execute(query)
            db_connection.commit()
            return {"result": "success",
                    "message": "it's deleted"
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def to_dict(self, user_tuple):
        return{
            "id" : user_tuple[0],
            "email" : user_tuple[1],
            "username" : user_tuple[2],
            "password" : user_tuple[3]
        }