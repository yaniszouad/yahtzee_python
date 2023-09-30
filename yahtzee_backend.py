import os
from UsersModel import User 

print(os.getcwd())
yahtzee_db_name=f"{os.getcwd()}\\class_models\\yahtzeeDB.db"

users = User(yahtzee_db_name)

users.initialize_users_table()
user_details={
    "email":"justin.gohde@trinityschoolnyc.org",
    "username":"justingohde",
    "password":"123TriniT"
}
results = users.create_user(user_details)
print(results)
user_id=results["message"]
results = users.get_users()
print(results)