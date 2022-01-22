from flask import Blueprint, request, session, redirect, render_template
from models.user import update_user, update_user_info
from models.posts import select_posts, select_image, img_update, background_update, upload_new_img, search_user, delete_photo

actions_controller = Blueprint("actions_controller", __name__,)

# RENDER USER INFORMATION ON HOME PAGE
@actions_controller.route("/home")
def home():
    if session.get('user_id'):
        id = session["user_id"]
        user = update_user_info(id)
        session["user_name"] = user["first_name"]
        session["user_surname"] = user["last_name"]
        session["user_address"] = user["address"]
        session["user_country"] = user["country"]
        session["user_breed"] = user["breed"]
        session["user_background_img"] = user["background_img"]
        session["user_profile_img"] = user["profile_img"]
        return render_template("home.html")
    else:
        return redirect("/")

# RENDER ALL IMAGES FROM DB
@actions_controller.route("/gallery")
def gallery():
    if session.get('user_id'):
        id = session["user_id"]
        photo_select = select_posts(id)
        return render_template("gallery.html", photo_select=photo_select)
    else:
        return redirect("/")

# REDIRECT TO EDIT PROFILE PAGE
@actions_controller.route("/edit_profile")
def edit_profile():
    if session.get('user_id'):
        return render_template("edit_profile.html")
    else:
        return redirect("/")

# EDIT PROFILE INFORMATION
@actions_controller.route("/edit_profile/process", methods=["POST"])
def edit_profile_process():
    id = session["user_id"]
    first_name = request.form.get("name")
    last_name = request.form.get("surname")
    address = request.form.get("address")
    breed = request.form.get("breed")
    country =request.form.get("country")
    update_user(id, first_name, last_name, address, breed, country)
    return redirect("/home")

# ZOOM ON INDIVIDUAL IMAGES
@actions_controller.route("/photo")
def focus_photo():
    if session.get('user_id'):
        post_id = request.args.get("photo_id")
        photo = select_image(post_id)
        photo_img = photo[0]
        photo_caption = photo[1]
        return render_template("focus_on_photo.html", img_url=photo_img, caption=photo_caption, post_id=post_id)
    else:
        return redirect("/")

# DELETE PHOTO IN GALLERY
@actions_controller.route("/delete/photo", methods=["GET"])
def delete_user_photo():
    post_id = request.args.get("photo_id")
    delete_photo(post_id)
    return redirect("/gallery")

# BACK BUTTON TO GALLERY PAGE
@actions_controller.route("/redirect/gallery")
def redirect_to_gallery():
    return redirect("/gallery")

# BACK BUTTON TO FRIENDS PAGE
@actions_controller.route("/redirect/friend")
def redirect_to_friends():
    return redirect("/friend/list")

# CHANGE PROFILE IMAGE
@actions_controller.route("/set/profile_img")
def change_profile_img():
    post_id = request.args.get("photo_id")
    new_img = select_image(post_id)
    img_update(new_img[0], session["user_id"])
    return redirect("/home")

# CHANGE BACKGROUND IMAGE
@actions_controller.route("/set/background_img")
def change_background_img():
    post_id = request.args.get("photo_id")
    new_img = select_image(post_id)
    background_update(new_img[0], session["user_id"])
    return redirect("/home")

# INSERT IMAGE (work in progress)
@actions_controller.route("/upload/image", methods=["POST"])
def upload_img():
    id = session["user_id"]
    image_url = request.form.get("image_url")
    caption = request.form.get("caption")
    if image_url[-3] == "jpg" or "png":
        upload_new_img(id, image_url, caption)
        return redirect("/gallery")
    elif image_url[-4] == "jpeg":
        upload_new_img(id, image_url, caption)
        return redirect("/gallery")
    else:
        return redirect("/gallery")

# LOAD FRIEND LIST
@actions_controller.route("/friend/list")
def friends():
    if session.get('user_id'):
        return render_template("my_friends.html")
    else:
        return redirect("/")

# SEARCH FOR FRIEND
@actions_controller.route("/friend/search")
def friend_search():
    if session.get('user_id'):
    #FOR INSTRUCTOR: On 'my_friends.html' i have a Form. How come 'user = request.form.get("name")' does not work?
        user = request.args.get("name")
        show_user = search_user(user)
        return render_template("search_friend.html", show_user=show_user, test=user)
    else:
        return redirect("/")

# VIEW ANOTHER USER PAGE
@actions_controller.route("/user_profile")
def view_page():
    if session.get('user_id'):
        user_id = request.args.get("user_id")
        user_info = update_user_info(user_id)
        return render_template("view_profile.html", user_background=user_info["background_img"], user_profile=user_info["profile_img"], user_name=user_info["first_name"], user_surname=user_info["last_name"], user_address=user_info["address"], user_country=user_info["country"], user_breed=user_info["breed"], user_id=user_info["id"])
    else:
        return redirect("/")

#VIEW ANOTHER USER GALLERY
@actions_controller.route("/view/photos")
def view_photos():
    if session.get('user_id'):
        user_id = request.args.get("user_id")
        posts_info = select_posts(user_id)
        return render_template("view_friend_photos.html", posts_info=posts_info)
    else:
        return redirect("/")

@actions_controller.route("/friend/photo")
def focus_friend_photo():
    if session.get('user_id'):
        post_id = request.args.get("photo_id")
        photo = select_image(post_id)
        photo_img = photo[0]
        photo_caption = photo[1]
        return render_template("focus_friend_photo.html", img_url=photo_img, caption=photo_caption, post_id=post_id)
    else:
        return redirect("/")