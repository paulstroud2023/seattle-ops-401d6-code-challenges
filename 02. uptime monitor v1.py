#!/usr/bin/python3


# Script: Ops 401 Class 02 script
# Author: Paul Stroud
# Date of latest revision: 04/18/23
# Purpose: Uptime monitoring script


import sys, os, datetime, time, re, subprocess

# define the IP address regex
ip_regex = "^(\d{1,3}\.){3}\d{1,3}$"  
# could also use ^([0-9]{1,3}\.){3}[0-9]{1,3}$
# both regex checks for a string that contains 3x groups of 1-3 numbers
# where each decimal digit is between 0-9
# the groups are separated by a '.'
# the string ends with another group of 1-3 digits between [0-9]



def IP_validation(addr):    # validates IP address
    if re.match(ip_regex, addr): # regex match ok?
       return True
    else: return False


#print(f"The script has {len(sys.argv) - 1} args\narg[0]={sys.argv[0]}")



###### MAIN CODE BELOW ########

if len(sys.argv) == 2:  # is there a script arg?
  ip_addr = sys.argv[1]

  if IP_validation(ip_addr):    # verify the IP is valid, otherwise abort
    # do useful stuff
    print(f"[ Monitoring uptime for: {ip_addr} ]")
    
    ping_count = 0
    ping_ok = 0

    try:
        while True:
            ping_result = subprocess.run(["ping", "-c 1", ip_addr], capture_output=True, text=True)
            ping_ok += 0 if ping_result.returncode else 1
            ping_count += 1
            print(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), ">", f"Host {ip_addr} is",
                "DOWN" if ping_result.returncode else "UP") #, "\n", ping_result.stdout)
            print("Ctrl+C to stop", end="\r")
            time.sleep(2)
    except KeyboardInterrupt:
       print("              ")
       uptime_pct = 100 * (ping_ok / ping_count)
       fail_pct = 100 * ((ping_count - ping_ok) / ping_count)
       print(f"UPTIME STATS: Host {ip_addr} was up {round(uptime_pct)}% of the time")
       if fail_pct > 0: print(f"({fail_pct}% pings failed)")
  else: print("Invalid IP detected. Please try again.")


# if len(sys.argv) == 1:
#     # The script has command-line arguments
#     print("YES")
# else:
#     # The script has no command-line arguments
#     print("NO")

# - Transmit a single ICMP (ping) packet to a specific IP every two seconds.
# - Evaluate the response as either success or failure.
# - Assign success or failure to a status variable.
# - For every ICMP transmission attempted, print the status variable along with a comprehensive timestamp and destination IP tested.
#     Example output: 2020-10-05 17:57:57.510261 Network Active to 8.8.8.8

# Stretch Goals (Optional Objectives)
# - Save the output to a text file as a log of events.
# - Accept user input for target IP address.





# print("badabing badaboom")










# do { # input validation loop
#     $timeout = Read-Host "Enter the screen lock timeout (in seconds)"
#    } while (-not [int]::TryParse($timeout, [ref]$null))    # is it an int?
   

# # change the screen lock timeout
# $setting = "InactivityTimeoutSecs"  # registry value to edit
# # path to the autorun key
# $keyPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" 
# # change the registry key
# Set-ItemProperty -Path $keyPath -Name $setting -Value $timeout -Force | Out-Null
# Write-Host "Applying the new setting... "
# gpupdate /force

# # notify the user
# Write-Host "Changed screen lock timeout to $timeout seconds."
# Write-Host "The new setting will take effect after a restart."
# Write-Host "Please save any open files and close all programs...`n"     # add newline
# sleep(2)    # pause for 2 sec
# Read-Host "Press any key to continue and restart the computer (Ctrl+C to abort)"

# Restart-Computer -Force


# End