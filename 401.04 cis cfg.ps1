# check for admin privileges
if (([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))
  { Write-Host "ADMIN ACCESS CHECK: OK" } # confirm admin privileges
 else # if no admin access, print to console and exit
  {
   Write-Host "ADMIN ACCESS CHECK: FAIL" 
   Write-Host "Please run this script as administrator"
   Exit
  }


# CIS benchmark 1.1.5 (L1)
# change the "Password must meet complexity requirements" setting
set-ItemProperty -path "HKLM:\SYSTEM\CurrentControlSet\Services\Netlogon\Parameters\" -name "RequireStrongKey" -value 1


# CIS benchmark 18.3.2 (L1)
# change the 'Do not allow password expiration time longer than required by policy" setting
set-ItemProperty -path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\" -name "PasswordExpiryWarning" -value 30

