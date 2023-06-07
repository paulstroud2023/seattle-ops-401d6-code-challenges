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
import re           # for regex matching


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



url_regex = r'^([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,}$'
ip_regex = r'^(\d{1,3}\.){3}\d{1,3}$'
port_regex = r'^\d{1,5}$'
wk_ports = (21, 22, 23, 25, 53, 67, 69, 80, 110, 123, 137, 139, 169, 443, 465, 514, 3389)   # well-known ports

#### MAIN ####

# validate the API key arg

if len(sys.argv) < 3:
  print("ERROR: Please provide the IP/URL and port number as script arguments.")
  sys.exit()

addr = sys.argv[1]
port = sys.argv[2]

print("port: ", port, bool(re.match(port_regex, port)))
print("IP: ", addr, bool(re.match(ip_regex, addr)))
print("URL: ", addr, bool(re.match(url_regex, addr)))

option = ""

try: 
    test = subprocess.check_output(["telnet", addr, port], timeout=5, text=True)
except:
    pass
print(test.stdout)

sys.exit()     

# os_name = platform.system()   # get the OS name
# if not (os_name == "Linux" or os_name == "Windows"):
#     print("ERROR: Unknown OS. Exiting...")  # doesn't like apples
# print(f"OS = {os_name}")


# dir = input("Enter the full dir path to search (current dir if empty) : ")
# #dir = "/home/user/TEST"
# dir = dir if dir != '' else os.getcwd() # if no input, use PWD from the OS


# total_files = 0     # all files in the dir/subdirs
# mal_files = 0       # detected malware counter

# print(f"\n[ Contents of {dir}: ]")

# hash_array = []     # 2D array to hold checksums and other file metadata
# tab = "  "          # constant for tabbing out text
# dtab = ""           # indent for dir names
# ftab = tab          # indent for file names
# for rootdir, subdirs, files in os.walk(dir):    # recursively parse the dir
#     total_files += len(files)                   # count all files

#     print(f"{dtab}{rootdir}/")                  # print the dir name
#     if not files: print(ftab + "<no files>")    # if dir is empty
#     else:                                       # if there are files in this dir
#         for i in files:
#             print(f"{ftab}- {i}")                                                   # print file names in a list
#             full_path = f'{rootdir}/{i}'                                            # add extra '/' for the full file path
#             cur_time = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")          # format date/time
#             filesize = os.path.getsize(full_path)                                   # get file size
#             hash = sha1_chksum(full_path)                                           # calc SHA1 hash
#             virus = malware_check(api_key, hash)                                    # send hash to VirusTotal
#             if virus[0] == 1: mal_files += 1                                        # count malware
#             hash_array.append([i, hash, virus[1], cur_time, fmt_fsize(filesize), full_path])  # add all data to the array
#     dtab += tab     # increase dir indent
#     ftab += tab     # increase file indent


# # test_hash = "77fed3357bf22385a18f5ab4008753cba324cce3"
# # hash_array.append(["malware.test", test_hash, malware_check(api_key, test_hash)[1], cur_time, "200 TB", "/some/where/else/malware.test"])
# # mal_files += 1


# ### REQ: Print the variable to the screen along with a timestamp, 
# ###      file name, file size, and complete (not symbolic) file path.
# columns = [ "FILE NAME", "SHA1 HASH", "MALWARE", "DATE/TIME", "FILE SIZE", "FILE LOCATION" ]
# column_width = []   # holds column widths for output formatting
# for i in range(len(columns)):
#    # calc the correct width for the largest text in the column + 3 extra chars for whitespace
#    column_width.append(max(max(len(row[i]) for row in hash_array), len(columns[i]))+3)

# # pre-format output with proper spacing for column names
# output = f"{columns[0]:<{column_width[0]}}" \
#          f"{columns[1]:<{column_width[1]}}" \
#          f"{columns[2]:<{column_width[2]}}" \
#          f"{columns[3]:<{column_width[3]}}" \
#          f"{columns[4]:<{column_width[4]}}" \
#          f"{columns[5]}"
# print(f'\n{output}')

# for i in range(len(hash_array)):    # iterate over the array
#    # pre-format output with proper spacing for each column
#    output = f"{hash_array[i][0]:<{column_width[0]}}" \
#             f"{hash_array[i][1]:<{column_width[1]}}" \
#             f"{hash_array[i][2]:<{column_width[2]}}" \
#             f"{hash_array[i][3]:<{column_width[3]}}" \
#             f"{hash_array[i][4]:<{column_width[4]}}" \
#             f"{hash_array[i][5]}"
#    print(output)

# # more numbers
# print(f"\n[ SCRIPT STATS for {dir}]")
# print(f'  Potential malware:\t{mal_files}')
# print(f'  Total files scanned:\t{total_files}')

# le end