import os
from typing import Tuple, List, function
from random import seed, randint
from time import time
from . import menu_options as menu
from .caesar_script import SYMBOLS

# Cleaning up the Terminal
# # # NOTE! CURRENTLY WORKS ONLY WITH WINDOWS => ADD OS RECOGNITION
LENGTH_SYMBOLS: int = len(SYMBOLS)


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


def modularInverse(a: int, b: int) -> int | None:
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
            return key_A * LENGTH_SYMBOLS + key_B


def getNewKey() -> int | None:
    """
    Receives an array of keys that can't be used to encrypt message
    
    Asks User for other key: can either type in new valid key or Quit

    :param invalidKeys: key values that can't be used during encryption process
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
        if userInput.upper().startswith('Q'):
            return None
        
        # If User chooses to generate a random key for encrypting
        if userInput.upper().startswith('R'):
            return generateRandomKey()
        
        # Removing spaces in order for isdigit() method to work properly
        userInput = userInput.replace(' ', '')

        # Checking whether ended up with a "number" string and that number is valid key
        if userInput.isdigit():
            key = int(userInput)
            if isValid(key):
                noNewKey = False
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


def multiplicativeEncryption(message: str, key: int):
    """
    Encrypts given string "message" with given "key"

    :param message: Message to be encrypted
    :param key: Key for producing keys for both multiplicational and Caesar encryption
    """
    key_A, key_B = getKeyParts(key)
    
    # If Users decided to Quit Encrypting
    if key_A == None:
        return
    
    # Getting a translation for each known symbol
    TranslationDictionary: dict = {}
    for id in range(LENGTH_SYMBOLS):
        shiftedId = (id * key_A + key_B) % LENGTH_SYMBOLS
        TranslationDictionary[SYMBOLS[id]] =  SYMBOLS[shiftedId]

