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
    
def update_user_info(id):
    results = database.sql_select("SELECT * FROM users WHERE id = %s", [id])
    return results[0]
    
 
def update_user(id, first_name, last_name, address, breed, country):
    database.sql_write("UPDATE users set first_name = %s, last_name = %s, address = %s, breed = %s, country = %s WHERE id = %s", [
        first_name,
        last_name,
        address,
        breed,
        country,
        id
    ])