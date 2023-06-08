#!/usr/bin/python3

# Script: Ops 401 Class 37 script
# Author: Paul Stroud
# Date of latest revision: 06/07/23
# Purpose: Cookie
# Resources used: google, stackoverflow, github demo, chatgpt

# MAIN REQS:
# Add here some code to make this script perform the following:
# - Send the cookie back to the site and receive a HTTP response
# - Generate a .html file to capture the contents of the HTTP response
# - Open it with Firefox


# The below Python script shows one possible method to return the cookie from a site that supports cookies.

import requests
import subprocess


cookie_monster_ascii = '\n            _  _' \
                       '\nme want    (.)(\')' \
                       '\nmore...   / ___, \  .-.' \
                       '\n    .-. _ \ \'--\' / (:::) ' \
                       '\n   (:::{ \'-`--=-`-\' }"`' \
                       '\n    `-\' `"/      \"`' \
                       '\n          \      /' \
                       '\n         _/  /\  \_' \
                       '\n       {   /  \   }' \
                       '\n         `"`    `"`'


### MAIN ###
print(cookie_monster_ascii)

targetsite = "http://www.whatarecookies.com/cookietest.asp" # Comment this out if you're using the line above
response = requests.get(targetsite)
cookie = response.cookies

print("Target site is " + targetsite)
print(cookie)

response = requests.get(targetsite, cookies=cookie) # send the cookie back to the site

# put the response into a .html file
filename = "response.html"
with open(filename, "w") as file:
    file.write(response.text)

subprocess.run(["firefox", filename]) # open html with firefox
