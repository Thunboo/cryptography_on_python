from .caesar_cipher import encryptCaesar, decryptCaesar
from .caesar_bruteforce import bruteforce_hack_caesar as BF_Hack 
from pyperclip import copy as add_clipboard
import os


def option_encrypt():
    My_Message = input("Enter a message to be encrypted:\n")
    My_Message = My_Message[:len(My_Message)] # Removing '\n' symbol
    my_key = int(input("Enter a key:\n"))

    # Copying the result to the clipboard
    add_clipboard(encryptCaesar(message=My_Message, key=my_key))

    print("Encrypted message was copied into clipboard!\n")


def option_decrypt():
    My_Message = input("Enter a message to be decrypted:\n")
    My_Message = My_Message[:len(My_Message)] # Removing '\n' symbol
    my_key = int(input("Enter a key:\n"))

    # Copying the result to the clipboard
    add_clipboard(decryptCaesar(message=My_Message, key=my_key))

    print("Decrypted message was copied into clipboard!\n")


def option_bruteforce():
    My_Message = input("Enter a message to be decrypted:\n")
    My_Message = My_Message[:len(My_Message)] # Removing '\n' symbol
    BF_Hack(message=My_Message)


def main():
    option: int = -1
    while (True):
        os.system("cls")
        print("""Welcome to Caesar Cipher Master!
    Pick an option:
    0) Leave...
    1) Encrypt a message
    2) Decrypt a message with known key
    3) Decrypt a message using BruteForce""")

        option = int(input()[:1])
        os.system("cls")
        if option == 0: break
        else:
            if option == 1: option_encrypt()
            elif option == 2: option_decrypt()
            elif option == 3: option_bruteforce()
            os.system("pause")


if __name__ == "__main__":
    main()