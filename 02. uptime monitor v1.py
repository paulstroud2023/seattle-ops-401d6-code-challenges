#!/usr/bin/python3


# Script: Ops 401 Class 02 script
# Author: Paul Stroud
# Date of latest revision: 04/18/23
# Purpose: Uptime monitoring script

# MAIN REQS:
# - Transmit a single ICMP (ping) packet to a specific IP every two seconds.
# - Evaluate the response as either success or failure.
# - Assign success or failure to a status variable.
# - For every ICMP transmission attempted, print the status variable along with a comprehensive timestamp and destination IP tested.
#       Example output: 2020-10-05 17:57:57.510261 Network Active to 8.8.8.8
#
# OPTIONAL REQS: (aka Stretch Goals)
# - Save the output to a text file as a log of events.
# - Accept user input for target IP address.





import sys          # for parsing script args
import datetime     # to access and format date/time
import time         # for timeout/sleep
import re           # for regex
import subprocess   # for running bash commands


###### GLOBAL VARS ########

# define the IP address regex
ip_regex = "^(\d{1,3}\.){3}\d{1,3}$"  
# regex equivalent to ^([0-9]{1,3}\.){3}[0-9]{1,3}$
# both regex checks for a string that contains 3x groups of 1-3 numbers
# where each decimal digit is between 0-9
# the groups are separated by a '.'
# the string ends with another group of 1-3 digits between [0-9]


###### FUNCTIONS ########

def IP_validation(addr):    # validates IP address
    if re.match(ip_regex, addr): # regex match ok?
       return True
    else: return False


###### MAIN CODE BELOW ########

if len(sys.argv) == 2:  # need exactly one script arg (the IP address)
  ip_addr = sys.argv[1] # save it to a var

  if IP_validation(ip_addr):    # verify the IP is valid, otherwise git to ze choppa
    # do useful stuff
    print(f"[ Monitoring uptime for: {ip_addr} ]")
    
    ping_count = 0  # all pings
    ping_ok = 0     # good pings

    try:  # you can't fail if you don't try
        FILE = open(f"uptime_log_{ip_addr}.txt", "w")    # create/open the log file

        while True:     # to infinity and beyond!
            # run a ping cmd and save results to a var
            ping_result = subprocess.run(["ping", "-c 1", ip_addr], capture_output=True, text=True)
           
            ping_ok += 0 if ping_result.returncode else 1   # ++ only good pings
            ping_count += 1  # ++ all attempts

            # craft a formatted log entry that includes date/time and a status message
            log_str = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S") + " > " + \
                      f"Host {ip_addr} is " + ("DOWN" if ping_result.returncode else "UP") + "\n"
            
            print(log_str, end="")  # print to console
            FILE.write(log_str)     # write a log entry
            print("Ctrl+C to stop", end="\r")   # floating message

            time.sleep(2)   # 2 sec timeout

    except KeyboardInterrupt:   # Ctrl+C
       print("              ")  # overwrite last line w/ spaces
       
       # calculate success/failure percentages
       uptime_pct = 100 * (ping_ok / ping_count)
       fail_pct = 100 * ((ping_count - ping_ok) / ping_count)
       
       # calculate stats and print/log them
       stats = f"UPTIME STATS: Host {ip_addr} was up {round(uptime_pct)}% of the time\n"
       print(stats, end="") # print stats
       FILE.write(stats)    # log stats

       # packet count stats
       stats = f"\tPackets sent: {ping_count}\n" + \
               f"\tPackets received: {ping_ok}\n" + \
               f"\tPackets lost: {ping_count - ping_ok}\n"
       print(stats, end="")
       FILE.write(stats)   # log success stats


       stats = f"({fail_pct}% pings failed)\n"
       if fail_pct > 0: # if any pings failed
         print(stats, end="")   # print the stats
         FILE.write(stats)      # log the stats
       
       FILE.close()    # close the file stream
    
    except:     # catch-all exception handling
       FILE.close()    # close the file stream (if still open)

  # git to ze choppa
  else: print("Invalid IP detected. Please try again.")
else: print("Invalid number of arguments. Please make sure the script has exactly one argument.")

print("\n^^^ Uptime monitor v1 - crafted by Paul Stroud ^^^")


# le goodbye