# Script: Ops 401 Class 01 script
# Author: Paul Stroud
# Date of latest revision: 04/18/23
# Purpose: Automation of SOC2-compliant configuration


# Main

do { # input validation loop
    $timeout = Read-Host "Enter the screen lock timeout (in seconds)"
   } while (-not [int]::TryParse($timeout, [ref]$null))    # is it an int?
   

# change the screen lock timeout
$setting = "InactivityTimeoutSecs"  # registry value to edit
# path to the autorun key
$keyPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" 
# change the registry key
Set-ItemProperty -Path $keyPath -Name $setting -Value $timeout -Force | Out-Null
Write-Host "Applying the new setting... "
gpupdate /force

# notify the user
Write-Host "Changed screen lock timeout to $timeout seconds."
Write-Host "The new setting will take effect after a restart."
Write-Host "Please save any open files and close all programs...`n"     # add newline
sleep(2)    # pause for 2 sec
Read-Host "Press any key to continue and restart the computer (Ctrl+C to abort)"

Restart-Computer -Force


# End