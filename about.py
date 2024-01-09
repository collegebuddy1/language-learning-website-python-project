#!/usr/local/bin/python3

from cgitb import enable
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie

print('Content-Type: text/html')
print()

try:
	cookie = SimpleCookie()
	http_cookie_header = environ.get('HTTP_COOKIE')
	if http_cookie_header:
		cookie.load(http_cookie_header)
		if 'sid' in cookie:
			sid = cookie['sid'].value
			session_store = open('sess_' + sid, writeback=False)
			if session_store.get('authenticated'):
			    nav_results = """
			        <li><a href="profile.py">Profile</a></li>
			        <li><a href="logout.py">Logout</a></li>
			        """
			else:
			    nav_results = """
			        <li><a href="register.py">Register</a></li>
			        <li><a href="login.py">Login</a></li>
			        """
		else:
			nav_results = """
				<li><a href="register.py">Register</a></li>
				<li><a href="login.py">Login</a></li>
				"""
	else:
		nav_results = """
			<li><a href="register.py">Register</a></li>
			<li><a href="login.py">Login</a></li>
			"""

except dbError:
	result = "<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>"

print("""
	<!DOCTYPE html>
	<html lang="en">
		<head>
			<title>About</title>
			<meta charset="utf-8"  />
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<link rel="stylesheet" href="style.css"  />
	    	<link rel="icon" type="image/png" href="icons/favicon/favicon.png"  />
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
			<main>
				<section class="hero_image">
					<h1>About</h1>
		            <p>
		                "The limits of my language mean the limits of my world." - Ludwig Wittgenstein
		            </p>
				</section>
			    <section>
			        <h1>The story behind Survival Chinese</h1>
			        <p>
			            This website was created out of years of frustration learning Chinese. Sifting through the endless amount of resources online and not finding much good content. Having lived in China for more than five years, I've met quite a number of foreigners who have lived there for over than a decade and still can't speak more than a few words. The goal behind Survival Chinese is to give beginners a small but practical base to start with, and as they grow more confident and comfortable, can use more abstract learning resources.
			        </p>
			    </section>
			</main>
		</body>
	</html>""" % (nav_results))
