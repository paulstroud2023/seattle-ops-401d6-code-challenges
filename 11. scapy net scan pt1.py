#!/usr/bin/python3

# Script: Ops 401 Class 08 script
# Author: Paul Stroud
# Date of latest revision: 05/01/23
# Purpose: Network Scanner pt1
# Resources used: google, stackoverflow, github demo, chatgpt


# Requirements
# In Python, create a TCP Port Range Scanner that tests whether a TCP port is open or closed. The script must:

# Utilize the scapy library
# Define host IP
# Define port range or specific set of ports to scan
# Test each port in the specified range using a for loop
# If flag 0x12 received, send a RST packet to graciously close the open connection. Notify the user the port is open.
# If flag 0x14 received, notify user the port is closed.
# If no flag is received, notify the user the port is filtered and silently dropped.
# Stretch Goals (Optional Objectives)
# Utilize the random library
# Randomize the TCP source port in hopes of obfuscating the source of the scan


import scapy.all

#!/usr/bin/python3

# Utilize the scapy library
from scapy.all import ICMP, IP, sr1, TCP

# Define host IP
host = "scanme.nmap.org"
# Define port range or specific set of ports to scan
port_range = [22, 23, 80, 443, 3389]
# Test each port in the specified range using a for loop
for dst_port in port_range:
  src_port = 1025
  response = sr1(IP(dst=host)/TCP(sport=src_port, dport=dst_port,flags="S"), timeout=1, verbose=0)
  # print(response.summary) # a little info
  # print(response.show()) # A LOT OF INFO
  # If flag 0x12 received, send a RST packet to graciously close the open connection. Notify the user the port is open.
  if(response.haslayer(TCP)):
    if(response.getlayer(TCP).flags == 0x12):
      print("TA DA")
      # PORT IS OPEN!!
  # If flag 0x14 received, notify user the port is closed.
  # If no flag is received, notify the user the port is filtered and silently dropped.1







#! /usr/bin/env python

import sys
from scapy.all import sr1,IP,ICMP

p=sr1(IP(dst=sys.argv[1])/ICMP())
if p:
    p.show()






#! /usr/bin/env python3

# Run this with sudo

from scapy.all import ICMP, IP, sr1, TCP

# Define target host and TCP port to scan
host = "scanme.nmap.org"
port_range = 22
src_port = 22
dst_port = 22

response = sr1(IP(dst=host)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=1,verbose=0)

print(response)


#### END DEMO


# print("Script complete!")

# # ze end