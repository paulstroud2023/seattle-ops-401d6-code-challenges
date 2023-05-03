#!/usr/bin/python3

# Script: Ops 401 Class 12 script
# Author: Paul Stroud
# Date of latest revision: 05/02/23
# Purpose: Network Scanner pt1
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

 
      if mode == 2:   # ICMP Ping Sweep
        # Declare Variables
        # ip = "127.0.0.1"
        # myIp = "10.0.0.68"
        # host = "scanme.nmap.org"
        # network = '10.0.0.1/24'

        # ----- Initialize an IPv4Address! -----
        # ip4 = ipaddress.IPv4Address(ip)
        # print(ip4.is_multicast)
          # Print True if the IP address is a loopback address.
        # print("Is loopback: ", ip4.is_loopback)

        # read target IP from user input; otherwise use default
        net = input('Enter a CIDR network address (default = 192.168.1.0/24)): ')
        net = "192.168.1.0/24" if (net == "") else net


        # ----- Initialize an IPv4Network() -----
        ip4Network = ipaddress.IPv4Network(net)
        # Print the network address of the network.
        print("Network address of the network: ", ip4Network.network_address)

          # Print the broadcast address
        print("Broadcast address: ", ip4Network.broadcast_address)

          # Print the network mask.
        print("Network mask: ", ip4Network.netmask)

        for ip in ip4Network.hosts():
           print(f'{ip} > ', end='')
           response = sr1(IP(dst=ip)/ICMP(), timeout=1, verbose=0)

           # If the response is empty, then the host is down
           if response is None:
             print("Host down")

           # Check for ICMP codes
           elif response.haslayer(ICMP):
             print(response.getlayer(ICMP).code) # now compare the reutnred code to 1, 2, 3, 9, 10, or 13.
                # Then the host is actively blocking ICMP traffic.
                # How do you cast to Integer in Python? String ->(cast) Integer "2" X 2 => int("2")
            # if no codes and reponse is good, host is up and responding! sebnd a RST(reset)


print("\nScript complete!")

# end of script