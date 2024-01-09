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
            if returned_results["lost_quiz_score"] == None:
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
                    <section class="buttons">
                        <button id="start">Click here to start</button>
                    </section>
                    """
            else:
                result = """<h1>You have already completed this quiz.</h1>
                            <a href="introductions.py">Back</a>"""
        else:
            result = '<h1>You have already completed this quiz</h1>'
    else:
        result = "<h1>Please login to attempt this quiz</h1>"

except dbError:
	result = "<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>"

print("""
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Lost</title>
        <meta charset="utf-8"  />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" type="image/png" href="icons/favicon/favicon.png"  />
        <link rel="stylesheet" href="style.css"  />
		<script src="lost.js" type="module"></script>
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
                <h1>Lost</h1>
                <p>
                    "Some beautiful paths can't be discovered without getting lost." - Erol Ozan
                </p>
            </section>
            <section>
                <h1>So you've lost your way..</h1>
                <p>
                    Another part of learning a foreign language and being in a foreign country is being lost. It happens to everyone. If you have ever been to another country at any point, you have probably gotten lost. Then that moment happens when you're looking at your phone/map/GPS/street signs confused. You work up the courage to ask someone how to get to your destination. But oh no! You don't know any of the key vocabulary needed. Fear not, once you've finished this section, you will know how to approach people and ask for help.
                </p>
            </section>
            <section>
                <h1>Excuse me..</h1>
                <p>
                    Think about this.. when you're approaching a stranger, how are you going to address them? What will you say? Do you approach the person and say "Hey dude! You wanna tell me how I can get to xx place? No, instead you will be polite. Words like <b>excuse me</b>, <b>sorry to bother you</b>, <b>I appreciate it</b> will come into play. When dealing with strangers, it is normal to be a bit more polite and formal. After all, we don't know these people and we're asking for their help! When approaching someone to ask them a question, you can start by saying <i lang="zh">"B&#249; h&#462;o y&#236; si"</i> which means "I'm sorry". In this context, it's more like "sorry to bother you. After that, <i lang="zh">q&#464;ng w&#232;n</i>, meaning "can I ask?".
                </p>
            </section>
            <section>
                <h1>Where is..?</h1>
                <p>
                    In Chinese, <b>where</b> is <i lang="zh">N&#462;l&#464;</i> and <b>located at</b> is <i lang="zh">Z&#224;i</i>. When asking where a location is, you put those two together along with the location. However, in Chinese, the structure is completely different. Instead of saying "Where is X located?", you would say "X is located where?" or <i lang="zh">X z&#224;i n&#462;l&#464;?</i>
                </p>
            </section>
            <section class="related_vocab">
                <h1>I want to go to..</h1>
                <p>
                    There's no point knowing how to say any of this if you don't know how to say the location! Here is a number of locations you might find yourself going to:
                </p>
                <table>
                    <tr>
                        <th>Word</th><th>Meaning</th>
                    </tr>
					<tr>
                        <td lang="zh">Hu&#466;ch&#275; zh&#224;n</td><td>Train Station</td>
                    </tr>
                    <tr>
                        <td lang="zh">G&#333;ngch&#275; zh&#224;n</td><td>Bus Station</td>
                    </tr>
                    <tr>
                        <td lang="zh">J&#299;ch&#462;ng</td><td>Airport</td>
                    </tr>
                    <tr>
                        <td lang="zh">B&#299;ngu&#462;n</td><td>Hotel</td>
                    </tr>
                    <tr>
                        <td lang="zh">Y&#237;nh&#225;ng</td><td>Bank</td>
                    </tr>
                    <tr>
                        <td lang="zh">Ch&#257;osh&#236;</td><td>Supermarket</td>
                    </tr>
                    <tr>
                        <td lang="zh">G&#333;ngyu&#225;n</td><td>Public Park</td>
                    </tr>
                </table>
            </section>
            <section>
                <h1>Putting it all together</h1>
                    <p>
                        Ok, the situation is upon you, you're lost in Shanghai, you want to get to the <i lang="zh">H&#243;ngqi&#225;o</i> train station. What do you say!? To make it easier for you, we've put together some sample sentences below as well as a podcast.
                    </p>
                    <ul>
                        <li><i lang="zh">B&#249;h&#462;o y&#236;si q&#464;ngw&#232;n</i>: Sorry to disturb you, can I ask something?</li>
                        <li><i lang="zh">K&#283;y&#464; b&#257;ng w&#466; y&#299;g&#232; m&#225;ng ma?</i>: Could you help me with something?</li>
                        <li><i lang="zh">W&#466; y&#466;udi&#462;n m&#237;l&#249;</i>: I'm a little lost.</li>
                        <li><i lang="zh">H&#243;ngqi&#225;o hu&#466;ch&#275; zh&#224;n z&#224;i n&#224;l&#464;?</i>: Where is Hongqiao station?</li>
                    </ul>
                    <audio controls>
                        <source src="podcast_mono.mp3" type="audio/mpeg">
                    </audio>
            </section>
            <section class="vocabulary">
                <h1>Key vocabulary</h1>
                <table>
                    <tr>
                        <th>Word</th><th>Meaning</th>
                    </tr>
                    <tr>
                        <td>M&#237;l&#249;</td><td>Lost</td>
                    </tr>
                    <tr>
                        <td>Y&#466;udi&#462;n</td><td>is placed before an adjective and is usually used in a negative sense. It means "a little" or "a bit", as in "I'm a little lost", or I'm a little tired. It does not refer to the size of something</td>
                    </tr>
                    <tr>
                        <td>B&#249;h&#462;o y&#236;si</td><td>I'm sorry/excuse me</td>
                    </tr>
                    <tr>
                        <td>XX z&#224;i n&#462;l&#464;?</td><td>Where is xx?</td>
                    </tr>
                    <tr>
                        <td>Q&#464;ng w&#232;n?</td><td>Can I ask?</td>
                    </tr>
                </table>
            </section>
			<section id="outer_box">
                %s
            </section>
        </main>
    </body>
</html>""" % (nav_results, result))
