from typing import Callable
from pyperclip import copy as add_clipboard
import os, sys
from time import time
from . import detect_english


def main():
    print("This file contains scripts for menu options")
    

def option_encrypt(encrypt_func: Callable, key_type: str = "int"):
    """
    Asks User for a string to be encrypted and a key

    Calls given Encrypting function

    Adds the result to the Clipboard
    """
    my_Message = input("Enter a message to be encrypted:\n")
    my_Message = my_Message[:len(my_Message)] # Removing '\n' symbol

    if key_type == "int":
        my_key = int(input("Enter a Key: (int)\n"))
    else:
        my_key = input("Enter a Key: (str)\n")
    
    # Copying the result to the clipboard if message can be encrypted
    Encrypted_message: str | None = encrypt_func(message=my_Message, key=my_key)
    if Encrypted_message != None:
        add_clipboard(Encrypted_message)
        print("Encrypted message was copied into clipboard!\n")


def option_decrypt(decrypt_func: Callable, key_type: str = "int"):
    """
    Asks User for a string to be decrypted and a key

    Calls given Decrypting function

    Adds the result to the Clipboard
    """
    my_Message = input("Enter a message to be decrypted:\n")
    my_Message = my_Message[:len(my_Message)] # Removing '\n' symbol
    
    if key_type == "int":
        my_key = int(input("Enter a Key: (int)\n"))
    else:
        my_key = input("Enter a Key: (str)\n")
    
    # Copying the result to the clipboard if message can be decrypted
    Decrypted_message: str | None = decrypt_func(message=my_Message, key=my_key)
    if Decrypted_message != None:
        add_clipboard(Decrypted_message)
        print("Decrypted message was copied into clipboard!\n")
    

def option_bruteforce(decrypt_func: Callable, minKeyValue: int = 0, maxKeyValue: int | str = "len(message)"):
    """
    Asks User for a string to be Decrypted

    Calls given BruteForce Decryption function
    
    :param decrypt_func: Function of decryption - uses it's own type of encryption
    :param minKeyValue: Starting Value for loop through all possible keys
    :param maxKeyValue: Ending Value for loop through all possible keys. \n
    NOTE: If (maxKeyValue = "len(message)") is passed - uses length of inputed messaged during work
    """
    my_Message = input("Enter a message to be decrypted:\n")
    my_Message = my_Message[:len(my_Message)] # Removing '\n' symbol

    if maxKeyValue == "len(message)":
        maxKeyValue = len(my_Message)
    
    detection = True
    print("\nDo you wish to DISABLE English text detection?\n")
    print("Yes - 'Y'\nor\nNo - 'N'")
    userInput = input(" > ")[:1]
    if userInput.strip().upper().startswith('Y'):
        detection = False

    if not detection:
        formated = len(str(maxKeyValue))
        print("All possible translations:\n")
        for key in range(minKeyValue, maxKeyValue):
            print(f"Key = {key:{formated}.0f} | {decrypt_func(message=my_Message, key=key)}...")
    else:
        for key in range(minKeyValue, maxKeyValue):
            
            decryptedText = decrypt_func(message=my_Message, key=key)
            
            # Some decryption functions may return None if decryption with given key is impossible
            if decryptedText == None:
                continue

            if detect_english.isEnglish(message=decryptedText, lettersPercentage=85):
                os.system("cls")

                if len(decryptedText) > 100:
                    print(f"\nPossible encrypted text (key = {key}):\n{decryptedText[:100]}...")
                else:
                    print(f"\nPossible encrypted text (key = {key}):\n{decryptedText}")
                print("Do you wish to Continue - 'C' bruteforcing message?\n")
                print("Continue - 'C'\nOr\nQuit - 'Q'\n???")
                response = input(" > ")
                if not response.strip().upper().startswith('C'):
                    add_clipboard(decryptedText)
                    print("\nLast possible decryption was copied into Clipboard\n")
                    break


def option_dictionaryHack(decrypt_func: Callable):
    """
    Asks User for a string to be Decrypted

    Using English words dictionary BruteForce attacks inputted message with given Decryption function
    
    :param decrypt_func: Function of decryption - uses it's own type of encryption
    """
    my_Message = input("Enter a message to be decrypted:\n")
    my_Message = my_Message[:len(my_Message)] # Removing '\n' symbol

    EnglishWords = detect_english.loadDictionary()
    for word in EnglishWords:
        print(word)
        os.system("CLS")
        decryptedText: str = decrypt_func(message=my_Message, key=word)
        if detect_english.isEnglish(message=decryptedText, wordPercentage=40):
            os.system("cls")

            if len(decryptedText) > 100:
                print(f"\nPossible encrypted text (key = {word}):\n{decryptedText[:100]}...")
            else:
                print(f"\nPossible encrypted text (key = {word}):\n{decryptedText}")

            print("Do you wish to Continue - 'C' bruteforcing message?\n")
            print("Continue - 'C'\nOr\nQuit - 'Q'\n???")
            response = input(" > ")
            if not response.strip().upper().startswith('C'):
                add_clipboard(decryptedText)
                print("\nLast possible decryption was copied into Clipboard\n")
                return
    print("Ran out of possible keys...")
    os.system("pause")    


