from typing import Callable
from pyperclip import copy as add_clipboard
import os
from time import time
from . import detect_english


def option_encrypt(encrypt_func: Callable):
    """
    Asks User for a string to be encrypted and a key
    Calls given Encrypting function
    Adds the result to the Clipboard
    """
    My_Message = input("Enter a message to be encrypted:\n")
    My_Message = My_Message[:len(My_Message)] # Removing '\n' symbol
    my_key = int(input("Enter a key:\n"))

    # Copying the result to the clipboard
    add_clipboard(encrypt_func(message=My_Message, key=my_key))

    print("Encrypted message was copied into clipboard!\n")


def option_decrypt(decrypt_func: Callable):
    """
    Asks User for a string to be decrypted and a key
    Calls given Decrypting function
    Adds the result to the Clipboard
    """
    My_Message = input("Enter a message to be decrypted:\n")
    My_Message = My_Message[:len(My_Message)] # Removing '\n' symbol
    my_key = int(input("Enter a key:\n"))

    # Copying the result to the clipboard
    add_clipboard(decrypt_func(message=My_Message, key=my_key))

    print("Decrypted message was copied into clipboard!\n")


def option_bruteforce(decrypt_func: Callable, minKeyValue: int, maxKeyValue: int | str = "len(message)"):
    """
    Asks User for a string to be Decrypted
    Calls given BruteForce Decryption function
    :param decrypt_func: Function of decryption - uses it's own type of encryption
    :param minKeyValue: Starting Value for loop through all possible keys
    :param maxKeyValue: Ending Value for loop through all possible keys. \n
    NOTE: If (maxKeyValue = "len(message)") is passed - uses length of inputed messaged during work
    """
    My_Message = input("Enter a message to be decrypted:\n")
    My_Message = My_Message[:len(My_Message)] # Removing '\n' symbol

    if maxKeyValue == "len(message)":
        maxKeyValue = len(My_Message)
    
    detection = True
    print("\nDo you wish to disable English text detection?\n")
    print("Yes - 'Y'\nor\nNo - 'N'")
    userInput = input(" > ")[:1]
    if userInput.upper().startswith('Y'):
        detection = False

    if not detection:
        formated = len(str(maxKeyValue))
        print("All possible translations:\n")
        for key in range(minKeyValue, maxKeyValue):
            print(f"Key = {key:{formated}.0f} | {decrypt_func(message=My_Message, key=key)}")
    else:
        for key in range(minKeyValue, maxKeyValue):
            decryptedText = decrypt_func(message=My_Message, key=key)

            if detect_english.isEnglish(message=decryptedText):
                os.system("cls")

                print(f"\nPossible encrypted text (key = {key}):\n{decryptedText[:100]}")
                print("Do you wish to Continue - 'C' bruteforcing message?\n")
                print("Continue - 'C'\nOr\nQuit - 'Q'\n???")
                response = input(" > ")
                if not response.upper().startswith('C'):
                    add_clipboard(decryptedText)
                    print("\nLast possible decryption was copied into Clipboard\n")
                    break
                
                os.system("cls")


def option_file(encrypt_func: Callable, decrypt_func: Callable, mode: str):
    """
    Asks User for a .txt file to be Encrypted / Decrypted and a key
    Calls given Encrypting / Decrypting function
    Writes the output to the new (or already existing) file
    """
    # print(os.getcwd()) # FOR DEBUGGING PURPOSES

    # Inputting a file name
    filename: str = input("Input path to a Filename: (file.txt)\n")
    filename = filename[:len(filename)] # Removing '\n' symbol
    if not os.path.exists(filename):
        print(f"{filename} \ndoes not exist...")
        return
    
    # Defining a output file name
    output_filename: str = filename[:len(filename) - 4] + "." + mode + "ed.txt"

    # Checking whether there is already a file with same name
    if os.path.exists(output_filename):
        print(f"This will overwrite \n'{output_filename}'\n")
        print("Continue - 'C'\nOr\nQuit - 'Q'\n???")
        response = input(" > ")
        if not response.upper().startswith('C'):
            return
        
    # Inputting a key value
    key: int = int(input("Enter a key\n"))

    # Opening file, reading it, closing it
    file_obj = open(file=filename, mode='r')
    content = file_obj.read()
    file_obj.close()
    
    # Calculating time of encryption/decryption
    start_time = time()
    if mode == "encrypt":
        translated_content: str = encrypt_func(message=content, key=key)
    elif mode == "decrypt":
        translated_content: str = decrypt_func(message=content, key=key)

    # Printing time of encryption/decryption
    print(f"{mode.capitalize()}ion time: {start_time - time()}")

    # Opening output file, writing translated text into it, closing it
    output_file_obj = open(file=output_filename, mode='w')
    output_file_obj.write(translated_content)
    output_file_obj.close()
    
    print(f"{mode.capitalize()}ed '{filename}' into '{output_filename}'")


def main():
    print("This file contains scripts for menu options")


if __name__ == "__main__":
    main()