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
username = ''
result = ''
if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    password = escape(form_data.getfirst('password', '').strip())
    if not username or not password:
        result = '<p>Error: user name and password are required</p>'
    else:
        sha256_password = sha256(password.encode()).hexdigest()
        try:
            connection = db.connect('localhost', 'username', 'password', 'database_name')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users
                              WHERE username = %s
                              AND password = %s""", (username, sha256_password))
            if cursor.rowcount == 0:
                result = '<p>Error: incorrect user name or password</p>'
            else:
                cookie = SimpleCookie()
                sid = sha256(repr(time()).encode()).hexdigest()
                cursor.execute("""SELECT * FROM users
                                  WHERE username = %s""", (username))
                returned_results = cursor.fetchone()
                user_id = returned_results["user_id"]
                cookie['user_id'] = user_id
                cookie['sid'] = sid
                session_store = open('sess_' + sid, writeback=True)
                session_store['authenticated'] = True
                session_store['username'] = username
                session_store.close()
                result = """
                   <h1>Succesfully logged in!</h1>
                   <ul>
                       <li><a href="getstarted.py">Resume learning</a></li>
                       <li><a href="profile.py">Check out your profile</a></li>
                   </ul>"""
                print(cookie)
                cursor.close()
                connection.close()
        except (db.Error, IOError):
            result = '<p>Sorry! We are experiencing problems at the moment. Please try again later.</p>'

print('Content-Type: text/html')
print()
print("""
    <!DOCTYPE html>
    <html class="form_page" lang="en">
        <head >
            <title>Login</title>
		    <meta charset="utf-8"  />
		    <meta name="viewport" content="width=device-width, initial-scale=1.0">
		    <link rel="icon" type="image/png" href="icons/favicon/favicon.png"  />
		    <link rel="stylesheet" href="style.css"  />
        </head>
        <body>
			<main>
				<section>
		            <form action="login.py" method="post">
                        <h1>Login Form</h1>
		                <input type="text" name="username" id="username" value="%s" placeholder="username"/>
		                <input type="password" name="password" id="password" placeholder="password" />
		                <input type="submit" value="Login" />
                        <p>Forgot your password?</p>
                        <p>Due to budget cuts we don't have a method of retrieving your password. Have you tried 'password'?</p>
                        %s
		            </form>
				</section>
			</main>
        </body>
    </html>""" % (username, result))
