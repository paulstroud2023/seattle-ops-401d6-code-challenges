#!/usr/bin/python3

# Script: Ops 401 Class 16 script
# Author: Paul Stroud
# Date of latest revision: 05/08/23
# Purpose: Brute force pt1
# Resources used: google, stackoverflow, github demo, chatgpt

# MAIN REQS:
# In Python, create a script that prompts the user to select one of the following modes:
# Mode 1: Offensive; Dictionary Iterator
#   Accepts a user input word list file path and iterates through the word list, assigning the word being read to a variable.
#   Add a delay between words.
#   Print to the screen the value of the variable.
# Mode 2: Defensive; Password Recognized
#   Accepts a user input string.
#   Accepts a user input word list file path.
#   Search the word list for the user input string.
#   Print to the screen whether the string appeared in the word list.


import sys    # for args and sys.exit() to kill the script
import time   # for time.sleep() timeout


### FUNCTIONS ####

# no functions

#### MAIN ####

if len(sys.argv) > 1:
  wordlist = sys.argv[1]
else: 
  wordlist = input('Enter the wordlist file ("/usr/share/wordlists/rockyou.txt" is default): ')
  ### if nothing entered, use the default filename
  wordlist = "/usr/share/wordlists/rockyou.txt" if (wordlist == "") else wordlist 

# menu loop
while True:
    time.sleep(1)
    print("\n>>> Password Iterator v1.0 <<<")
    print("Select the operation to perform:" \
          "\n\t1. Dictionary Iterator" \
          "\n\t2. Password Lookup" \
          "\n\t0. Exit")

    op = -1  # holds user input
    while not (op >= 0 and op <= 2):
      try:
         op = int(input("Enter a menu option (0-2): "))
      except KeyboardInterrupt:   # Ctrl+C
         print()
         sys.exit()
      except: # catch all for anything other than menu options or Ctrl+C
         print("Invalid input. Please try again.")

    if op == 0:
      print("Exiting the script...")
      sys.exit()  # kill the script
    else:
      if op == 1:   # password iterator
        print(f"Parsing {wordlist} as the wordlist file:")
        try:
            file = open(wordlist, "rt")
            for pw in file:   # iterate over each line/word in the wordlist
               print("  ", pw.strip(), sep='')  # simulate doing useful stuff with each pw
               time.sleep(1)
        except FileNotFoundError: print(f"File {wordlist} does not exist")

      if op == 2:   # password lookup
        test = input("Input the password to look up: ")
        print(f"Looking for {test} in {wordlist}:")
        i = 0   # line counter
        try:
            file = open(wordlist, "rt")
            for pw in file:
               i += 1
               if (test == pw.strip()):
                 print(f"MATCH FOUND!   Line {i}: {test} - {pw.strip()}")
        except FileNotFoundError: print(f"File {wordlist} does not exist")

# end of script