#!/usr/local/bin/python3

from cgitb import enable
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie

print('Content-Type: text/html')
print()

result = '<p>You are already logged out</p>'
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = open('sess_' + sid, writeback=True)
            session_store['authenticated'] = False
            session_store.close()
            result = """
                <h1>Successfully logged out!</h1>
                <p>Thanks for vising Survival Chinese</p>
                <p><a href="login.py">Login again</a></p>"""
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
    <!DOCTYPE html>
    <html id="logout" lang="en">
        <head>
	        <title>Logout</title>
	        <meta charset="utf-8" />
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="icon" type="image/png" href="icons/favicon/favicon.png"  />
            <link rel="stylesheet" href="style.css"  />
        </head>
        <body>
            <main>
                <section>
                    %s
                </section>
            </main>
        </body>
    </html>""" % (result))
