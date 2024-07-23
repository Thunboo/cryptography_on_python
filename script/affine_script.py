import os
from typing import Tuple, List
from random import seed, randint
from time import time
from . import menu_options as menu
from .caesar_script import SYMBOLS

LENGTH_SYMBOLS: int = len(SYMBOLS)

def main():
    option: int = -1
    while (True):
        os.system("cls")
        print("""Welcome to Affine Cipher Master!
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
            if option == 1:   menu.option_encrypt(encrypt_func=encryptAffine)
            elif option == 2: menu.option_decrypt(decrypt_func=decryptAffine)
            elif option == 3: menu.option_bruteforce(decrypt_func=decryptAffine, minKeyValue=0, maxKeyValue=LENGTH_SYMBOLS**2)
            elif option == 4: menu.option_file(encrypt_func=encryptAffine, decrypt_func=decryptAffine, mode = "encrypt")
            elif option == 5: menu.option_file(encrypt_func=encryptAffine, decrypt_func=decryptAffine, mode = "decrypt")
            elif option == 6: menu.option_file_bruteforce(decrypt_func=decryptAffine, minKeyValue=0, maxKeyValue=LENGTH_SYMBOLS**2)
            os.system("pause")


def findModInverse(a: int, b: int) -> int | None:
    """
    For given modular expression: (a * i) % b = 1
    
    Finds i value using Euclid's algorithm
    """
    # There can't be a modular inverse for coprime A and B values
    if greatestCommonDivisor(a, b) != 1:
        return None
    
    # Euclid's MAGIC ✨
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, b
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % b


def greatestCommonDivisor(a: int, b: int) -> int:
    """
    Finds Greatest Common Divisor of 2 numbers using Euclid's algorithm

    :param a: First number
    :param b: Second number
    :return: Greatest Common Divisor for A and B
    """
    while a != 0:
        a, b = b % a, a
    return b


def isValid(key: int) -> bool:
    """
    Checks whether key is Valid for Enrypting or it is NOT

    :param key: Key being checked
    :return: Valid / Not Valid
    """
    # In 1st case - If key in [0, 2 * LEN] => Multiplicational Encryption won't work
    condition1: function = lambda key: key > 2 * LENGTH_SYMBOLS
    # In 2nd case - If Produced key_A results in not coprime number with LENGTH_SYMBOLS => Multiplicational Encryption won't work
    condition2: function = lambda key: greatestCommonDivisor(key // LENGTH_SYMBOLS, LENGTH_SYMBOLS) == 1
    # In 3rd case - If key mod LEN == 0 => Caesar Encryption does nothing
    condition3: function = lambda key: key % LENGTH_SYMBOLS != 0

    conditions: List[function] = [condition1, condition2, condition3]
    if any(cond(key) == False for cond in conditions):
        return False
    return True


def generateRandomKey() -> int:
    """
    Generates a random valid key for Encryption

    :return: Valid Key
    """
    seed(time()) # Base seed for random generation based on current time
    while (True):
        key_A: int = randint(2, LENGTH_SYMBOLS) # First condition will always be True
        key_B: int = randint(1, LENGTH_SYMBOLS) # Third condition will always be True
        if greatestCommonDivisor(key_A, LENGTH_SYMBOLS) == 1: # Second condition check
            key: int = key_A * LENGTH_SYMBOLS + key_B
            print(f"Generated key: {key}")
            return key


def getNewKey() -> int | None:
    """
    Asks User for new key: can either Type in new valid key or Quit

    :return: A new key or None (no new key, quitting encryption process)
    """
    noNewKey: bool = True
    while (noNewKey):
        os.system("cls")

        print("These are RULES for valid key for Athens Encryption:")
        print(f"    1) key > {2 * LENGTH_SYMBOLS}")
        print(f"    2) key % (mod) {LENGTH_SYMBOLS} != 0\n")
        print(f"    3) key // {LENGTH_SYMBOLS} is NOT coprime to {LENGTH_SYMBOLS}\n")
        print("Enter a new key (int) or Use Random key - 'R'\nor\nQuit - 'Q'")
        userInput: str = input(" > ")

        # If User chooses to quit this type of encrypting
        if userInput.strip().upper().startswith('Q'):
            return None
        
        # If User chooses to generate a random key for encrypting
        if userInput.strip().upper().startswith('R'):
            return generateRandomKey()
        
        # Removing spaces in order for isdigit() method to work properly
        userInput = userInput.replace(' ', '')

        # Checking whether ended up with a "number" string and that number is valid key
        if userInput.isdigit():
            key = int(userInput)
            if isValid(key):
                return key


def getKeyParts(key: int) -> Tuple[int, int] | Tuple[None, None]:
    """
    Receives a single key and transforms it into 2 keys

    :return: Tuple with 2 new keys or No keys if Users wants to Quit Encrypting
    """
    
    if not isValid(key):
        key: int | None = getNewKey()
        if key == None:
            return (None, None)

    key_A = key // LENGTH_SYMBOLS
    key_B = key % LENGTH_SYMBOLS
    return (key_A, key_B)


def encryptAffine(message: str, key: int) -> str | None:
    """
    Encrypts given string "message" with given "key"

    :param message: Message to be encrypted
    :param key: Key for producing keys for both multiplicational and Caesar encryption
    """
    key_A, key_B = getKeyParts(key)
    
    # If Users decided to Quit Encrypting
    if key_A == None:
        print("Quitting...")
        return None
    
    # Getting a translation for each known symbol
    Translation_Dictionary: dict = {}
    for id in range(LENGTH_SYMBOLS):
        shiftedId = (id * key_A + key_B) % LENGTH_SYMBOLS
        Translation_Dictionary[SYMBOLS[id]] = SYMBOLS[shiftedId]


    # Encrypting a message
    Encrypted_message: List[str] = ['']
    for symbol in message:
        if symbol in Translation_Dictionary:
            Encrypted_message.append(Translation_Dictionary[symbol])
        else:
            Encrypted_message.append(symbol)
    
    return ''.join(Encrypted_message)


def decryptAffine(message: str, key: int) -> str | None:
    
    """
    Decrypts given string "message" with given "key"

    :param message: Message to be decrypted
    :param key: Key for producing keys for both Multiplicational and Caesar encryption
    """
    # If that key could not be used to encrypt data => you can't decrypt data with it
    if not isValid(key):
        return None
    
    key_A, key_B = getKeyParts(key)
    
    # Getting a translation for each known symbol
    Translation_Dictionary: dict = {}
    # # Euclid Magic ✨ Style
    # modInv_A: int = modularInverse(key_A, LENGTH_SYMBOLS)
    # for id in range(LENGTH_SYMBOLS):
    #     shiftedId = (id - key_B) * modInv_A % LENGTH_SYMBOLS
    #     Translation_Dictionary[SYMBOLS[id]] =  SYMBOLS[shiftedId]
    
    # No Euclid's Magic
    for id in range(LENGTH_SYMBOLS):
        shiftedId = (id * key_A + key_B) % LENGTH_SYMBOLS
        Translation_Dictionary[SYMBOLS[shiftedId]] = SYMBOLS[id]

    # Decrypting a message
    Decrypted_message: List[str] = ['']
    for symbol in message:
        if symbol in Translation_Dictionary:
            Decrypted_message.append(Translation_Dictionary[symbol])
        else:
            Decrypted_message.append(symbol)
    
    return ''.join(Decrypted_message)


if __name__ == "__main__":
    main()