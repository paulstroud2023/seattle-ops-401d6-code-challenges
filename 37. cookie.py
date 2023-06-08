#!/usr/bin/python3

# Script: Ops 401 Class 37 script
# Author: Paul Stroud
# Date of latest revision: 06/07/23
# Purpose: Cookie
# Resources used: google, stackoverflow, github demo, chatgpt

# MAIN REQS:
# In Python create a script that executes from a Linux box to perform the following:
#   Prompts the user to type a URL or IP address.
#   Prompts the user to type a port number.
#   Performs banner grabbing using netcat against the target address at the target port; prints the results to the screen then moves on to the step below.
#   Performs banner grabbing using telnet against the target address at the target port; prints the results to the screen then moves on to the step below.
#   Performs banner grabbing using Nmap against the target address of all well-known ports; prints the results to the screen.



#!/usr/bin/env python3

# The below Python script shows one possible method to return the cookie from a site that supports cookies.

import requests

# targetsite = input("Enter target site:") # Uncomment this to accept user input target site
targetsite = "http://www.whatarecookies.com/cookietest.asp" # Comment this out if you're using the line above
response = requests.get(targetsite)
cookie = response.cookies

def bringforthcookiemonster(): # Because why not!
    print('''

              .---. .---.
             :     : o   :    me want cookie!
         _..-:   o :     :-.._    /
     .-''  '  `---' `---' "   ``-.
   .'   "   '  "  .    "  . '  "  `.
  :   '.---.,,.,...,.,.,.,..---.  ' ;
  `. " `.                     .' " .'
   `.  '`.                   .' ' .'
    `.    `-._           _.-' "  .'  .----.
      `. "    '"--...--"'  . ' .'  .'  o   `.

        ''')

bringforthcookiemonster()
print("Target site is " + targetsite)
print(cookie)

# Add here some code to make this script perform the following:
# - Send the cookie back to the site and receive a HTTP response
# - Generate a .html file to capture the contents of the HTTP response
# - Open it with Firefox
#
# Stretch Goal
# - Give Cookie Monster hands