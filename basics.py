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
			username = session_store['username']
			session_store.close()
			connection = db.connect('localhost', 'username', 'password', 'database_name')
			cursor = connection.cursor(db.cursors.DictCursor)
			cursor.execute("""SELECT * FROM users WHERE username = %s""", (username))
			returned_results = cursor.fetchone()
			if returned_results["basics_quiz_score"] == None:
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
				result = """<h1>You have already completed this quiz</h1>
							<a href="introductions.py">Next</a>"""
		else:
			result = "<h1>Please login to attempt this quiz</h1>"
	else:
		result = "<h1>Please login to attempt this quiz</h1>"

except dbError:
	result = "<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>"

print("""<!DOCTYPE html>
		<html lang="en">
			<head>
				<title>The Basics</title>
				<meta charset="utf-8"  />
				<meta name="viewport" content="width=device-width, initial-scale=1.0">
				<link rel="icon" type="image/png" href="icons/favicon/favicon.png"  />
				<link rel="stylesheet" href="style.css"  />
		        <script src="basics.js" type="module"></script>
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
		                <h1>Pronunciation</h1>
		                <p>
		                    "Learners also need to develop a concern for pronunciation. They must recognize that poor, unintelligible speech will make their attempts at conversing frustrating and unpleasant both for themselves and for their listeners." - Joanne Kenworthy
		                </p>
		            </section>
		            <section>
		                <h1>How to pronounce letters in the Chinese Alphabet</h1>
		                <p>
		                        Welcome to the first section of Survival Chinese. Here we will discuss about the basics of Chinese, how to read and pronounce words, as well as the number system. So let's get into it!
		                </p>
		                <p>
		                        Good pronunciation is the cornerstone of language learning. If you have a limited vocabulary but can be understood, you will get much further than someone with a large vocabulary whose pronunciation is unintelligible. Here we will learn the correct way to pronounce Chinese words, starting with the most difficult ones.
		                </p>
		                <table>
						<caption>Difficult consonant sounds</caption>
		                    <tr>
		                        <th>Sound</th><th>How to pronounce it</th>
		                    </tr>
							<tr>
		                        <td>zh</td><td>As in <b>J</b>ames or <b>J</b>oin</td>
		                    </tr>
		                    <tr>
		                        <td>ao</td><td>As in <b>oww</b></td>
		                    </tr>
		                    <tr>
		                        <td>ia</td><td>As in Y<b>ea</b>h</td>
		                    </tr>
		                    <tr>
		                        <td>z</td><td>As in ca<b>ts</b> or ren<b>ts</b></td>
		                    </tr>
		                    <tr>
		                        <td>x</td><td>Almost, but not quite <b>sh</b>are</td>
		                    </tr>
		                    <tr>
		                        <td>q</td><td>Almost, but not quite <b>ch</b>air</td>
		                    </tr>
		                    <tr>
		                        <td>j</td><td>Almost, but not quite <b>j</b>am</td>
		                    </tr>
		                </table>
		                <p>
		                    The consonants and consonant pairs listed above are some of the trickiest sounds to pronounce for a native english speaker. In comparison to this, Chinese vowels are much easier to pronounce, as they very closely represent certain sounds in the English language. These sounds can change based on which consonants and other vowels they're paired with, but for the most part, they sound as they are below.
		                </p>
		                <table>
						<caption>Vowel sounds</caption>
		                    <tr>
		                        <th>Sound</th><th>How to pronounce it</th>
		                    </tr>
							<tr>
		                        <td>a</td><td>As in <b>ah</b> or <b>ha</b></td>
		                    </tr>
		                    <tr>
		                        <td>e</td><td>Is like "<b>uh</b>" or "<b>duh</b>"</td>
		                    </tr>
		                    <tr>
		                        <td>i</td><td>Is like "s<b>ee</b>" or "kn<b>ee</b>"</td>
		                    </tr>
		                    <tr>
		                        <td>o</td><td>Is more like "<b>oh</b>"</td>
		                    </tr>
		                    <tr>
		                        <td>u</td><td>Is like "h<b>oo</b>t" or "b<b>oo</b>t"</td>
		                    </tr>
		                </table>
		            </section>
		            <section>
		                <h1>Getting to grips with tones</h1>
		                <p>
		                    Once you can understands the basics of how to vocalise Chinese words, the next thing to look at is <b>tones</b>. Tones in the Chinese language literally change the meaning of a word. Many words have identical pronunciations, such as <i lang="zh">M&#462;</i> (Horse) and <i lang="zh">M&#257;</i> (Mother). So <strong>get your tones right</strong> or you might end up in some sticky situations!
		                </p>
		                <p>
		                    There are 4 tones in Mandarin Chinese, making it a tonal language. Two completely different words might sound similar to the untrained ear, but can completely alter the meaning of a sentence. The tones appear over the <i lang="zh">pinyin</i> of a word (<i>pinyin</i> meaning the romanization of a Chinese character, making it readable without having to be able to read Chinese characters).
		                </p>

		                <figure>
		                    <img id="tone_image" src="images/illustrations/tones.svg" alt="A picture of Chinese tones"  />
		                    <figcaption>The four tones</figcaption>
		                </figure>
					</section>
					<section>
						<h1>How to pronounce each tone</h1>
						<p>
							When learning how to pronounce each tone, it can be helpful to look at the way the symbol is written. The way the word should be pronounced will follow the line. For example, the first tone is written with a perfectly horizontal line, so when pronouncing it, your pitch will stay the same all the way across the word, while the fourth tone is a sharp downward slope, and so the cadence should drop sharply, almost like it would when a person is speaking angrily in english.
						</p>

						<section>
							<h1>Tone 1</h1>
							<p>
								Tone 1 is pronounced evenly, without any change in cadence. It should be pronounced almost monotonously.
							</p>
						</section>
						<section>
							<h1>Tone 2</h1>
							<p>
								Tone 2 is pronounced with a rising intonation. The closest comparison in English is when asking a question. The pitch of the speaker's tone will rise at the end, e.g. "Are you sure?". This is how you would pronounce a word with the second tone.
							</p>
						</section>
						<section>
							<h1>Tone 3</h1>
							<p>
								Tone 3 is pronounced with an initial drop, then rising intonation. There is no equivalent in English.
							</p>
						</section>
						<section>
							<h1>Tone 4</h1>
							<p>
								Tone 4 is pronounced with a falling intonation. The closest comparison in English is when a person is angrily stating something. For example "I already told you, I don't have it!". The person's pitch will drop at the end, which is very similar to how words with the fourth tone should be pronounced.
							</p>
		                </section>
		            </section>
		            <section>
		                <h1>Understanding numbers</h1>
		                <p>The numbering system in Chinese is very straightforward. The numbers 0-10 are unique, everything after that is a repetition.</p>

		                <table>
						<caption>Numbers one to ten</caption>
		                    <tr>
		                        <th>Number</th><th  lang="zh">How to say it</th>
		                    </tr>
							<tr>
		                        <td>0</td><td  lang="zh">L&#237;ng</td>
		                    </tr>
		                    <tr>
		                        <td>1</td><td  lang="zh">Y&#299;</td>
		                    </tr>
		                    <tr>
		                        <td>2</td><td  lang="zh">&#200;r</td>
		                    </tr>
		                    <tr>
		                        <td>3</td><td  lang="zh">S&#257;n</td>
		                    </tr>
		                    <tr>
		                        <td>4</td><td  lang="zh">S&#236;</td>
		                    </tr>
		                    <tr>
		                        <td>5</td><td  lang="zh">W&#468;</td>
		                    </tr>
		                    <tr>
		                        <td>6</td><td  lang="zh">Li&#249;</td>
		                    </tr>
		                    <tr>
		                        <td>7</td><td  lang="zh">Q&#299;</td>
		                    </tr>
		                    <tr>
		                        <td>8</td><td  lang="zh">B&#257;</td>
		                    </tr>
		                    <tr>
		                        <td>9</td><td  lang="zh">Ji&#468;</td>
		                    </tr>
		                    <tr>
		                        <td>10</td><td  lang="zh">Sh&#237;</td>
		                    </tr>
		                </table>

		                <p>After ten, any number is a combination of however many tens there are and whatever the ones digit is. For example, the number thirteen will be <i lang="zh">sh&#237; s&#257;n</i> (one ten and three), the number 35 will be <i lang="zh">s&#257;n sh&#237; w&#468;</i> (three tens and five), while ninety seven will be <i lang="zh">ji&#468; sh&#237; q&#299;</i>.</p>
		            </section>

		            <section class="vocabulary">
						<h1>Important Vocabulary</h1>
		                <table>
		                    <tr>
		                        <th>Word</th><th>Meaning</th>
		                    </tr>
							<tr>
		                        <td lang="zh">W&#466;</td><td>I/me</td>
		                    </tr>
		                    <tr>
		                        <td lang="zh">N&#464;</td><td>You</td>
		                    </tr>
		                    <tr>
		                        <td lang="zh">T&#257;</td><td>He/She</td>
		                    </tr>
		                    <tr>
		                        <td lang="zh">W&#466; men</td><td>We/Us</td>
		                    </tr>
		                    <tr>
		                        <td lang="zh">N&#464; men</td><td>You (plural)</td>
		                    </tr>
		                    <tr>
		                        <td lang="zh">T&#257; men</td><td>They</td>
		                    </tr>
		                    <tr>
		                        <td lang="zh">N&#464; h&#462;o</td><td>Hello</td>
		                    </tr>
		                    <tr>
		                        <td lang="zh">Z&#224;i ji&#224;n</td><td>Goodbye</td>
		                    </tr>
		                    <tr>
		                        <td lang="zh">Zu&#243; ti&#257;n</td><td>Yesterday</td>
		                    </tr>
		                    <tr>
		                        <td lang="zh">J&#299;n ti&#257;n</td><td>Today</td>
		                    </tr>
		                    <tr>
		                        <td lang="zh">M&#237;ng ti&#257;n</td><td>Tomorrow</td>
		                    </tr>
		                </table>
		            </section>
					<section id="outer_box">
						%s
					</section>
		        </main>
			</body>
		</html>""" % (nav_results, result))
