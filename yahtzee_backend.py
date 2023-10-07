import unittest
import sqlite3
import os

from UsersModel import User

yahtzee_db_name=f"{os.getcwd()}/yahtzeeDB.db"
table_name = "users"

users = User(yahtzee_db_name)

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
users_data = [
    (1, "cookie.monster@trinityschoolnyc.org", "cookieM", "123TriniT"),
    (2, "justin.gohde@trinityschoolnyc.org", "justingohde", "123TriniT"),
    (3, "zelda@trinityschoolnyc.org", "princessZ", "123TriniT"),
    (4, "test.user@trinityschoolnyc.org", "testuser", "123TriniT")
]

class TestUserModel(unittest.TestCase):
    def test_1(self):
        """UsersModel: create_user w/ 1 user"""
        users.initialize_users_table()
        results = users.create_user(user_1)
        self.assertEqual(results["result"], "success", "Creating a user should return success")
        self.assertEqual(results["message"]["email"], "cookie.monster@trinityschoolnyc.org", "Data of returned user should match data of added user")
        self.assertEqual(results["message"]["username"], "cookieM", "Data of returned user should match data of added user")    
        self.assertEqual(results["message"]["password"], "123TriniT", "Data of returned user should match data of added user")

        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {table_name};"
            results = cursor.execute(query)
            all_users = []
            for user in results.fetchall():
                all_users.append(user)
            self.assertEqual(len(all_users), 1, "Creating a single user should result in a table with 1 user")
            self.assertEqual(all_users[0][1], "cookie.monster@trinityschoolnyc.org", "Data of returned user should match data of added user")
            self.assertEqual(all_users[0][2], "cookieM", "Data of returned user should match data of added user")    
            self.assertEqual(all_users[0][3], "123TriniT", "Data of returned user should match data of added user")
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()

    def test_2(self):
        """UsersModel: create_user w/ 4 users"""
        users.initialize_users_table()
        users.create_user(user_1)
        users.create_user(user_2)
        users.create_user(user_3)
        users.create_user(user_4)
        
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {table_name} ORDER BY username;"
            results = cursor.execute(query)
            all_users = []
            for user in results.fetchall():
                all_users.append(user)
            self.assertEqual(len(all_users), 4, "Creating 4 users should result in a table with 4 users")
            self.assertEqual(all_users[0][1], "cookie.monster@trinityschoolnyc.org", "Data of returned user should match data of added user")
            self.assertEqual(all_users[1][1], "justin.gohde@trinityschoolnyc.org", "Data of returned user should match data of added user")
            self.assertEqual(all_users[2][2], "princessZ", "Data of returned user should match data of added user")
            self.assertEqual(all_users[3][2], "testuser", "Data of returned user should match data of added user")    
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()

    def test_3(self):
        """UsersModel: create_user w/ already taken username or email"""
        users.initialize_users_table()
        results = users.create_user(user_1)
        user_1_username={
            "email":"cookie.monster2@trinityschoolnyc.org",
            "username":"cookieM",
            "password":"123TriniT"
        }
        results = users.create_user(user_1_username)
        self.assertEqual(results["result"], "error", "Creating a user with the same username should result in an error")

        user_1_email={
            "email":"cookie.monster@trinityschoolnyc.org",
            "username":"cookieM2",
            "password":"123TriniT"
        }
        results = users.create_user(user_1_email)
        self.assertEqual(results["result"], "error", "Creating a user with the same email should result in an error")

    def test_4(self):
        """UsersModel: create_user w/ data in incorrect format"""
        users.initialize_users_table()
        user_incorrect_email_1={
            "email":"test.usertrinityschoolnyc.org",
            "username":"testuser",
            "password":"123TriniT"
        }
        results = users.create_user(user_incorrect_email_1)
        self.assertEqual(results["result"], "error", "Creating a user with incorrect email (no @) should return error")
        
        user_incorrect_email_2={
            "email":"test.user@trinityschoolnycorg",
            "username":"testuser",
            "password":"123TriniT"
        }
        results = users.create_user(user_incorrect_email_2)
        self.assertEqual(results["result"], "error", "Creating a user with incorrect email (no . three letters from the end of the email) should return error")
        
        user_incorrect_username_bad_characters={
            "email":"test.user@trinityschoolnyc.org",
            "username":"test@!user",
            "password":"123TriniT"
        }
        results = users.create_user(user_incorrect_username_bad_characters)
        self.assertEqual(results["result"], "error", "Creating a user with incorrect username (includes special characters) should return error")
        
        user_incorrect_password_fewer_than_8={
            "email":"test.user@trinityschoolnyc.org",
            "username":"test@!user",
            "password":"123Tr"
        }
        results = users.create_user(user_incorrect_password_fewer_than_8)
        self.assertEqual(results["result"], "error", "Creating a user with incorrect password (fewer than 8 characters) should return error")
        
        user_incorrect_password_all_lower={
            "email":"test.user@trinityschoolnyc.org",
            "username":"test@!user",
            "password":"asdfasdfasdfas"
        }
        results = users.create_user(user_incorrect_password_all_lower)
        self.assertEqual(results["result"], "error", "Creating a user with incorrect password (all lowercase) should return error")
    
        user_incorrect_password_all_upper={
            "email":"test.user@trinityschoolnyc.org",
            "username":"test@!user",
            "password":"ASDFGASDFASDF"
        }
        results = users.create_user(user_incorrect_password_all_upper)
        self.assertEqual(results["result"], "error", "Creating a user with incorrect password (all uppercase) should return error")
    
        user_incorrect_password_no_numbers={
            "email":"test.user@trinityschoolnyc.org",
            "username":"test@!user",
            "password":"ASDFsdfasdfSDF"
        }
        results = users.create_user(user_incorrect_password_no_numbers)
        self.assertEqual(results["result"], "error", "Creating a user with incorrect password (no numbers) should return error")
    
    def test_5(self):
        """UsersModel: exists w/ username and id"""
        users.initialize_users_table()
        u1=users.create_user(user_1)
        u2=users.create_user(user_2)
        u3=users.create_user(user_3)
        
        result_username = users.exists(username="princessZ")
        self.assertEqual(result_username["result"], "success", "Should return success")
        self.assertEqual(result_username["message"], True, "username that exists should return True")

        result_id = users.exists(id=u2["message"]["id"])
        self.assertEqual(result_id["result"], "success", "Should return success")
        self.assertEqual(result_id["message"], True, "id that exists should return True")
    
    def test_6(self):
        """UsersModel: doesn't exist w/ username and id"""
        users.initialize_users_table()
        u1=users.create_user(user_1)
        u2=users.create_user(user_2)
        u3=users.create_user(user_3)
        
        result_username = users.exists(username="princessZZZZZZZ")
        self.assertEqual(result_username["result"], "success", "Should return success for username that doesn't exist")
        self.assertEqual(result_username["message"], False, "username that exists should return False")

        result_id = users.exists(id=-1234567890)
        self.assertEqual(result_id["result"], "success", "Should return success for id that doesn't exist")
        self.assertEqual(result_id["message"], False, "id that exists should return False")
    
    def test_7(self):
        """UsersModel: get_user that exists w/ username and id"""
        users.initialize_users_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO users VALUES(?, ?, ?, ?);", users_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()
        
        user = users.get_user(username=user_4["username"])
        self.assertEqual(user["result"], "success", "getting an existing user by username should return success")
        self.assertEqual(user["message"]["email"], user_4["email"], "Data should match - email")
        self.assertEqual(user["message"]["username"], user_4["username"], "Data should match - username")
        self.assertEqual(user["message"]["password"], user_4["password"], "Data should match -password")

        user = users.get_user(id=3)
        self.assertEqual(user["result"], "success", "getting an existing user by id should return success")
        self.assertEqual(user["message"]["email"], user_3["email"], "Data should match - email")
        self.assertEqual(user["message"]["username"], user_3["username"], "Data should match - username")
        self.assertEqual(user["message"]["password"], user_3["password"], "Data should match  password")
    
    def test_8(self):
        """UsersModel: get_user that doesn't exist w/ username and id"""
        users.initialize_users_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO users VALUES(?, ?, ?, ?);", users_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()
        
        user = users.get_user(username="something")
        self.assertEqual(user["result"], "error", "getting a user that does't exist by username should return error")
  
        user = users.get_user(id=175)
        self.assertEqual(user["result"], "error", "getting a user that does't exist by id should return error")
 
    def test_9(self):
        """UsersModel: get_users with multiple users"""
        users.initialize_users_table()
        u1=users.create_user(user_1)
        u2=users.create_user(user_2)
        u3=users.create_user(user_3)

        all_users = users.get_users()
        
        self.assertEqual(all_users["result"], "success", "Askings for all users when 3 users exists should return success")
        self.assertEqual(len(all_users["message"]), 3, "The length of the list of users returned by get_users() should be 3")
        self.assertIn(u1["message"], all_users["message"], "Data of returned user should match data of added user")
        self.assertIn(u2["message"], all_users["message"], "Data of returned user should match data of added user")
        self.assertIn(u3["message"], all_users["message"], "Data of returned user should match data of added user")

    def test_10(self):
        """UsersModel: get_users with no users"""
        users.initialize_users_table()
        all_users = users.get_users()

        self.assertEqual(all_users["result"], "success", "Askings for all users when no users exists should return success")
        self.assertEqual(len(all_users["message"]), 0, "The length of an empty list should be 0")

    def test_11(self):
        """UsersModel: get_users with 1 user"""
        users.initialize_users_table()
        u1=users.create_user(user_1)

        all_users = users.get_users()

        self.assertEqual(all_users["result"], "success", "Askings for all users when 1 user exists should return success")
        self.assertEqual(len(all_users["message"]), 1, "The length of the list of users returned by get_users() should be 1")
        self.assertEqual(u1["message"], all_users["message"][0], "Data of returned user should match data of added user")

    def test_12(self):
        """UsersModel: update_user with 1 change"""
        users.initialize_users_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO users VALUES(?, ?, ?, ?);", users_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()

        new_user = {
            "id":3,
            "email":"princessZ@trinityschoolnyc.org", 
            "username":"princessZ", 
            "password":"123TriniT"
        }

        changed_user = users.update_user(new_user)
        retrieved_used = users.get_user(id=new_user["id"])
        self.assertEqual(changed_user["result"], "success", "updating a user should return success")
        self.assertEqual(changed_user["message"]["email"], new_user["email"], "email of changed user returned by update_user should match data of added user")
        self.assertEqual(changed_user["message"]["username"], new_user["username"], "username of changed user returned by update_user should match data of added user")    
        self.assertEqual(changed_user["message"]["password"], new_user["password"], "password of changed user returned by update_user should match data of added user")
        self.assertEqual(retrieved_used["message"]["email"], new_user["email"], "email of changed user in database should match data of added user")
        self.assertEqual(retrieved_used["message"]["username"], new_user["username"], "username of changed user in database should match data of added user")    
        self.assertEqual(retrieved_used["message"]["password"], new_user["password"], "password of changed user in database should match data of added user")
        
    def test_13(self):
        """UsersModel: update_user with multiple changes"""
        users.initialize_users_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO users VALUES(?, ?, ?, ?);", users_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()

        new_user = {
            "id":3,
            "email":"princessZ@trinityschoolnyc.org", 
            "username":"princessZzzzzzz", 
            "password":"123TriniTy"
        }

        changed_user = users.update_user(new_user)
        retrieved_used = users.get_user(id=new_user["id"])
        self.assertEqual(changed_user["result"], "success", "updating a user should return success")
        self.assertEqual(changed_user["message"]["email"], new_user["email"], "email of changed user returned by update_user should match data of added user")
        self.assertEqual(changed_user["message"]["username"], new_user["username"], "username of changed user returned by update_user should match data of added user")    
        self.assertEqual(changed_user["message"]["password"], new_user["password"], "password of changed user returned by update_user should match data of added user")
        self.assertEqual(retrieved_used["message"]["email"], new_user["email"], "email of changed user in database should match data of added user")
        self.assertEqual(retrieved_used["message"]["username"], new_user["username"], "username of changed user in database should match data of added user")    
        self.assertEqual(retrieved_used["message"]["password"], new_user["password"], "password of changed user in database should match data of added user")
        
    def test_14(self):
        """UsersModel: update_user that doesn't exist"""
        users.initialize_users_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO users VALUES(?, ?, ?, ?);", users_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()

        new_user = {
            "id":8,
            "email":"asdfasdf@trinityschoolnyc.org", 
            "username":"asdfasdf", 
            "password":"123Trasdfasdf"
        }

        changed_user = users.update_user(new_user)
        self.assertEqual(changed_user["result"], "error", "updating a user that doesn't exist should return error")

    def test_15(self):
        """UsersModel: delete_user that exists"""
        
        users.initialize_users_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO users VALUES(?, ?, ?, ?);", users_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()
        
        old_user =users.remove_user(user_4["username"])
        all_users = users.get_users()

        self.assertEqual(all_users["result"], "success", "Removing a user that exists should return success")
        self.assertEqual(len(all_users["message"]), 3, "4 users were added. 1 was deleted. 3 users should be in the database")
        self.assertEqual(old_user["message"]["email"], user_4["email"], "Returned user should include an email")
        self.assertEqual(old_user["message"]["username"], user_4["username"], "Returned user should include an username")
        self.assertEqual(old_user["message"]["password"], user_4["password"], "Returned user should include an password")
        self.assertIn("id", old_user["message"],  "Returned user should include an id")

    def test_16(self):
        """UsersModel: delete_user that doesn't exist"""
        users.initialize_users_table()
        try: 
            db_connection = sqlite3.connect(yahtzee_db_name)
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO users VALUES(?, ?, ?, ?);", users_data)
            db_connection.commit()
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        finally:
            db_connection.close()
        
        old_user=users.remove_user("DonkeyKong")
        print(old_user)
        self.assertEqual(old_user["result"], "error", "Trying to delete a user that doesn't exist should result in an error")

TestUserModel().test_4()