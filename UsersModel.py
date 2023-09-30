import sqlite3
import random
import string

def check_email(new_email):
    return new_email
def check_password(new_password):
    return new_password
def check_email(new_email):
    return new_email
print("wow")

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
                    email TEXT,
                    username TEXT,
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
            
            passwordTemp = user_details["password"]
            goodPassword = "none"

            if len(passwordTemp) >= 8:
                if string.digits in passwordTemp:
                    if string.ascii_letters.upper() in passwordTemp:
                        if string.ascii_letters.lower() in passwordTemp:
                            goodPassword = passwordTemp
                        else:
                            return "must have one lowercase letter at least"
                    else:
                        return "must have one uppercase letter at least"
                else:
                    return "must have at least 1 #"
            else:
                return "must be 8 chars at least"

            user_data = (user_id, user_details["email"], user_details["username"], goodPassword)
            #are you sure you have all data in the correct format?

            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
            db_connection.commit()
            return {"result": "success",
                    "message": user_id
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