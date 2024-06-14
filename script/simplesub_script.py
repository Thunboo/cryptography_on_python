import os
from copy import deepcopy
from random import seed, shuffle
from typing import Any
from time import time
from pyperclip import copy as add_clipboard
from . import menu_options as menu
from .caesar_script import ALPHABET_STR
from .detect_english import getPatternsDictionary, getWordPattern, removeNonValidChars, loadDictionary

ALPHABET: list[str] = list(ALPHABET_STR.upper())
ALPHABET_SET: set = set(ALPHABET_STR.upper())


def generateRandomKey() -> str:
    """
    Generates a Random Key for Simple Subtitute Cipher

    :return: Randomly generated Key
    """
    os.system("cls")
    seed(time())
    alphabet_copy: list[str] = deepcopy(ALPHABET)
    shuffle(alphabet_copy)
    key: str = ''.join(alphabet_copy)
    print(f"Your Key is : \"{key}\"")
    return key


def isValid(key: Any) -> bool:
    """
    Checks whether Key can be used to translate message

    :param key: Key ro be checked
    :return: True / False
    """
    if type(key) != str:
        return False
    
    # If not all letters are encrypted via key
    if set(key.upper()) != ALPHABET_SET:
        # print(f"KEY SETS DOES NOT MATCH:\n{set(key.upper())}\n{ALPHABET_SET}") # FOR DEBUGGING PURPOSES
        # print("Invalid Key Input : Length does not match the requirement\n")
        return False
    return True


def getNewKey() -> int | None:
    """
    Asks User for new key: can either Type in new valid key or Quit

    :return: A new key or None (no new key, quitting encryption process)
    """
    noNewKey: bool = True
    while (noNewKey):
        os.system("cls")

        print("This is single RULE for valid key for Simple Substitution Encryption:")
        print(f"    1) Key contains all letters from \"{ALPHABET_STR}\"\n")
        print("Enter a new key (str) or Use Random key - type in 'Random'\nor\nQuit - Just hit 'Enter'")
        userInput: str = input(" > ")

        # If User chooses to quit this type of encrypting
        if userInput == '':
            return None
        
        # If User chooses to generate a random key for encrypting
        if userInput.strip().upper() == "RANDOM":
            return generateRandomKey()
        
        userInput = userInput.replace(' ', '')
        if isValid(userInput):
            return userInput


def translateMessage(message: str, key: Any, mode: str) -> str | None:
    """
    Translates the given message considering both the key and mode

    :param message: Message to be tranlated
    :param key: Translation key 
    :param mode: "encrypt" or "decrypt"
    :return: Either Translated Message or None (cannot be translated with given key)
    """
    if mode not in ["encrypt", "decrypt"]:
        return None
    
    if not isValid(key):
        key = getNewKey()
    
    # If Users decided to Quit Encrypting
    if key == None:
        print("Quitting...")
        return None
    
    key = key.upper()
    Encrypt_Dictionary: dict = {}
    for id in range(len(ALPHABET)):
        Encrypt_Dictionary[ALPHABET[id]] = key[id]
    
    output_message: list[str] = ['']
    if mode == "encrypt":
        for symbol in message:
            if symbol.upper() in Encrypt_Dictionary:
                if symbol.isupper():
                    output_message.append(Encrypt_Dictionary[symbol])
                else:
                    output_message.append(Encrypt_Dictionary[symbol.upper()].lower())
            else:
                output_message.append(symbol)

    # If We are Decrypting a message - We need "swapped" Dictionary
    if mode == "decrypt":
        Decrypt_Dictionary: dict = {Value: Key for Key, Value in Encrypt_Dictionary.items()}
        for symbol in message:
            if symbol.upper() in Decrypt_Dictionary:
                if symbol.isupper():
                    output_message.append(Decrypt_Dictionary[symbol])
                else:
                    output_message.append(Decrypt_Dictionary[symbol.upper()].lower())
            else:
                output_message.append(symbol)

    return ''.join(output_message)


def encryptSub(message: str, key: Any) -> str | None:
    """
    Encrypts given Message with given Key (if possible)
    
    :param message: Message to be encrypted
    :param key: Encryption key 
    :return: Either Encrypted Message or None (cannot be encrypted with given key)
    """
    return translateMessage(message=message, key=key, mode="encrypt")


def decryptSub(message: str, key: Any) -> str | None:
    """
    Decrypts given Message with given Key (if possible)
    
    :param message: Message to be decrypted
    :param key: Decryption key 
    :return: Either Decrypted Message or None (cannot be decrypted with given key)
    """
    return translateMessage(message=message, key=key, mode="decrypt")
    
#####################################################

def blankLetterMapping() -> dict:
    """
    Return a BLANK dictionary where for each letter an empty array being set
    
    :return: Blank Letter Mapping Dictionary: {'A': [ ], ... , 'Z': [ ]}
    """
    blankDict: dict = {}
    for letter in ALPHABET:
        blankDict[letter] = []
    return blankDict


