#!/usr/bin/python3


# Script: Ops 401 Class 06 script
# Author: Paul Stroud
# Date of latest revision: 04/24/23
# Purpose: Uptime monitoring script v2


# MAIN REQS:
# In Python, create a script that utilizes the cryptography library to:
  # Prompt the user to select a mode: 
    # Encrypt a file (mode 1)
    # Decrypt a file (mode 2)
    # Encrypt a message (mode 3)
    # Decrypt a message (mode 4)
  # If mode 1 or 2 are selected, prompt the user to provide a filepath to a target file.
  # If mode 3 or 4 are selected, prompt the user to provide a cleartext string.
# Depending on the selection, perform one of the below functions. You’ll need to create four functions:
  # Encrypt the target file if in mode 1. 
    # Delete the existing target file and replace it entirely with the encrypted version.
  # Decrypt the target file if in mode 2. 
    # Delete the encrypted target file and replace it entirely with the decrypted version.
  # Encrypt the string if in mode 3. 
    # Print the ciphertext to the screen.
  # Decrypt the string if in mode 4. 
    # Print the cleartext to the screen.



import sys          # for parsing script args
# import datetime     # to access and format date/time
# import time         # for timeout/sleep
# import re           # for regex
# import subprocess   # for running bash commands

# import smtplib      # to send emails via SMTP
# from email.message import EmailMessage  # to craft emails
# import os           # to verify if file exists


from cryptography.fernet import Fernet


###### FUNCTIONS ########

# save a cryptographic key
def save_cryptokey(name = "401.06.key"):
    keyfile = open(name, "wb")
    keyfile.write(Fernet.generate_key())

def load_cryptokey(name = "401.06.key"):
    return open(name, "rb").read()

def encrypt_file(name):
    enc_name = name + ".enc"
    

# def decrypt_file():

# def encrypt_msg():


# def decrypt_msg():


# menu loop
while True:
    print("[ Encryption Utility v1.0 ]")
    print("Select the operation to perform:")
    print("\t1. Encrypt a file")
    print("\t2. Decrypt a file")
    print("\t3. Encrypt a message")
    print("\t4. Decrypt a message")
    print("\t5. Exit")
    op = 0
    while not (op >= 1 and op <= 5):
      try:
         op = int(input("Enter a menu option (1-5): "))
      except KeyboardInterrupt: exit
      except:
         print("Invalid input. Please try again.")

    if op == 5:
       print("Exiting the script...")
       sys.exit()
print("BOOM")
input()



print (Fernet.generate_key())


