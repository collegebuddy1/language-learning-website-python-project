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
								<li><a href='logout.py'>Logout</a></li>
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
			if returned_results["introductions_quiz_score"] == None:
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
							<a href="basics.py">Back</a>|<a href="acquaintances.py">Next</a>"""
		else:
			result = '<h1> Please login to attempt this quiz</h1>'
	else:
		result = "<h1>Please login to attempt this quiz</h1>"

except dbError:
	result = "<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>"

print("""
<!DOCTYPE html>
<html lang="en">
	<head>
		<title>Introduction</title>
		<meta charset="utf-8"  />
		<meta name="viewport" content="width=device-width, initial-scale=1.0"  />
        <link rel="icon" type="image/png" href="icons/favicon/favicon.png"  />
		<link rel="stylesheet" href="style.css"  />
        <script src="introductions.js" type="module"></script>
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
                <h1>Introductions</h1>
                <p>"If you are trying to get information across to someone, your ability to create a compelling introduction may be the most important single factor in the later success of your mission." - John Medina</p>
            </section>
            <section>
                <h1>Introducing yourself</h1>
                <p>
                    Introductions are important.. <b>VERY</b> important! They are also a key part of any foreign language. If you need to use a foreign language, you are probably in a different part of the world. If you are in a different part of the world, you probably don't know the people around you. If you don't know the people around you, you will definitely need to introduce yourself to get to know the people around you! It's just a fact of life. An introduction is like an advertisement, it is when people get a first impression of who you are. That is what makes this section so important!
                </p>
            </section>
            <section>
                <h1>Saying hello</h1>
                <p>
                    In the last section, we learned the greeting <i lang="zh">N&#464; h&#462;o</i>, which is a greeting used when talking to one person. <i lang="zh">N&#464;</i> meaning you and <i lang="zh">h&#462;o</i> meaning good. In other words, you're literally saying "You are good". In that case, how would you greet multiple people? You would say <i lang="zh">D&#224; ji&#257; h&#462;o</i> (<i lang="zh">D&#224; ji&#257;</i> meaning <b>everyone</b>) or you can also use the phrase <i lang="zh">N&#464; men h&#462;o</i> (<i lang="zh">N&#464; men</i> from the first section meaning 'you' (plural)). If you want to say "Nice to meet you" you can say <i lang="zh">H&#283;n g&#257;o x&#236;ng r&#232;n sh&#237; n&#464;</i> (which literally means "Very happy to meet you"). I've broken the words down in the vocabulary section.
                </p>
            </section>
            <section>
                <h1>All about me</h1>
                <p>
                    Because the title of this topic is introductions, it stands to reason that a lot of this section will focus on me! me! me! (err.. you! you! you!). Introductions are used to talk about yourself, so it is important to learn how to do so! The verb structure is such that when speaking about yourself, the language structure is subject + action, the same as in English.
                </p>
                <p>
                    To start with, you might remember that I is <i lang="zh">W&#466;</i>. How can we use that further? For example, to say "My name is" in Chinese you say <i lang="zh">W&#466; ji&#224;o</i> (name). Another example, to say "I am xx years old", you would use <i lang="zh">W&#466;</i> again, along with the verb <b>to be</b> which is <i lang="zh">sh&#236;</i> followed by your age, e.g. <i lang="zh">W&#466; sh&#236; s&#257;n sh&#237; w&#468; su&#236;</i> - I'm 35 years old. <i lang="zh">Su&#236;</i> in this sentence means <b>years old</b>.
                </p>
                <section class="related_vocab">
				<h1>Related vocabulary</h1>
                    <table>
					<caption>Some other verb structures that start with <b>"I"</b></caption>
                        <tr>
                            <th>Word</th><th>Translation</th>
                        </tr>
                        <tr>
                            <td>W&#466; x&#464;hu&#257;n</td><td>I like</td>
                        </tr>
                        <tr>
                            <td>W&#466; y&#466;u</td><td>I have</td>
                        </tr>
                        <tr>
                            <td>W&#466; y&#224;o</td><td>I want</td>
                        </tr>
                        <tr>
                            <td>W&#466; zu&#242;</td><td>I do</td>
                        </tr>
                        <tr>
                            <td>W&#466; q&#249;</td><td>I go</td>
                        </tr>
                    </table>
                </section>
            </section>
            <section>
				<h1>What do you do?</h1>
				<p>
					If you were to describe yourself, what would you normally talk about? You name, age, maybe your job and/or your hobbies. The way you would talk about your job in Chinese is by using the word <i lang="zh">G&#333;ngzu&#242;</i>. This means work/job. So if you wanted to say "My job is", you would say "<i lang='zh'>W&#466; de g&#333;ngzu&#242; sh&#236;</i>. <i lang="zh">de</i> here means it is yours, it implies ownership of something. So <i lang="zh">W&#466; de</i> means mine.
				</p>
				<section class="related_vocab">
                    <h1>Related vocabulary</i></h1>
                    <table>
						<caption>Some other examples with <i lang="zh">'de'</i></caption>
                        <tr>
                            <th>Example</th><th>Translation</th>
                        </tr>
                        <tr>
                            <td lang="zh">W&#466; de m&#237;ngz&#236;</td><td>My name</td>
                        </tr>
                        <tr>
                            <td lang="zh">W&#466; de p&#233;ng y&#466;u</td><td>My friend</td>
                        </tr>
                        <tr>
                            <td lang="zh">W&#466; de &#224;ih&#224;o</td><td>My hobby</td>
                        </tr>
                    </table>
                </section>
            </section>

            <section class="vocabulary">
                <h1>Important vocabulary</h1>
                <table>
                    <tr>
                        <th>Word</th><th>Translation</th>
                    </tr>
                    <tr>
                        <td lang="zh">D&#224; ji&#257;</td><td>Everyone</td>
                    </tr>
                    <tr>
                        <td lang="zh">N&#464; men h&#462;o</td><td>Hello (to a group of people)</td>
                    </tr>
                    <tr>
                        <td lang="zh">X&#464; hu&#257;n</td><td>To like</td>
                    </tr>
					<tr>
						<td lang="zh">G&#333;ngzu&#242;</td><td>Work</td>
					</tr>
                    <tr>
                        <td lang="zh">Su&#236;</td><td>Years old</td>
                    </tr>
                </table>
            </section>
            <section id="outer_box">
    			%s
    		</section>
        </main>
	</body>
</html>""" % (nav_results, result))