def option_file(encrypt_func: Callable, decrypt_func: Callable, mode: str, key_type: str = "int"):
    """
    Asks User for a .txt file to be Encrypted / Decrypted and a key
    NOTE: File should be in '/messages/' directory

    Calls given Encrypting / Decrypting function
    
    Writes the output to the new (or already existing) file

    :param encrypt_func: Function for Encrypting data
    :param decrypt_func: Function for Decrypting data
    :param mode: Can be either "encrypt" or "decrypt"
    """

    if not os.path.exists("./messages/"):
        if os.getcwd() != 'C:\\WINDOWS\\system32':
            print(f"ERROR !\nNo 'messages' directory was found\nWant to create one?")
            print("Yes - 'Y'\nor\nNo - 'N'")
            userInput = input(" > ")[:1]
            if userInput.strip().upper().startswith('Y'):
                os.mkdir("messages")
                print("Directory 'messages' was created")
                os.system("pause")
            return
        else:
            print("WARNING !!!\n\
                OPENED IN 'C:\\WINDOWS\\system32'\n\
                PLEASE, RUN THIS SCRIPT VIA CMD, OPENED IN CURRENT DIRECTORY.\n")
            os.system("pause")
            sys.exit()

    # Inputting a file name
    filename: str = input(f"Input a Filename with data to be {mode}ed: (*name*.txt)\n > ")
    filename = filename[:len(filename)] + ".txt" # Removing '\n' symbol and adding .txt
    
    if not os.path.exists("./messages/" + filename):
        print(f"ERROR !\n'{filename}' does not exist in '/messages/' directory !")
        os.system("pause")
        return
    
    # Defining an output file name
    output_filename: str = filename[:len(filename) - 4] + "_" + mode + "ed.txt"

    # Checking whether there is already a file with same name
    if os.path.exists("./messages/" + output_filename):
        print(f"This will overwrite \n'{output_filename}'\n")
        print("Continue - 'C'\nOr\nQuit - 'Q'\n???")
        response = input(" > ")
        if not response.strip().upper().startswith('C'):
            return
        
    # Inputting an int key value
    if key_type == "int":
        key: int = int(input(f"Enter a key ({key_type})\n > "))
    elif key_type == "str":
        key: str = input(f"Enter a key ({key_type})\n > ")
    else:
        key: int = -1

    # Opening file, reading it, closing it
    file_obj = open(file="./messages/" + filename, mode='r')
    content = file_obj.read()
    file_obj.close()
    
    # Calculating time of encryption/decryption
    start_time = time()
    if mode == "encrypt":
        translated_content: str = encrypt_func(message=content, key=key)
    elif mode == "decrypt":
        translated_content: str = decrypt_func(message=content, key=key)

    # Printing time of encryption/decryption
    print(f"{mode.capitalize()}ion time: {time() - start_time}")

    # Opening output file, writing translated text into it, closing it
    output_file_obj = open(file="./messages/" + output_filename, mode='w')
    output_file_obj.write(translated_content)
    output_file_obj.close()
    
    print(f"{mode.capitalize()}ed '{filename}' into '{output_filename}'")


