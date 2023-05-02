#!/usr/bin/python3

# Script: Ops 401 Class 11 script
# Author: Paul Stroud
# Date of latest revision: 05/02/23
# Purpose: Network Scanner pt1
# Resources used: Alex White, google, stackoverflow, github demo, chatgpt

# MAIN REQS:
# In Python, create a TCP Port Range Scanner that tests whether a TCP port is open or closed. The script must:
# - Utilize the scapy library
# - Define host IP
# - Define port range or specific set of ports to scan
# - Test each port in the specified range using a for loop
# - If flag 0x12 received, send a RST packet to graciously close the open connection. Notify the user the port is open.
# - If flag 0x14 received, notify user the port is closed.
# - If no flag is received, notify the user the port is filtered and silently dropped.

# OPTIONAL REQS: (aka Stretch Goals)
# - Utilize the random library
# - Randomize the TCP source port in hopes of obfuscating the source of the scan



import os     # for root access check
import sys    # for sys.exit() to kill the script
import random # for random num gen
from scapy.all import ICMP, IP, sr1, TCP  # import relevant tools from scapy


# check for admin access
print("ROOT ACCESS CHECK: ", end="")
if os.geteuid() == 0: print("OK")
else:
    print("FAIL\nPlease run this script as root/sudo")
    sys.exit()

# read target IP from an arg; otherwise use default
if len(sys.argv) == 2: host = sys.argv[1] 
else: host = "scanme.nmap.org"

# generate random source port
src_port = random.randrange(10000, 50000)



# ports to scan
port_range = [21, 22, 23, 69, 80, 123, 161, 443, 445, 995, 3389]

print(f"Scanning {host}: ")
for dst_port in port_range: # scan each port from the list
  # send a TCP SYN packet to the target
  response = sr1(IP(dst=host)/TCP(sport=src_port, dport=dst_port, flags="S"), timeout=1, verbose=0)

  if(response == None): # if request timed out
    print(f"   Port {dst_port} timed out.")

  elif(response.haslayer(TCP)): # valid response received?
    # SYN/ACK flag, port open
    if(response.getlayer(TCP).flags == 0x12): 
      print(f'   Port {dst_port} is OPEN')
      # send RST flag to close the connection
      sr1(IP(dst=host)/TCP(sport=src_port, dport=dst_port, flags="R"), timeout=1, verbose=0)
    # ACK/RST flag, port closed
    if(response.getlayer(TCP).flags == 0x14): print(f'   Port {dst_port} is CLOSED')
    # no flags, port filtered
    if(response.getlayer(TCP).flags == 0x00): print(f'   Port {dst_port} is FILTERED')


print("\nScript complete!")

# # ze end