#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage
from html import escape
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db

form_data = FieldStorage()
username = ""
result = ""
if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    password1 = escape(form_data.getfirst('password1', '').strip())
    password2 = escape(form_data.getfirst('password2', '').strip())
    if not username or not password1 or not password2:
        result = "<p>Error: user name and passwords are required</p>"
    elif password1 != password2:
        result = "<p>Error: passwords must be equal</p>"
    else:
        try:
            connection = db.connect('localhost', 'username', 'password', 'database_name')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users
                              WHERE username = %s""", (username))
            if cursor.rowcount > 0:
                result = "<p>Error: user name already taken</p>"
            else:
                sha256_password = sha256(password1.encode()).hexdigest()
                cursor.execute("""INSERT INTO users (username, password)
                                  VALUES (%s, %s)""", (username, sha256_password))
                connection.commit()
                cursor.execute("""SELECT * FROM users
                                  WHERE username = %s""", (username))
                returned_results = cursor.fetchone()
                user_id = returned_results["user_id"]
                cursor.close()
                connection.close()
                cookie = SimpleCookie()
                sid = sha256(repr(time()).encode()).hexdigest()
                cookie["user_id"] = user_id
                cookie["sid"] = sid
                session_store = open("sess_" + sid, writeback=True)
                session_store["authenticated"] = True
                session_store["username"] = username
                session_store.close()
                result = """
                   <h1>Succesfully registered!</h1>
                   <ul>
                       <li><a href="getstarted.py">Get started on your learning journey</a></li>
                       <li><a href="profile.py">Check out your user profile</a></li>
                   </ul>"""
                print(cookie)
        except (db.Error):
            result = "<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>"

print("Content-Type: text/html")
print()
print("""
    <!DOCTYPE html>
    <html class="form_page" lang="en">
        <head>
            <title>New User</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
		    <link rel="icon" type="image/png" href="icons/favicon/favicon.png"  />
		    <link rel="stylesheet" href="style.css"  />
        </head>
        <body>
            <main>
                <section>
                    <form action="register.py" method="post">
                        <label for="username">User name: </label>
                        <input type="text" name="username" id="username" value="%s" />
                        <label for="password1">Password: </label>
                        <input type="password" name="password1" id="password1" />
                        <label for="passwords2">Re-enter password: </label>
                        <input type="password" name="password2" id="password2" />
                        <input type="submit" value="Register" />
                        %s
                    </form>
                </section>
            </main>
        </body>
    </html>""" % (username, result))
