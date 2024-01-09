#!/usr/local/bin/python3

from cgitb import enable
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie

print('Content-Type: text/html')
print()


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

except dbError:
	result = "<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>"

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Start learning</title>
            <meta charset = "utf-8"  />
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

            <main id="choice">
                <section>
                    <h1>Welcome to Survival Chinese!</h1>
                    <p>The goal of this website is to get you comfortable with the kind of Chinese you would use in every day situations. Many websites tend to teach extremely basic content, or content that is abstract. The goal of this website is to teach you things that you can go and use immediately. We will start with the basics of pronunciation and personal pronouns, then work our way up from there! While it is not compulsory to start at the start, it is recommended.</p>
                </section>
                <section class="icons">
                    <a href="basics.py">
                        <figure>
                            <img src="images/icon_images/basics_rectangular.jpg"  alt="An image of some worn building blocks with letters stacked one on top of each other."  />
                            <figcaption>Basics</figcaption>
                        </figure>
                    </a>
                    <a href="introductions.py">
                        <figure>
                            <img src="images/icon_images/introduction_rectangular.jpg"  alt="An image of a woman making a speech, surrounded by people."  />
                            <figcaption>Introductions</figcaption>
                        </figure>
                    </a>
                    <a href="acquaintances.py">
                        <figure>
                            <img src="images/icon_images/acquaintance_drink_rectangular.jpg" alt="An image of three glasses being clinked together in a bar scene."  />
                            <figcaption>Acquaintances</figcaption>
                        </figure>
                    </a>
                    <a href="lost.py">
                        <figure>
                            <img src="images/icon_images/lost_hand_rectangular.jpg" alt="An image of a person pointing at a map."  />
                            <figcaption>Lost</figcaption>
                        </figure>
                    </a>
                </section>
            </main>
        </body>
    </html>""" % (nav_results))
