#!/usr/bin/python3

# Script: Ops 401 Class 12 script
# Author: Paul Stroud
# Date of latest revision: 05/02/23
# Purpose: Network Scanner pt2
# Resources used: Alex White, google, stackoverflow, github demo, chatgpt

# MAIN REQS:
# Add the following features to your Network Security Tool:

# User menu prompting choice between TCP Port Range Scanner mode and ICMP Ping Sweep mode, with the former leading to yesterday’s feature set
# ICMP Ping Sweep tool
# Prompt user for network address including CIDR block, for example “10.10.0.0/24”
# Careful not to populate the host bits!

# Create a list of all addresses in the given network
# Ping all addresses on the given network except for network address and broadcast address
# If no response, inform the user that the host is down or unresponsive.
# If ICMP type is 3 and ICMP code is either 1, 2, 3, 9, 10, or 13 then inform the user that the host is actively blocking ICMP traffic.
# Otherwise, inform the user that the host is responding.
# Count how many hosts are online and inform the user.


import os     # for root access check
import sys    # for sys.exit() to kill the script
import random # for random num gen
from scapy.all import ICMP, IP, sr1, TCP  # import relevant tools from scapy
import ipaddress  # to work w/ IP addresses
import time   # for time.sleep() timeout


import logging  # to eliminate "WARNING" messages from scapy

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # change log level to errors only



# check for admin access
print("ROOT ACCESS CHECK: ", end="")
if os.geteuid() == 0: print("OK")
else:
    print("FAIL\nPlease run this script as root/sudo")
    sys.exit()


# menu loop
while True:
    time.sleep(1)
    print("\n>>> Net Scanner v2.0 <<<")
    print("Select the mode:" \
          "\n   1. TCP Port Range Scanner" \
          "\n   2. ICMP Ping Sweep" \
          "\n   0. Exit")

    mode = -1  # holds user input
    while not (mode >= 0 and mode <= 2):
      try:
         mode = int(input("Enter a menu option (0-2): "))
      except KeyboardInterrupt:   # Ctrl+C
         print()
         sys.exit()
      except: # catch all for anything other than 1-5 or Ctrl+C
         print("Invalid input. Please try again.")

    if mode == 0:
      print("Exiting the script...")
      sys.exit()  # kill the script
    else:
      if mode == 1:   # TCP Port Range Scanner
        # generate random source port
        src_port = random.randrange(10000, 50000)

        # ports to scan
        port_range = [21, 22, 23, 69, 80, 123, 161, 443, 445, 995, 3389]

        # read target IP from user input; otherwise use default
        host = input('Enter the IP address or domain name to scan (default = scanme.nmap.org)): ')
        host = "scanme.nmap.org" if (host == "") else host

        print(f"Scanning {host}: ")
        for dst_port in port_range: # scan each port from the list
          # send a TCP SYN packet to the target
          response = sr1(IP(dst=host)/TCP(sport=src_port, dport=dst_port, flags="S"), timeout=1, verbose=0)

          if(response == None): # if request timed out
            print(f"   Port {dst_port} timed out")

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

 
      if mode == 2:   # ICMP Ping Sweep

        cidr = input('Enter a CIDR network address (default = 192.168.1.0/24)): ')
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
               print("Host is up")
               up_count += 1
        
        print(f"STATS: {up_count}/{ip_count} hosts are up on {cidr}")


# end of script