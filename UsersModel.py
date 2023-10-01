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
                    id INTEGER PRIMARY KEY,
                    email TEXT UNIQUE,
                    username TEXT UNIQUE,
                    password TEXT UNIQUE
                ) WITHOUT ROWID;
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, username = None, id = None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            query = f"SELECT * from {self.table_name} WHERE {self.table_name}.id = {user_id};"
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
                return "email already exists"   
            if "@" not in user_details["email"]:
                return "need an @ symbol"
            if "." not in user_details["email"].split("@")[1]:
                return "need a valid domain"
            if (user_details["username"] in cursor.execute("SELECT * FROM users;").fetchall()):
                return "username already exists"
            
            passwordTemp = str(user_details["password"])
            goodPassword = "none"

            if len(passwordTemp) >= 8:
                if any(char.isdigit() for char in passwordTemp):
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
            print(user_details)
            print(user_data)
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
            print("what then")
            db_connection.commit()
            return {"result": "success",
                    "message": user_data
                    }
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def get_user(self, user_id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            query = f"SELECT * from {self.table_name} WHERE {self.table_name}.id = {user_id};"
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
            db_connection = sqlite3.connect("users")
            cursor = db_connection.cursor()

            query = f"SELECT * FROM users;"
            print(query)
            results = cursor.execute(query)
            db_connection.commit()
            return {"result": "success",
                    "message": results.fetchall()
                    }
            
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def update_user(self, user_details):
        try: 
            db_connection = sqlite3.connect("users")
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
            db_connection = sqlite3.connect("users")
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