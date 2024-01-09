#!/usr/local/bin/python3

from cgitb import enable
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie

import pymysql as db

print('Content-Type: text/html')
print()

username=""

result = """
   <p>Please create an account or login to access this page.</p>
   <ul>
       <li><a href="register.py">Register</a></li>
       <li><a href="login.py">Login</a></li>
   </ul>"""

nav_results = """
	<li><a href="register.py">Register</a></li>
	<li><a href="login.py">Login</a></li>
	"""

try:
	cookie = SimpleCookie()
	http_cookie_header = environ.get('HTTP_COOKIE')
	if http_cookie_header:
		cookie.load(http_cookie_header)
		if 'sid' in cookie:
			sid = cookie['sid'].value
			session_store = open('sess_' + sid, writeback=False)
			if session_store.get('authenticated'):
				if session_store.get('authenticated'):
				    nav_results = """
				        <li><a href="logout.py">Logout</a></li>
				        """
				else:
				    nav_results = """
				        <li><a href="register.py">Register</a></li>
				        <li><a href="login.py">Login</a></li>
				        """
				username = session_store['username']
				connection = db.connect('localhost', 'username', 'password', 'database_name')
				cursor = connection.cursor(db.cursors.DictCursor)
				cursor.execute("""SELECT * FROM users WHERE username = %s""", (username))
				returned_results = cursor.fetchone()
				result = """<table id="quiz_results">
				       <tr><th colspan="2">Quiz Scores</th></tr>
				       <tr><th>Quiz</th><th>Score</th></tr>"""
				for item in returned_results:
					if "quiz" in item:
					   output_temp = item.split("_")
					   output_concat = output_temp[0]
					   output_name = output_concat[0].upper() + output_concat[1:len(output_concat)]
					   result += "<tr><td>%s</td><td>%s</td>" %(output_name, returned_results[item])

	else:
		print()



except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Profile</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="icon" type="image/png" href="icons/favicon/favicon.png"  />
            <link rel="stylesheet" href="style.css"  />
			<script src="night.js" type="module"></script>
        </head>
        <body>
            <nav>
                <ul>
					<li><a href="index.html">Home</a></li>
					<li><a href="getstarted.py">Learn</a></li>
					<li><a href="about.py">About</a></li>
					<li id="list_container">User
						<ul>
							%s
						</ul>
					</li>
				</ul>
				<button id="night_mode"><img src="icons/sun.svg" alt="An icon of the sun"  /></button>
            </nav>
			<main id="profile">
		        <section>
		           <h1>Welcome %s</h1>

		           %s
		        </section>
			</main>
		</body>
    </html>""" % (nav_results, username, result))
