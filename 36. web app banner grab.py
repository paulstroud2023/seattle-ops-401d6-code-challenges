#!/usr/bin/python3

# Script: Ops 401 Class 36 script
# Author: Paul Stroud
# Date of latest revision: 06/06/23
# Purpose: Web Application Fingerprinting / Banner Grabbing
# Resources used: google, stackoverflow, github demo, chatgpt

# MAIN REQS:
# In Python create a script that executes from a Linux box to perform the following:
#   Prompts the user to type a URL or IP address.
#   Prompts the user to type a port number.
#   Performs banner grabbing using netcat against the target address at the target port; prints the results to the screen then moves on to the step below.
#   Performs banner grabbing using telnet against the target address at the target port; prints the results to the screen then moves on to the step below.
#   Performs banner grabbing using Nmap against the target address of all well-known ports; prints the results to the screen.

import platform     # to get OS name
import os           # for os.walk() recursive directory list
import hashlib      # to calc hashes
import datetime     # to get date/time
import math         # for math functions (floor, log, pow)
import time         # for time() and sleep()
import sys          # for sys.exit
import requests     # to parse HTTP requests

import subprocess
import socket
import re           # for regex matching


### GLOBAL VARS ###

url_regex = r'^([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,}$'
ip_regex = r'^(\d{1,3}\.){3}\d{1,3}$'
port_regex = r'^\d{1,5}$'
wk_ports = (21, 22, 23, 25, 53, 67, 69, 80, 110, 123, 137, 139, 169, 443, 465, 514, 3389)   # well-known ports




### FUNCTIONS ####

# runs a timer and prints the seconds/countdown
# the number is updated in place
def timeout(timer):
    wspace1 = 0     # prev digit counter; init the var for use in the loop
    for i in range(timer, 0, -1):
       print(i, end='', flush=True)     # "flush=True" to display immediately (could hang otherwise)
       wspace = len(str(i)) # number of digits in i
       # if fewer digits than last loop, print an extra space
       if wspace < wspace1: print(' \b', end='', flush=True)    
       time.sleep(1)
       print('\b' * wspace, end='', flush=True) # erase the number
       wspace1 = wspace     # save value for the next loop



def net_conn(cmd, addr, port, opt=''):
  skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # IPv4 TCP connection
  skt.connect((addr, int(port)))
  print("Netcat...")

  #sneding the netcat command
  opt = opt if opt == '' else opt+' '
  cmd_str = f"{cmd} {opt}{addr} {port}"
  input(cmd_str)
  skt.sendall(cmd_str.encode())
  time.sleep(.5)
  skt.shutdown(socket.SHUT_WR)

  # Repsonse placeholder
  output = ""

  # Convert the data that we received
  while True:
    data = skt.recv(1024)
    if(not data):
      break
    output += data.decode()

  print(output)
  #close the connection
  skt.close()



#### MAIN ####

if len(sys.argv) < 3:
  print("ERROR: Please provide the IP/URL and port number as script arguments.")
  sys.exit()

addr = sys.argv[1]
port = sys.argv[2]

print("port: ", port, bool(re.match(port_regex, port)))
print("IP: ", addr, bool(re.match(ip_regex, addr)))
print("URL: ", addr, bool(re.match(url_regex, addr)))

net_conn("telnet", addr, port)
net_conn("nc", addr, port)
net_conn("nmap", addr, port, opt="-O -V")

sys.exit()     
