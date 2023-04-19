# Script: Ops 401 Class 02 script
# Author: Paul Stroud
# Date of latest revision: 04/18/23
# Purpose: Uptime monitoring script


# Main

import os, datetime, time

# - Transmit a single ICMP (ping) packet to a specific IP every two seconds.
# - Evaluate the response as either success or failure.
# - Assign success or failure to a status variable.
# - For every ICMP transmission attempted, print the status variable along with a comprehensive timestamp and destination IP tested.
#     Example output: 2020-10-05 17:57:57.510261 Network Active to 8.8.8.8

# Stretch Goals (Optional Objectives)
# - Save the output to a text file as a log of events.
# - Accept user input for target IP address.

print("badabing badaboom")










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