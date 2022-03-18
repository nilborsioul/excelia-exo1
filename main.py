from bottle import route, run, template, request, response, redirect
import sqlite3
from helpers import addition, generate_cookie_value
import sys


@route("/addition/<a>/<b>")
@route("/addition/<a>/<b>/")
def routeaddition(a, b):
    return addition(a, b)


@route("/user")
@route("/user/")
def user_info():
    fb_session = request.get_cookie('fb_session')

    conn = sqlite3.connect('fb.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM facebook WHERE cookie = '{fb_session}'")
    result = cursor.fetchone()

    if result is None:
        redirect("/login")

    return template('user_info', username=result[1], email=result[2])


@route("/login", method=["GET", "POST"])
@route("/login/", method=["GET", "POST"])
def login():
    if request.method == 'GET':
        return template("login_template")
    else:
        username = request.forms.username
        password = request.forms.password

        conn = sqlite3.connect('fb.db')
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT password FROM facebook WHERE username = '{username}' "
        )
        db_password = cursor.fetchone()
        print(db_password)
        if db_password[0] == "":
            return {"error": True, "message": "Utilisateur inconnu"}

        if db_password[0] != password:
            return {"error": True, "message": "Mot de passe érroné"}

        cookie_value = generate_cookie_value()

        cursor.execute(
            f"UPDATE facebook SET cookie = '{cookie_value}' WHERE username = '{username}'"
        )
        conn.commit()

        response.set_cookie("fb_session", cookie_value, path="/")
        redirect("/user/")

@route("/signup", method=["GET", "POST"])
@route("/signup/", method=["GET", "POST"])
def signup():
    if request.method == "GET":
        return template("signup_template")
    else:
        username = request.forms.username
        email = request.forms.email
        password = request.forms.password
        print(username)
        print(email)
        print(password)
        conn = sqlite3.connect("fb.db")
        cursor = conn.cursor()
        sql_request = f"INSERT INTO facebook (username, email, password) VALUES ('{username}','{email}','{password}')"
        print(sql_request)
        cursor.execute(sql_request)
        conn.commit()
        return {
            "error": False,
            "message": f"Bien enregistre en tant que {username} id: {cursor.lastrowid}",
        }


run(host='0.0.0.0', port=sys.argv[1], reloader=True)
