from math import ceil
from typing import List
from pyperclip import copy as add_clipboard
import os
from . import menu_options as menu


def main():
    option: int = -1
    while (True):
        os.system("cls")
        print("""Welcome to Transposition Cipher Master!
    Pick an option:
    0) Leave...
    1) Encrypt a message
    2) Decrypt a message with known key
    3) Decrypt a message using BruteForce
    4) Encrypt a file
    5) Decrypt a file with known key
    6) Decrypt a file using BruteForce""")

        option = int(input()[:1])
        os.system("cls")
        if option == 0: break
        else:
            if option == 1:   menu.option_encrypt(encrypt_func=encryptTransposition)
            elif option == 2: menu.option_decrypt(decrypt_func=decryptTransposition)
            elif option == 3: menu.option_bruteforce(decrypt_func=decryptTransposition, minKeyValue=1)
            elif option == 4: menu.option_file(encrypt_func=encryptTransposition, decrypt_func=decryptTransposition, mode = "encrypt")
            elif option == 5: menu.option_file(encrypt_func=encryptTransposition, decrypt_func=decryptTransposition, mode = "decrypt")
            elif option == 6: menu.option_file_bruteforce(decrypt_func=decryptTransposition, minKeyValue=1)
            os.system("pause")


def encryptTransposition(message: str = "", key: int = 0) -> None | str:
    """
    Encrypts given string "message" with given "key"
    :param message: message to be encrypted
    :param key: Shifting value
    :return: Encrypted string
    """
    length: int = len(message)

    # Checking whether there is a non-blank message
    if length == 0:
        raise Exception("No text was provided...")

    # Encrypting message
    Encrypted_message: List[str] = [""]
    for column in range(key):
        for row in range(ceil(length / key)):
            index: int = row * key + column
            if index < length:
                Encrypted_message.append(message[index])
    
    return ''.join(Encrypted_message)


def decryptTransposition(message: str = "", key: int = 0) -> None | str:
    """
    Decrypts given string "message" with given "key"
    :param message: message to be decrypted
    :param key: Shifting value
    :return: Decrypted string
    """
    length: int = len(message)

    # Checking whether there is a non-blank message
    if length == 0:
        raise Exception("No text was provided...")

    # Decrypting message
    cols, rows = ceil(length / key), key 
    blank_cells: int = cols * rows - length
    Decrypted_message: List[str] = [""] * cols
    # We write our encrypted message into the table
    # Then we gather symbols column-by-column collecting the decrypted data
    # Worth mentioning that there is some blank cells which we won't count as a part of our message

    col: int = 0
    row: int = 0
    for symbol in message:
        Decrypted_message[col] += symbol
        col += 1

        if (col == cols) or ((col == cols - 1) and (row >= rows - blank_cells)):
            col = 0
            row += 1
    
    return ''.join(Decrypted_message)


if __name__ == "__main__":
    main()