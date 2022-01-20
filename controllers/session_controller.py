from flask import Blueprint, request, session, redirect, render_template
import bcrypt
from models.user import user_signup, select_user

session_controller = Blueprint("session_controller", __name__,)

@session_controller.route("/login")
def login():
    return render_template("login.html")

@session_controller.route("/loggedIn", methods=["POST"])
def logged_in():
    email = request.form.get("email")
    password = request.form.get("password")
    user = select_user(email)
    valid_password = user and bcrypt.checkpw(password.encode(), user['password'].encode())
    if valid_password:
        session["user_id"] = user["id"]
        session["user_name"] = user["first_name"]
        session["user_surname"] = user["last_name"]
        session["user_address"] = user["address"]
        session["user_country"] = user["country"]
        session["user_breed"] = user["breed"]
        session["user_background_img"] = user["background_img"]
        session["user_profile_img"] = user["profile_img"]
        return redirect("/home")
    else:
        return redirect("/")

@session_controller.route("/signup")
def signup():
    return render_template("signup.html")

@session_controller.route("/signup/submission", methods=["POST"])
def signup_submission():
    email = request.form.get("email")
    password = request.form.get("password")
    first_name = request.form.get("first name")
    last_name = request.form.get("surname")
    user_signup(email, password, first_name, last_name)
    return redirect('/')

@session_controller.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")
