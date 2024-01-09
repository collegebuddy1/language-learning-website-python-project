#!/usr/local/bin/python3

from cgitb import enable
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie

import pymysql as db

print('Content-Type: text/html;')
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
			username = session_store["username"]
			session_store.close()
			connection = db.connect('localhost', 'username', 'password', 'database_name')
			cursor = connection.cursor(db.cursors.DictCursor)
			cursor.execute("""SELECT * FROM users WHERE username = %s""", (username))
			returned_results = cursor.fetchone()
			if returned_results["acquaintances_quiz_score"] == None:
				result = """
					<h1>Test your knowledge with a quiz</h1>
					<p>
						The vocabulary section above will be hidden once you start!
					</p>
					<section class="hidden_items" id="questions_box">
					    <h1 id="question_text"></h1>
					    <section id="answer_area">
					        <button class="button">Answer 1</button>
					        <button class="button">Answer 2</button>
					        <button class="button">Answer 3</button>
					        <button class="button">Answer 4</button>
					    </section>
					</section>
					<section>
					    <button id="start">
							Click here to start
						</button>
					</section>
				            """
			else:
			    result = """<h1>You have already completed this quiz.</h1>
							<a href="introductions.py">Back</a>|<a href="lost.py">Next</a>"""
		else:
			result = "<h1>Please login to attempt this quiz</h1>"
	else:
	    result = "<h1>Please login to attempt this quiz</h1>"

except dbError:
	result = "<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>"

print("""<!DOCTYPE html>
		<html lang="en">
	    <head>
	        <title>Making friends</title>
	        <meta charset="utf-8"  />
	        <meta name="viewport" content="width=device-width, initial-scale=1.0">
	        <link rel="icon" type="image/png" href="icons/favicon/favicon.png"  />
	        <link rel="stylesheet" href="style.css"  />
			<script src="acquaintances.js" type="module"></script>
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
					<h1>Acquaintances</h1>
		            <p>
		                "Life is beautiful not because of the things we see or do. Life is beautiful because of the people we meet." - Simon Sinek
		            </p>
				</section>
		        <section>
					<h1>Long time no see!</h1>
			        <p>
			            That introduction you made last time went great. So great that everyone you introduced yourself to has fond memories of you. Now some time has passed and you've bumped into one of the people you introduced yourself to. What do you say? How do you keep the conversation going and continue to give that great impression that you gave before? Look no further, your answers are all here!
			        </p>
				</section>
			    <section>
					<h1>How have you been..?</h1>
			        <p>
			            Think about this, you haven't seen someone for a while. How would you greet them in English? One of the most common phrases you might find yourself saying is "Long time no see!". Many sources debate about the origins of this phrase, but it is widely agreed to come from one of two areas. Either from American Indians or sailors of the British navy who picked it up from Chinese people they enountered on their journeys. That is to say, the phrase is the exact same in Chinese as it is in English. In Chinese you would say <i lang="zh">H&#462;oji&#468; b&#249;ji&#224;n</i>. <i lang="zh">H&#462;oji&#468;</i> meaning a <b>long</b> time and <i lang="zh">B&#249;ji&#224;n</i> which literally means <b>No see</b> or to not see.
			        </p>
				</section>
			    <section>
			        <h1>How are you doing?</h1>
			        <p>
			            If you find yourself bumping into an acquaintance or a good friend during your travels in China, chances are they will ask you 'have you eaten?'. No, they're not curious about your hunger levels or when your last snack was! <i lang="zh">N&#464; ch&#299;f&#224;n le m&#462;?</i> is one of the first things people will ask you once you start a conversation with them. It's a start to a conversation. If someone asks you, you can normally reply with <i lang="zh">ch&#299; le, n&#464; ne? </i>. <i lang="zh">ch&#299; le</i> means I have eaten, <i lang="zh">ch&#299;</i> being the verb <b>To eat</b>.
			        </p>
		        </section>
		        <section>
		            <h1>Now that we're done with pleasantries</h1>
		            <p>
		                Ok, you've said hello, you've asked have they eaten. Now you want to ask them how they're doing. This part is a bit more tricky. To ask someone how they have been recently, you'd say <i lang="zh">zu&#236;j&#236;n gu&#242; d&#233; z&#283;ny&#224;ng</i>. <i lang="zh">zu&#236; j&#236;n</i> meaning 'recent' or 'recently', <i lang="zh">z&#283;ny&#224;ng</i> meaning 'how' and <i lang="zh">gu&#242; d&#233;</i> which indicates the passing of time. All together it means how have things gone recently?
		             </p>
		        </section>
		        <section>
		            <h1>How have things been going?</h1>
		            <p>
		                Quick! Someone has used what we just taught you above and has asked you <i lang="zh">zu&#236;j&#236;n gu&#242; d&#233; z&#283;ny&#224;ng?</i>. What do you say? If you're anything like me, no matter if your house was just blown away by a tornado or you one the lottery, you'll have the same answer, 'Not too bad'. Well, how would you say it in Chinese? <i lang="zh">H&#225;i b&#250;cu&#242;</i>. <i lang="zh">b&#250; cu&#242;</i> meaning not bad. <i lang="zh">cu&#242;</i> by itself meaning wrong/incorrect and <i lang="zh">b&#249;</i> meaning not.
		            </p>
		        </section>
		        <section class="vocabulary">
					<h1>Vocabulary</h1>
				    <table>
		                <tr>
		                    <th>Words</th><th>Translation</th>
		                </tr>
		                <tr>
		                    <td>H&#462;oji&#468; b&#249;ji&#224;n</td><td>Long time no see</td>
		                </tr>
		                <tr>
		                    <td>H&#462;o ji&#468;</td><td>A long time</td>
		                </tr>
		                <tr>
		                    <td>Ji&#224;n</td><td>To see</td>
		                </tr>
		                <tr>
		                    <td>Ch&#299;</td><td>To eat</td>
		                </tr>
		                <tr>
		                    <td>B&#249; cu&#242;</td><td>Not bad</td>
		                </tr>
		            </table>
		        </section>
				<section id="outer_box">
					%s
				</section>
			</main>
	    </body>
	</html>""" % (nav_results, result))
