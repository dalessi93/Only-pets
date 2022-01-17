import database
import bcrypt

def user_signup(email, password, first_name, last_name):
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    database.sql_write("INSERT into users (email, password, first_name, last_name) VALUES (%s, %s, %s, %s);", [email, password, first_name, last_name])

def select_user(email):
    results = database.sql_select("SELECT * FROM users WHERE email = %s", [email])
    if len(results) > 0:
        return results[0]
    else:
        return None
