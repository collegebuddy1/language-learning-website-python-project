#!/usr/local/bin/python3

from cgi import FieldStorage
from html import escape
from cgitb import enable
enable()

import pymysql as db

print("Content-Type: text/html")
print()

form_data = FieldStorage()
quiz = escape(form_data.getfirst("quiz", "").strip())
user_score = escape(form_data.getfirst("user_score", "0").strip())
user_id = escape(form_data.getfirst("user_id", "").strip())
user_score = int(user_score)


try:
    connection = db.connect('localhost', 'username', 'password', 'database_name')
    cursor = connection.cursor(db.cursors.DictCursor)
    if quiz == "introductions_quiz_score":
        cursor.execute("""UPDATE users SET introductions_quiz_score=%s WHERE user_id=%s""", (user_score, user_id))
    elif quiz == "basics_quiz_score":
        cursor.execute("""UPDATE users SET basics_quiz_score=%s WHERE user_id=%s""", (user_score, user_id))
    elif quiz == "acquaintances_quiz_score":
        cursor.execute("""UPDATE users SET acquaintances_quiz_score=%s WHERE user_id=%s""", (user_score, user_id))
    elif quiz == "lost_quiz_score":
        cursor.execute("""UPDATE users SET lost_quiz_score=%s WHERE user_id=%s""", (user_score, user_id))
    connection.commit()
    result = "Success"
    cursor.close()
    connection.close()

except db.Error:
    result = "Error has occurred when storing data"

print(result)
