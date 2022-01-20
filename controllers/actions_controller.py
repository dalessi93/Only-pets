from flask import Blueprint, request, session, redirect, render_template
import bcrypt
from models.user import update_user, update_user_info
from models.posts import select_posts, select_image, img_update, background_update

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
    id = session["user_id"]
    photo_select = select_posts(id)
    return render_template("gallery.html", photo_select=photo_select)

# REDIRECT TO EDIT PROFILE PAGE
@actions_controller.route("/edit_profile")
def edit_profile():
    return render_template("edit_profile.html")

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
    post_id = request.args.get("photo_id")
    photo = select_image(post_id)
    photo_img = photo[0]
    photo_caption = photo[1]
    return render_template("focus_on_photo.html", img_url=photo_img, caption=photo_caption, post_id=post_id)

# BACK BUTTON ON GALLERY PAGE
@actions_controller.route("/redirect/gallery")
def redirect_to_gallery():
    return redirect("/gallery")

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
@actions_controller.route("/set/background_img", method=["POST"])
def insert_img():
    return redirect("/gallery")
