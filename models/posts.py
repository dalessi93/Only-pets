import database

def select_posts(id):
    results = database.sql_select("SELECT post_id, user_id, image, post FROM posts JOIN users ON users.id = posts.user_id WHERE id = %s order by post_id desc", [id])
    return results

# SELECT IMAGE
def select_image(post_id):
    results = database.sql_select("SELECT image, post FROM posts WHERE post_id = %s", [post_id])
    return results[0]

# UPDATE PROFILE IMAGE
def img_update(new_img, id):
    database.sql_write("UPDATE users SET profile_img = %s WHERE id = %s", [new_img, id])

# UPDATE BACKGROUND IMAGE
def background_update(new_img, id):
    database.sql_write("UPDATE users SET background_img = %s WHERE id = %s", [new_img, id])

# UPLOAD NEW IMAGE
def upload_new_img(user_id, image, post):
    database.sql_write("INSERT INTO posts (user_id, image, post) VALUES (%s, %s, %s)", [user_id, image, post])

# SEARCH FRIEND
def search_user(name):
    # Why "SELECT * FROM users WHERE first_name LIKE CONCAT(%, %s, %), [name]" does not work? Also, LIKE case insensitive property not working.
    results = database.sql_select("SELECT * FROM users WHERE first_name LIKE %s", [name])
    return results