def option_file_bruteforce(decrypt_func: Callable,  minKeyValue: int, maxKeyValue: int | str = "len(message)"):
    """
    Asks User for a .txt file to be Decrypted using BruteForce

    Calls given BruteForce Decryption function
    
    Writes the output(s) to the new (or already existing) file(s) in special directory
    
    :param decrypt_func: Function of decryption - uses it's own type of encryption
    :param minKeyValue: Starting Value for loop through all possible keys
    :param maxKeyValue: Ending Value for loop through all possible keys. \n
    NOTE: If (maxKeyValue = "len(message)") is passed - uses length of inputed messaged during work
    """

    if not os.path.exists("./messages/"):
        if os.getcwd() != 'C:\\WINDOWS\\system32':
            print(f"ERROR !\nNo 'messages' directory was found\nWant to create one?")
            print("Yes - 'Y'\nor\nNo - 'N'")
            userInput = input(" > ")[:1]
            if userInput.strip().upper().startswith('Y'):
                os.mkdir("messages")
                print("Directory 'messages' was created")
                os.system("pause")
            return
        else:
            print("WARNING !!!\n\
                OPENED IN 'C:\\WINDOWS\\system32'\n\
                PLEASE, RUN THIS SCRIPT VIA CMD, OPENED IN CURRENT DIRECTORY.\n")
            os.system("pause")
            sys.exit()

    # Inputting a file name
    filename: str = input("Input a Filename with data to be Bruteforced: (*name*.txt)\n > ")
    filename = filename[:len(filename)] + ".txt" # Removing '\n' symbol
    
    if not os.path.exists("./messages/" + filename):
        print(f"ERROR !\n'{filename}' does not exist in '/messages/' directory !")
        os.system("pause")
        return
    
    # Defining an output file name
    output_filename: str = filename[:len(filename) - 4] + "_bruteforced.txt"

    # Checking whether there is already a file with same name
    if os.path.exists("./messages/" + output_filename):
        print(f"This will overwrite \n'{output_filename}'\n")
        print("Continue - 'C'\nOr\nQuit - 'Q'\n???")
        response = input(" > ")
        if not response.strip().upper().startswith('C'):
            return
        
    # Opening file, reading it, closing it
    file_obj = open(file="./messages/" + filename, mode='r')
    content = file_obj.read()
    file_obj.close()
    
    if maxKeyValue == "len(message)":
        maxKeyValue: int = len(content)
    
    # English text detection feature : ON / OFF ?
    detection = True
    print("\nDo you wish to DISABLE English text detection?\n")
    print("Yes - 'Y'\nor\nNo - 'N'")
    userInput = input(" > ")[:1]
    if userInput.strip().upper().startswith('Y'):
        detection = False

    # Begining decrypting
    if not detection:
        # Here we will just print all of the possible outcomes from decrypting (First 50 symbols)
        formated = len(str(maxKeyValue))    # Only for formating output purpose
        print("All possible translations:\n")
        for key in range(minKeyValue, maxKeyValue):
            print(f"Key = {key:{formated}.0f} | {decrypt_func(message=content, key=key)[:50]}...")
    else:
        # Here we will show to the User all found outcomes from decrypting one-by-one
        # But only if they meet the requirement of being English Text - 'isEnglish' function
        
        '''
        # Creating a directory to store files
        newFolder: str = "BruteForce_Decryption_Output"
        curDir: str = os.getcwd()
        path: str = os.path.join(curDir, newFolder)
        if not os.path.exists(path=path):
            os.mkdir(path=path)

        # If os.mkdir failed 
        if not os.path.exists(path):
            raise Exception("FAILED CREATING AN OUTPUT DIRECTORY")
        '''

        # Looping through all possible keys
        for key in range(minKeyValue, maxKeyValue):
            # Get a variant of decrypted text
            decryptedText = decrypt_func(message=content, key=key)
            
            # Some decryption functions may return None if decryption with given key is improper for decrypting
            if decryptedText == None:
                continue
            
            if not detect_english.isEnglish(message=decryptedText):
                continue
            
            # If text meets the requirement of being English Text
            os.system("cls")
            print(f"\nPossible encrypted text (key = {key}):\n{decryptedText[:50]}...\n")

            # Ask whether User wants to Save this output
            print("Do you wish to Save - 'S' bruteforced message?\n")
            print("Save - 'S'\nOr\nNot - 'N'\n???")
            response = input(" > ")

            # If User picks to Save text
            if response.strip().upper().startswith('S'):
                # Checking if file with that name already exists
                if os.path.exists("./messages/" + output_filename):
                    print(f"This will overwrite \n'{output_filename}'\n")
                    print("Save Anyway - 'S'\nOr\nNot - 'N'\n???")
                    response = input(" > ")
                    
                    # If User picks to NOT Overwrite
                    if not response.strip().upper().startswith('S'):
                        continue
                
                output_file_obj = open(file="./messages/" + output_filename, mode='w')
                output_file_obj.write(decryptedText)
                output_file_obj.close()
            
                # Message, that script has successfully Decrypted and Written text into output_file
                print(f"Decrypted '/messages/{filename}' into '/messages/{output_filename}'\n")
            
            print("Do you wish to Continue - 'C' bruteforcing message?\n")
            print("Continue - 'C'\nOr\nQuit - 'Q'\n???")
            response = input(" > ")
            if not response.strip().upper().startswith('C'): # If User choosen NOT to Continue BruteForcing
                break


if __name__ == "__main__":
    main()