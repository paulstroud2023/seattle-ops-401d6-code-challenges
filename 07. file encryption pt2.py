#!/usr/bin/python3

# Script: Ops 401 Class 07 script
# Author: Paul Stroud
# Date of latest revision: 04/25/23
# Purpose: File encryption pt2


# MAIN REQS:
# Add a feature capability to your script to:
#   Recursively encrypt a single folder and all its contents.
#   Recursively decrypt a single folder that was encrypted by this tool.



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


# encrypt a file using the given crypto key (v2.0)
def encrypt_file(name, key, force="n"):
    enc_name = name + ".enc"                # encrypted file name
    cleartext = open(name, "rb").read()     # read the source file
    ciphertext = Fernet(key).encrypt(cleartext) # encrypt the data
    open(enc_name, "wb").write(ciphertext)  # write out to a new file

    if force == "y":  # quietly delete the file and stop the function
       os.remove(name)
       return
    
    # prompt the user to delete the original file (default is yes)
    while True:
      cln = input(f"Delete the original file {name}?  (Y/n): ")
      if cln == "y" or cln == "Y" or cln == "":
        os.remove(name) # nuke the file
        break           # break the loop
      if cln == "n" or cln == "N": break  # break the loop without deleting
    

# decrypt a file using the given crypto key (v2.0)
def decrypt_file(name, key, force="n"):
    dec_name = name.split(".enc")[0]      # extract decrypted file name
    ciphertext = open(name, "rb").read()  # read the source file
    cleartext = Fernet(key).decrypt(ciphertext) # decrypt the data
    open(dec_name, "wb").write(cleartext) # write out to a new file

    if force == "y":  # quietly delete the file and stop the function
       os.remove(name)
       return

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
   

# get a list of all files in a dir
# the list will have full path + filename for each file
def list_dir(dir_name):
    filelist = [] # list to hold file names
    # use os.walk to recursively parse the directory
    for root, dirs, files in os.walk(dir_name):
    # create a full filename w/ path, append to filelist
      for file in files:
         filelist.append(os.path.join(root, file))
    return filelist



###### MAIN CODE ########

key_name = input('Enter the crypto key name ("401.07.key" is default): ')
key_name = "401.07.key" if (key_name == "") else key_name  # if nothing entered, use the default key name

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
    print("\n>>> Encryption Utility v2.0 <<<")
    print("Select the operation to perform:" \
          "\n\t1. Encrypt a file" \
          "\n\t2. Decrypt a file" \
          "\n\t3. Encrypt a message" \
          "\n\t4. Decrypt a message" \
          "\n\t5. Encrypt all files in a folder" \
          "\n\t6. Decrypt all files in a folder" \
          "\n\t0. Exit")

    op = -1  # holds user input
    while not (op >= 0 and op <= 6):
      try:
         op = int(input("Enter a menu option (0-6): "))
      except KeyboardInterrupt:   # Ctrl+C
         print()
         sys.exit()
      except: # catch all for anything other than 1-5 or Ctrl+C
         print("Invalid input. Please try again.")

    if op == 0:
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

      if op == 5:   # encrypt all files in a folder
        dir_name = input('Enter the folder name/path ("401.07" is default): ')
        dir_name = "401.07" if (dir_name == "") else dir_name
        
        if os.path.exists(dir_name):  # if the dir exists
          files = list_dir(dir_name)  # grab all filenames
          for i in sorted(files):     # sort the list and encrypt each file
              encrypt_file(i, key, force="y")  # encrypt, force deletion w/o prompt
              print(f"Encrypted {i}")
        else: print(f"Dir {dir_name} does not exist. Please try again.")

      if op == 6:   # decrypt all files in a folder
        dir_name = input('Enter the folder name/path ("401.07" is default): ')
        dir_name = "401.07" if (dir_name == "") else dir_name

        if os.path.exists(dir_name):  # if the dir exists
          files = list_dir(dir_name)  # grab all filenames
          for i in sorted(files):     # sort the list and encrypt each file
              decrypt_file(i, key, force="y")  # decrypt, force deletion w/o prompt
              print(f"Decrypted {i}")
        else: print(f"Dir {dir_name} does not exist. Please try again.")


print("Script complete!")

# ze end