def fillLetterMapping(word: str, candidate: str) -> dict:
    """
    For given word and it is possible decryption returns a possible decryption for each letter
    """
    letterMapping: dict = blankLetterMapping()
    for id in range(len(word)):
        # If possible decryption for letter is not represented as a variant -> add it
        if candidate[id] not in letterMapping[word[id]]:
            letterMapping[word[id]].append(candidate[id])
    
    return letterMapping


def intersectLetterMapping(map_A: dict, map_B: dict) -> dict:
    """
    For two given Letters Mappings intersects them leaving only those letters which are represented in both Mappings
    """
    intersection: dict = blankLetterMapping()

    for letter in ALPHABET:
        if map_A[letter] == []:    # If A = [] => any letter => copy B
            intersection[letter] == deepcopy(map_B[letter])
        elif map_B[letter] == []:  # If B = [] => any letter => copy A
            intersection[letter] == deepcopy(map_A[letter])
        else:
            for mappedLetter in map_A[letter]:
                if mappedLetter in map_B[letter]:
                    intersection[letter].append(mappedLetter)
    
    return intersection


def removeSolvedLetter(letterMapping: dict):
    """
    Removes all letters decryption variant from given Letter Mapping 
    if can determine a single one decryption for single letter
    """
    looping: bool = True
    while (looping):
        looping = False
        solvedLetters: list[str] = []

        for letter in ALPHABET:
            # If letter is determined to be decrypted with single variant
            if len(letterMapping[letter]) == 1:
                # Appending its ONLY POSSIBLE decryption
                solvedLetters.append(letterMapping[letter][0])
        
        for letter in ALPHABET:
            for sl in solvedLetters:
                variants: int = len(letterMapping[letter])
                if (variants != 1) and (sl in letterMapping[letter]):
                    letterMapping[letter].remove(sl)
                    if variants - 1 == 1:
                        looping = True


def getMessage() -> str | None:
    message = input("Enter a message to be decrypted:\n")
    if len(message) == 0:
        return None
    message = message[:len(message)] # Removing '\n' symbol
    return message
    

def bruteforceHack(message: str | None = None):
    """
    Bruteforces an inputted or given message and decrypts it if possible

    If ended up with decrypted message -> Adds it to a clipboard
    """
    if message == None:
        message: str | None = getMessage()
    if message == None:
        return
    
    patterns_dictionary: dict = getPatternsDictionary()
    letterMapping: dict = blankLetterMapping()

    message = removeNonValidChars(message)
    words: list[str] = message.upper().split()
    ENGLISH_WORDS: dict = loadDictionary()

    for word in words:
        """ 
        We might have ended up with something like this:
            The word was: m3SS4g3 (stands for message)
            But after convertion it becomes: MSSG -> "0.1.1.2" pattern
            WHICH IS WRONG!

            NOTE! Correct pattern for m3SS4g3 -> "0.1.2.2.3.4.1"
            So if we have transformed word like "m3SS4g3" into "MSSG":
            We check whether this thing even an Enclish Word
        """
        if word not in ENGLISH_WORDS:
            continue
        pattern: str = getWordPattern(word)
        candidates: list[str] = patterns_dictionary[pattern]
        for candidate in candidates:
            newMapping: dict = fillLetterMapping(word, candidate)
            letterMapping = intersectLetterMapping(letterMapping, newMapping)
    
    removeSolvedLetter(letterMapping)
    
    encryptionKey: list[str] = [""]
    for _, value in letterMapping.items():
        encryptionKey.append(value)
    key: str = ''.join(encryptionKey)
    
    add_clipboard(decryptSub(message, key))
    print("Decrypted message was copied into clipboard!\n")
    return


def main():
    option: int = -1
    while (True):
        os.system("cls")
        print("""Welcome to Simple Substitution Cipher Master!
    Pick an option:
    0) Leave...
    1) Encrypt a message
    2) Decrypt a message with known key
    3) Decrypt a message using BruteForce
    4) Encrypt a file
    5) Decrypt a file with known key""")

        option = int(input()[:1])
        os.system("cls")
        if option == 0: break
        else:
            if option == 1:   menu.option_encrypt(encrypt_func=encryptSub, key_type="str")
            elif option == 2: menu.option_decrypt(decrypt_func=decryptSub, key_type="str")
            elif option == 3: bruteforceHack()
            elif option == 4: menu.option_file(encrypt_func=encryptSub, decrypt_func=decryptSub, mode = "encrypt", key_type="str")
            elif option == 5: menu.option_file(encrypt_func=encryptSub, decrypt_func=decryptSub, mode = "decrypt", key_type="str")
            os.system("pause")


if __name__ == "__main__":
    main()