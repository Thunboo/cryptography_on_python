import os
from typing import List
from . import menu_options as menu
from .caesar_script import ALPHABET_STR
# from .detect_english import removeNonValidChars

DictOfKeys: dict = {} # Letter -> id (key)
for i in range(len(ALPHABET_STR)):
    DictOfKeys[ALPHABET_STR[i]] = i

ALPHABET_LEN: int = len(ALPHABET_STR)
LETTER_SET: set = set(ALPHABET_STR)
ETAOIN = 'ETAOINSHRDLCUМWFGYPBVKJXQZ'

def encryptVigenere(message: str, key: str) -> str:
    '''
    ...
    '''
    Encrypted_message: List[str] = ['']
    key = key.lower()
    keyLen: int = len(key)

    id: int = 0
    nonLetterCnt: int = 0
    for id in range(len(message)):
        if message[id].lower() in LETTER_SET:
            subKey: str = key[(id - nonLetterCnt) % keyLen]
            shift: int = DictOfKeys[subKey]
            currentLetterId: int = DictOfKeys[message[id].lower()]
            if message[id].islower():
                Encrypted_message.append(ALPHABET_STR[(currentLetterId + shift) % ALPHABET_LEN])
            else:
               Encrypted_message.append(ALPHABET_STR[(currentLetterId + shift) % ALPHABET_LEN].upper())
        else:
            nonLetterCnt += 1
            Encrypted_message.append(message[id])
    
    return ''.join(Encrypted_message)


def decryptVigenere(message: str, key: str) -> str:
    '''
    ...
    '''
    Decrypted_message: List[str] = ['']
    key = key.lower()
    keyLen: int = len(key)

    id: int = 0
    nonLetterCnt: int = 0
    for id in range(len(message)):
        if message[id].lower() in LETTER_SET:
            subKey: str = key[(id - nonLetterCnt) % keyLen]
            shift: int = DictOfKeys[subKey]
            currentLetterId: int = DictOfKeys[message[id].lower()]
            if message[id].islower():
                Decrypted_message.append(ALPHABET_STR[(currentLetterId - shift) % ALPHABET_LEN])
            else:
               Decrypted_message.append(ALPHABET_STR[(currentLetterId - shift) % ALPHABET_LEN].upper())
        else:
            nonLetterCnt += 1
            Decrypted_message.append(message[id])
    
    return ''.join(Decrypted_message)

# Frequency Analisis ##################

def getLetterCount(message: str) -> dict:
    """
    Return a dictionary where for each letter there is a counter of its occurances
    
    :param message: Message being checked
    :return: Letter Counter Dictionary: {'A': int, ... , 'Z': int}
    """
    counterDict: dict = {}
    for letter in ALPHABET_STR:
        counterDict[letter] = 0
    
    for letter in message.lower():
        if letter in ALPHABET_STR:
            counterDict[letter] += 1
    return counterDict


def getFrequencyOrder(message: str) -> str:
    '''
    For a given Message returns a string of all Letters appearing in Message in descending order
    '''
    letterToFreq: dict = getLetterCount(message=message)
    '''
    # CODE FROM BOOK
    freqToLetter: dict = {}
    for letter in ALPHABET_STR:
        if letterToFreq[letter] not in freqToLetter:
            freqToLetter[letterToFreq[letter]] = [letter]
        else:
            freqToLetter[letterToFreq[letter]].append(letter)

    for freq in freqToLetter: # Going through all keys
        freqToLetter[freq].sort(key=ETAOIN.find, reverse=True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])
    
    freqPairs: List[tuple] = list(freqToLetter.items())
    freqPairs.sort(key=[0], reverse=True)
    ...
    '''
    orderList: List[tuple] = list(letterToFreq.items())
    orderList.sort(key=lambda x: (x[1], ETAOIN.find(x[0])), reverse=True)
    return ''.join(item[0] for item in orderList)
    # JOKE :) # return ''.join(item[0] for item in sorted(list(letterToFreq.items()), key=lambda x: (x[1], ETAOIN.find(x[0])), reverse=True))


def getEngFrequencyMatchScore(message: str) -> int:
    '''
    For a given Message count a Match Score of most and least appearing letters 
    
    Score: (0 - 12) <=> (low match - high match)
    '''
    frequencyOrder: str = getFrequencyOrder(message=message)
    matchScore: int = 0
    for letter in ETAOIN[:6]:
        if letter in frequencyOrder[:6]:
            matchScore += 1

    for letter in ETAOIN[-6:]:
        if letter in frequencyOrder[-6:]:
            matchScore += 1
    
    return matchScore

# Dictionary Hack #####################



def main():
    option: int = -1
    while (True):
        os.system("cls")
        print("""Welcome to Vigenere Cipher Master!
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
            if option == 1:   menu.option_encrypt(encrypt_func=encryptVigenere, key_type="str")
            elif option == 2: menu.option_decrypt(decrypt_func=decryptVigenere, key_type="str")
            # elif option == 3: menu.option_bruteforce(decrypt_func=decryptAffine, minKeyValue=0, maxKeyValue=LENGTH_SYMBOLS**2)
            # elif option == 4: menu.option_file(encrypt_func=encryptAffine, decrypt_func=decryptAffine, mode = "encrypt")
            # elif option == 5: menu.option_file(encrypt_func=encryptAffine, decrypt_func=decryptAffine, mode = "decrypt")
            # elif option == 6: menu.option_file_bruteforce(decrypt_func=decryptAffine, minKeyValue=0, maxKeyValue=LENGTH_SYMBOLS**2)
            os.system("pause")


if __name__ == "__main__":
    main()