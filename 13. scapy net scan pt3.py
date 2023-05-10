#!/usr/bin/python3

# Script: Ops 401 Class 13 script
# Author: Paul Stroud
# Date of latest revision: 05/03/23
# Purpose: Network Scanner pt3
# Resources used: Alex White, google, stackoverflow, github demo, chatgpt

# MAIN REQS:
# Objectives
# The final iteration of your network scanning tool will perform the following:

# Ping an IP address determined by the user.
# If the host exists, scan its ports and determine if any are open.
# Tasks
# Here’s a general outline of how to achieve the desired outcome.

# In Python, combine the two modes (port and ping) of your network scanner script.
# Eliminate the choice of mode selection.
# Continue to prompt the user for an IP address to target.
# Move port scan to its own function.
# Call the port scan function if the host is responsive to ICMP echo requests.
# Print the output to the screen.

import os     # for root access check
import sys    # for sys.exit() to kill the script
import random # for random num gen
from scapy.all import ICMP, IP, sr1, TCP  # import relevant tools from scapy
import ipaddress  # to work w/ IP addresses
#import time   # for time.sleep() timeout

import logging  # to eliminate "WARNING" messages from scapy

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # change log level to errors only

### FUNCTIONS ####

def tcp_port_scan(host, tab='\t'):
    # generate random source port
    src_port = random.randrange(10000, 50000)

    # ports to scan
    port_range = [21, 22, 23, 69, 80, 123, 161, 443, 445, 995, 3389]

    print(f"{tab}Scanning {host}: ")
    for dst_port in port_range: # scan each port from the list
      # send a TCP SYN packet to the target
      response = sr1(IP(dst=host)/TCP(sport=src_port, dport=dst_port, flags="S"), timeout=1, verbose=0)

      if(response == None): # if request timed out
        print(f"{tab}  Port {dst_port} timed out")

      elif(response.haslayer(TCP)): # valid response received?
        # SYN/ACK flag, port open
        if(response.getlayer(TCP).flags == 0x12): 
          print(f'{tab}  Port {dst_port} is OPEN')
          # send RST flag to close the connection
          sr1(IP(dst=host)/TCP(sport=src_port, dport=dst_port, flags="R"), timeout=1, verbose=0)
        # ACK/RST flag, port closed
        if(response.getlayer(TCP).flags == 0x14): print(f'{tab}  Port {dst_port} is CLOSED')
        # no flags, port filtered
        if(response.getlayer(TCP).flags == 0x00): print(f'{tab}  Port {dst_port} is FILTERED')



#### MAIN ####

# check for admin access
print("ROOT ACCESS CHECK: ", end="")
if os.geteuid() == 0: print("OK")
else:
    print("FAIL\nPlease run this script as root/sudo")
    sys.exit()


print("\n>>> Net Scanner v3.0 <<<")

cidr = input('Enter a CIDR network (default = 192.168.1.0/24)): ')
cidr = "192.168.1.0/24" if (cidr == "") else cidr

# display network info - net addr, broadcast, subnet mask
print(f"  Net info for {cidr}:")
net = ipaddress.IPv4Network(cidr)
print("\tNetwork address: ", net.network_address)
print("\tBroadcast address: ", net.broadcast_address)
print("\tSubnet mask: ", net.netmask)

up_count = 0
ip_count = 0
for ip in net.hosts():
    ip_count += 1
    ip_str = str(ip)
    print(f'  Ping to {ip_str}: > ', end='')
    ping_reply = sr1(IP(dst=ip_str)/ICMP(), timeout=1, verbose=0)

    if ping_reply == None: print("Host down / No response")
    else: 
      if (ping_reply.getlayer(ICMP).type == 3 and ping_reply.getlayer(ICMP).code in [1, 2, 3, 9, 10, 13]):
        print("Host is blocking ICMP traffic")
      else: 
        print("Host is UP")
        tcp_port_scan(ip_str)
        up_count += 1

print(f"STATS: {up_count}/{ip_count} hosts are up on {cidr}")

# end of script