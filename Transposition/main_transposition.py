from transposition_cipher import encryptTransposition, decryptTransposition
from transposition_bruteforce import bruteforce_hack_transposition as BF_Hack 
from pyperclip import copy as add_clipboard
import os


def option_encrypt():
    My_Message = input("Enter a message to be encrypted:\n")
    My_Message = My_Message[:len(My_Message)] # Removing '\n' symbol
    my_key = int(input("Enter a key:\n"))

    # Copying the result to the clipboard
    add_clipboard(encryptTransposition(message=My_Message, key=my_key))

    print("Encrypted message was copied into clipboard!\n")


def option_decrypt():
    My_Message = input("Enter a message to be decrypted:\n")
    My_Message = My_Message[:len(My_Message)] # Removing '\n' symbol
    my_key = int(input("Enter a key:\n"))

    # Copying the result to the clipboard
    add_clipboard(decryptTransposition(message=My_Message, key=my_key))

    print("Decrypted message was copied into clipboard!\n")


def option_bruteforce():
    My_Message = input("Enter a message to be decrypted:\n")
    My_Message = My_Message[:len(My_Message)] # Removing '\n' symbol
    BF_Hack(message=My_Message)


def main_transposition():
    option: int = -1
    while (True):
        os.system("cls")
        print("""Welcome to Transposition Cipher Master!
    Pick an option:
    1) Encrypt a message
    2) Decrypt a message with known key
    3) Decrypt a message using BruteForce
    4) Leave...""")

        option = int(input()[:1])
        os.system("cls")
        if option == 4: break
        else:
            if option == 1: option_encrypt()
            elif option == 2: option_decrypt()
            elif option == 3: option_bruteforce()
            os.system("pause")


if __name__ == "__main__":
    main_transposition()