from flask import Flask, render_template, request
from functions import *
import re

app = Flask(__name__)


# user routes:
@app.route("/")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/forgot-password")
def forgot():
    return render_template("forgot-password.html")


# Backend routes:


@app.route("/login-check", methods=["POST"])
def get_user(user_detail, password, POW, captcha):

    if len(captcha) < 10:
        return {"success": False, "message": "Captcha is missing"}

    ip_address = request.remote_addr

    if not check_captcha(captcha, ip_address):
        return {"success": False, "message": "Captcha is invaild"}

    if "@" in user_detail:
        query = {"email": f"{user_detail}"}
    else:
        query = {"username": f"{user_detail}"}

    exist = search(query)

    if exist == None:
        return {"success": False, "message": "username/email doesn't match"}

    if exist.password != password:
        return {"success": False, "message": "password doesn't match"}

    return {"success": True, "message": "login successfull"}


@app.route("/check-userinfo")
def check(email, username):
    if len(email) > 10:
        email_pattern = r"^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$"

        if not re.match(email_pattern, email):
            return {"success": False, "message": "invalid email"}

        query = {"email": f"{email}"}
        exist = search(query)

        if exist != None:
            return {"success": False, "message": "email already exists"}

    if len(username) > 2:
        usr_pattern = r"^[a-zA-Z][a-zA-Z0-9]*(_[a-zA-Z0-9]+)?$"

        if not re.match(usr_pattern, username):
            return {"success": False, "message": "invalid username"}

        query = {"username": f"{username}"}
        exist = search(query)

        if exist != None:
            return {"success": False, "message": "Username already exists"}


if __name__ == "__main__":
    app.run(debug=True)
