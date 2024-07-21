import os
from typing import List
from . import menu_options as menu


# Defining the Alphabet and the Encryptable Symbols
ALPHABET_STR: str = "abcdefghijklmnopqrstuvwxyz"
SYMBOLS: str = ALPHABET_STR + ALPHABET_STR.upper() + "1234567890" + " .,?!"
SYMBOLS_SET: set = set(SYMBOLS)


def main():
    option: int = -1
    while (True):
        os.system("cls")
        print("""Welcome to Caesar Cipher Master!
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
            if option == 1:   menu.option_encrypt(encrypt_func=encryptCaesar)
            elif option == 2: menu.option_decrypt(decrypt_func=decryptCaesar)
            elif option == 3: menu.option_bruteforce(decrypt_func=decryptCaesar, maxKeyValue=len(SYMBOLS))
            elif option == 4: menu.option_file(encrypt_func=encryptCaesar, decrypt_func=decryptCaesar, mode = "encrypt")
            elif option == 5: menu.option_file(encrypt_func=encryptCaesar, decrypt_func=decryptCaesar, mode = "decrypt")
            elif option == 6: menu.option_file_bruteforce(decrypt_func=decryptCaesar, maxKeyValue=len(SYMBOLS))
            os.system("pause")


# Encrypting Function
def encryptCaesar(message: str = "", key: int = 0) -> None | str:
    """
    Encrypts given string "message" with given "key"

    :param message: message to be encrypted
    :param key: Shifting through alphabet value
    :return: Encrypted string
    """
    # Checking whether there is a non-blank message
    if len(message) == 0:
        raise Exception("No text was provided...")

    # Checking whether all message symbols are valid for Encryption
    """
    We make a set of symbols composing a message
    Then we check in ALL symbols are valid

    If any off those symbols is NOT defined as ENCRYPTABLE -> raising an Exception
    """
    for Symbol in set(message):
        if Symbol not in SYMBOLS_SET:
            print(f"UNKNOWN SYMBOL '{Symbol}'")
            raise Exception("Found a non-valid symbol to be encrypted...")

    # Defining the Symbol-To-Symbol Translation Dictionary
    key = key % len(SYMBOLS) # If key is bigger than the amount of symbols -> take modulus
    NEW_alphabet: str = SYMBOLS[key:] + SYMBOLS[:key]
    Translation_Dictionary: dict = {}

    # Defining the trnsformation of every letter in alphabet
    for symbol_id in range(len(SYMBOLS)):
        # key "Symbol" -> "Shifted Symbol"
        Translation_Dictionary[SYMBOLS[symbol_id]] = NEW_alphabet[symbol_id]

    # Encrypting a message
    Encrypted_message: str = ""
    for i in range(len(message)):
        Encrypted_message += Translation_Dictionary[message[i]]

    return Encrypted_message


# Decrypting Function
def decryptCaesar(message: str = "", key: int = 0) -> None | str:
    """
    Decrypts given string "message" with given "key"

    :param message: message to be decrypted
    :param key: Shifting through alphabet value
    :return: Decrypted string
    """
    # Checking whether there is a non-blank message
    if len(message) == 0:
        raise Exception("No text was provided...")

    # Checking whether all message symbols are valid for Encryption
    """
    We make a set of symbols composing a message
    Then we check in ALL symbols are valid

    If any off those symbols is NOT defined as ENCRYPTABLE -> raising an Exception
    """
    if any(Symbol not in SYMBOLS_SET for Symbol in set(message)):
        raise Exception("Found a non-valid symbol to be encrypted...")

    # Defining the Symbol-To-Symbol Translation Dictionary
    # If key is bigger than the amount of symbols -> take modulus
    key = key % len(SYMBOLS)
    NEW_alphabet: str = SYMBOLS[key:] + SYMBOLS[:key]
    Translation_Dictionary: dict = {}

    # Defining the trnsformation of every letter in alphabet
    for symbol_id in range(len(SYMBOLS)):
        # key "Symbol" -> "Shifted Symbol"
        Translation_Dictionary[NEW_alphabet[symbol_id]] = SYMBOLS[symbol_id]

    # Encrypting a message
    Decrypted_message: List[str] = [""]
    for i in range(len(message)):
        Decrypted_message.append(Translation_Dictionary[message[i]])

    return ''.join(Decrypted_message)


if __name__ == "__main__":
    main()