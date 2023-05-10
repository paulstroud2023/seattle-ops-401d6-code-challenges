#!/usr/bin/python3

# Script: Ops 401 Class 06 script
# Author: Paul Stroud
# Date of latest revision: 04/24/23
# Purpose: File encryption pt1


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



import sys          # for breaking out of the script
import time         # for timeout/sleep
import os           # to verify if file exists

from cryptography.fernet import Fernet  # for encryption/decryption


###### FUNCTIONS ########

# save cryptographic key to a file
def save_cryptokey(name):
    keyfile = open(name, "wb")
    keyfile.write(Fernet.generate_key())

# load cryptographic key from a file
def load_cryptokey(name):
    return open(name, "rb").read()


# encrypt a file using the given crypto key
def encrypt_file(name, key):
    enc_name = name + ".enc"                # encrypted file name
    cleartext = open(name, "rb").read()     # read the source file
    ciphertext = Fernet(key).encrypt(cleartext) # encrypt the data
    open(enc_name, "wb").write(ciphertext)  # write out to a new file

    # prompt the user to delete the original file (default is yes)
    while True:
      cln = input(f"Delete the original file {name}?  (Y/n): ")
      if cln == "y" or cln == "Y" or cln == "":
        os.remove(name) # nuke the file
        break           # break the loop
      if cln == "n" or cln == "N": break  # break the loop without deleting
    

# decrypt a file using the given crypto key
def decrypt_file(name, key):
    dec_name = name.split(".enc")[0]      # extract decrypted file name
    ciphertext = open(name, "rb").read()  # read the source file
    cleartext = Fernet(key).decrypt(ciphertext) # decrypt the data
    open(dec_name, "wb").write(cleartext) # write out to a new file

    # prompt the user to delete the original file (default is yes)
    while True:
      cln = input(f"Delete the original file {name}?  (Y/n): ")
      if cln == "y" or cln == "Y" or cln == "":
        os.remove(name) # nuke the file
        break           # break the loop
      if cln == "n" or cln == "N": break  # break the loop without deleting



# encrypt a plaintext message string
def encrypt_msg(msg, key):  # `msg` is a string, `key` is the crypto key file
    # encode plaintext string as bytes
    # create a new crypto/Fernet obj to encrypt the encoded string
    # decode the ciphertext back into a string and return the result
    return Fernet(key).encrypt(msg.encode()).decode('utf-8')

# decrypt a ciphertext message string
def decrypt_msg(msg, key): # `msg` is a string, `key` is the crypto key file
    # encode ciphertext string as bytes
    # create a new crypto/Fernet obj to decrypt the encoded string
    # decode the plaintext back into a string and return the result
    return Fernet(key).decrypt(msg.encode()).decode('utf-8')
   

###### MAIN CODE ########

key_name = input('Enter the crypto key name ("401.06.key" is default): ')
key_name = "401.06.key" if (key_name == "") else key_name  # if nothing entered, use the default key name

# if key file doesn't exist, create a new one
if not os.path.exists(key_name):
   print(f"Creating a new key {key_name}... ", end="")
   save_cryptokey(key_name)
   print("DONE")

# load the key from the file
print(f"Loading {key_name}... ", end="")
key = load_cryptokey(key_name)
print("DONE")


# menu loop
while True:
    time.sleep(1)
    print("\n>>> Encryption Utility v1.0 <<<")
    print("Select the operation to perform:")
    print("\t1. Encrypt a file")
    print("\t2. Decrypt a file")
    print("\t3. Encrypt a message")
    print("\t4. Decrypt a message")
    print("\t5. Exit")

    op = 0  # holds user input
    while not (op >= 1 and op <= 5):
      try:
         op = int(input("Enter a menu option (1-5): "))
      except KeyboardInterrupt:   # Ctrl+C
         print()
         sys.exit()
      except: # catch all for anything other than 1-5 or Ctrl+C
         print("Invalid input. Please try again.")

    if op == 5:
      print("Exiting the script...")
      sys.exit()  # kill the script
    else:
      if op == 1:   # encrypt a file
        try:
            fname = input("Enter the file to encrypt: ")
            encrypt_file(fname, key)
            print(f"Encrypted file saved as {fname}.enc")
        except FileNotFoundError: print(f"File {fname} does not exist")

      if op == 2:   # decrypt a file
        try:
            fname = input("Enter the file to decrypt: ")
            decrypt_file(fname, key)
            print(f"Decrypted file saved as {fname.split('.enc')[0]}")
        except FileNotFoundError: print(f"File {fname} does not exist")

      if op == 3:   # encrypt a string
        plain = input("Enter the message to encrypt: ")
        cipher = encrypt_msg(plain, key)
        print(f"Encrypted message: {cipher}")

      if op == 4:   # decrypt a file
        cipher = input("Enter the message to decrypt: ")
        plain = decrypt_msg(cipher, key)
        print(f"Decrypted message: {plain}")

print("Script complete!")

# ze end