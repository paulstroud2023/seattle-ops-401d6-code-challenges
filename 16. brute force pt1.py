#!/usr/bin/python3

# Script: Ops 401 Class 16 script
# Author: Paul Stroud
# Date of latest revision: 05/08/23
# Purpose: Brute force pt1
# Resources used: google, stackoverflow, github demo, chatgpt

# MAIN REQS:
# In Python, create a script that prompts the user to select one of the following modes:

# Mode 1: Offensive; Dictionary Iterator

# Accepts a user input word list file path and iterates through the word list, assigning the word being read to a variable.
# Add a delay between words.
# Print to the screen the value of the variable.
# Mode 2: Defensive; Password Recognized

# Accepts a user input string.
# Accepts a user input word list file path.
# Search the word list for the user input string.
# Print to the screen whether the string appeared in the word list.









import os     # for root access check
import sys    # for args and sys.exit() to kill the script
# import random # for random num gen
# from scapy.all import ICMP, IP, sr1, TCP  # import relevant tools from scapy
#import time   # for time.sleep() timeout


### FUNCTIONS ####



#### MAIN ####

# check for admin access
print("ROOT ACCESS CHECK: ", end="")
if os.geteuid() == 0: print("OK")
else:
    print("FAIL\nPlease run this script as root/sudo")
    sys.exit()


print("\n>>> Brute Force Tool v1.0 <<<")

# end of script