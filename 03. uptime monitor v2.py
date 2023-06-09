#!/usr/bin/python3


# Script: Ops 401 Class 03 script
# Author: Paul Stroud
# Date of latest revision: 04/19/23
# Purpose: Uptime monitoring script v2


# MAIN REQS:
# Ask the user for an email address and password to use for sending notifications.
# Send an email to the administrator if a host status changes (from “up” to “down” or “down” to “up”).
# Clearly indicate in the message which host status changed, the status before and after, and a timestamp of the event.
#
# OPTIONAL REQS: (aka Stretch Goals)
# Append all status changes to an event log. Each event must include a timestamp, event code, any host IP addresses involved, and a human readable description.
# Check for BURNER_EMAIL_ADDRESS and BURNER_EMAIL_PASSWORD environment variables (eg: loaded from .profile). If found, the script skips requesting credentials via user input.




import sys          # for parsing script args
import datetime     # to access and format date/time
import time         # for timeout/sleep
import re           # for regex
import subprocess   # for running bash commands

import smtplib      # to send emails via SMTP
from email.message import EmailMessage  # to craft emails
import os           # to verify if file exists


###### GLOBAL VARS ########

# define the IP address regex
ip_regex = "^(\d{1,3}\.){3}\d{1,3}$"  
# regex equivalent to ^([0-9]{1,3}\.){3}[0-9]{1,3}$
# both regex checks for a string that contains 3x groups of 1-3 numbers
# where each decimal digit is between 0-9
# the groups are separated by a '.'
# the string ends with another group of 1-3 digits between [0-9]

# global arrays
ip_status = { 0:"UP", 1:"DOWN" }  # node status messages
flair = [ "✓", "✗" ]             # some visual flair


###### FUNCTIONS ########

def IP_validation(addr):    # validates IP address
    if re.match(ip_regex, addr): # regex match ok?
       return True
    else: return False

# displays a message and writes it to log file
def print_log(str, file):  # str needs to end with '\n'
    file.write(str)     # entry in the log file
    print(str, end="")  # message to console
   
# send an email via SMTP
def send_email(subj, msg, rcvr, sdr, sdr_pw, smtp_svr="smtp.gmail.com", smtp_port=587):
    #print(f'Sending {msg} to {rcvr}')
    SMTP = smtplib.SMTP(smtp_svr, smtp_port)
    SMTP.starttls()
    SMTP.login(sdr, sdr_pw)

    em = EmailMessage()
    em['From'] = sdr
    em['To'] = rcvr
    em['Subject'] = subj
    em.set_content(msg)

    test = SMTP.sendmail(sdr, rcvr, em.as_string())

    SMTP.quit()


###### MAIN CODE BELOW ########


# --- start arg validation ---

if len(sys.argv) != 2:  # need exactly one script arg (the IP address)
  print("Invalid number of arguments. Please make sure the script has exactly one argument.")
  exit

ip_addr = sys.argv[1]   # save arg to a var

if (not IP_validation(ip_addr)):    # check if IP is invalid
  # git to ze choppa
  print("Invalid IP detected. Please try again.")
  exit

# --- end arg validation ---



# attempt to read email info from a text file
# the format for the text file is:
# <sender addr>
# <SMTP password (sender)>
# <receiver addr>
# there is no input validation
# no leading spaces or any other formatting
if (os.path.exists("email.txt")): # if file exists, read credentials 
  print("Loading email info for alerts... ", end="")
  FILE = open("email.txt", "r")  # open the file
  # read each line into its var, strip the trailing newline
  sender = FILE.readline().replace("\n", "")
  sender_pw = FILE.readline().replace("\n", "")
  receiver = FILE.readline().replace("\n", "")
  FILE.close()    # close the file stream
  print('OK')
else:   # manually enter the info
  print("Enter the following information for email alerts:")
  sender = input("\tSender email: ")
  sender_pw = input("\tSMTP password: ")
  receiver = input("\tRecipient email: ")


# we're ready to go
# now let's do useful stuff

print(f"\n[ Monitoring uptime for: {ip_addr} ]")

ping_count = 0  # all pings
ping_ok = 0     # good pings

try:  # you can't fail if you don't try
    FILE = open(f"uptime_log_{ip_addr}.txt", "w")    # create/open the log file
    last_ping = 0   # 0 is good, 1 is bad
    while True:     # to infinity and beyond!
        # run a ping cmd and save results to a var
        ping_result = subprocess.run(["ping", "-c 1", ip_addr], capture_output=True, text=True)
        pstat = ping_result.returncode # shortcut var for status code (0 is good, 1 is bad)

        # pull current date/time; format and save to a var
        timecode = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")

        ping_ok += 0 if pstat else 1   # ++ only good pings
        ping_count += 1  # ++ all attempts

        # craft a formatted log entry that includes date/time and a status message
        log_str = timecode + " > " + f"Host {ip_addr} is " + ip_status[pstat] + " " + flair[pstat] + "\n"
        
        print_log(log_str, FILE)
        print("Ctrl+C to stop", end="\r")   # floating message

        if (last_ping != pstat): # status change?
          alert_str = f"Host ({ip_addr}) status changed from {ip_status[last_ping]} to {ip_status[pstat]}"
          print_log(timecode +  " > ALERT: " + alert_str + "\n", FILE)
          # alert the admin
          send_email(f"UPTIME ALERT: Host {ip_addr} is {ip_status[pstat]}", 
                     timecode + " > " + alert_str, receiver, sender, sender_pw)

        last_ping = pstat
        time.sleep(2)   # 2 sec timeout

except KeyboardInterrupt:   # Ctrl+C
    print("              ")  # overwrite last line w/ spaces
    
    # calculate success/failure percentages
    uptime_pct = 100 * (ping_ok / ping_count)
    fail_pct = 100 * ((ping_count - ping_ok) / ping_count)
    
    # calculate stats and print/log them
    stats = f"UPTIME STATS: Host {ip_addr} was up {round(uptime_pct)}% of the time\n"
    print_log(stats, FILE)

    # packet count stats
    stats = f"\tPackets sent: {ping_count}\n" + \
            f"\tPackets received: {ping_ok}\n" + \
            f"\tPackets lost: {ping_count - ping_ok}\n"
    print_log(stats, FILE)


    stats = f"({round(fail_pct)}% pings failed)\n"
    if fail_pct > 0: # if any pings failed
      print_log(stats, FILE)
    
    FILE.close()    # close the file stream

except:     # catch-all exception handling
    FILE.close()    # close the file stream (if still open)


print("\n^^^ Uptime monitor v2 - crafted by Paul Stroud ^^^")


# le goodbye