import os
from itertools import product as iterProduct
from re import compile as RECompile
from typing import List
from pyperclip import copy as add_clipboard
from . import menu_options as menu
from .detect_english import isEnglish


ALPHABET_STR: str = "abcdefghijklmnopqrstuvwxyz".upper()
DictOfKeys: dict = {} # Letter -> id (key)
for i in range(len(ALPHABET_STR)):
    DictOfKeys[ALPHABET_STR[i]] = i

ALPHABET_LEN: int = len(ALPHABET_STR)
LETTER_SET: set = set(ALPHABET_STR)
ETAOIN = 'ETAOINSHRDLCUМWFGYPBVKJXQZ'
 

def main():
    option: int = -1
    while (True):
        os.system("cls")
        print("""Welcome to Vigenere Cipher Master!
    Pick an option:
    0) Leave...
    1) Encrypt a message
    2) Decrypt a message with known key
    3) Decrypt a message using BruteForce (dictionary hack)
    4) Decrypt a message using BruteForce (Kasiski Method) | BROKEN !!!
    -----------------
    5) Encrypt a file
    6) Decrypt a file with known key""")

        option = int(input()[:1])
        os.system("cls")
        if option == 0: break
        else:
            if option == 1:   menu.option_encrypt(encrypt_func=encryptVigenere, key_type="str")
            elif option == 2: menu.option_decrypt(decrypt_func=decryptVigenere, key_type="str")
            elif option == 3: menu.option_dictionaryHack(decrypt_func=decryptVigenere)
            elif option == 4: bruteForceKeyHack(encryptedMessage=getUserMessage())
            elif option == 5: menu.option_file(encrypt_func=encryptVigenere, decrypt_func=decryptVigenere, mode = "encrypt")
            elif option == 6: menu.option_file(encrypt_func=encryptVigenere, decrypt_func=decryptVigenere, mode = "decrypt")
            os.system("pause")


def encryptVigenere(message: str, key: str) -> str:
    '''
    Encrypts given Message with given Key
    
    :param message: Message to be encrypted
    :param key: Encryption key 
    :return: Encrypted Message
    '''
    Encrypted_message: List[str] = ['']
    key = key.upper()
    keyLen: int = len(key)

    id: int = 0
    nonLetterCnt: int = 0
    for id in range(len(message)):
        if message[id].upper() in LETTER_SET:
            subKey: str = key[(id - nonLetterCnt) % keyLen]
            shift: int = DictOfKeys[subKey]
            currentLetterId: int = DictOfKeys[message[id].upper()]
            if message[id].isupper():
                Encrypted_message.append(ALPHABET_STR[(currentLetterId + shift) % ALPHABET_LEN])
            else:
               Encrypted_message.append(ALPHABET_STR[(currentLetterId + shift) % ALPHABET_LEN].lower())
        else:
            nonLetterCnt += 1
            Encrypted_message.append(message[id])
    
    return ''.join(Encrypted_message)


def decryptVigenere(message: str, key: str) -> str:
    '''
    Decrypts given Message with given Key
    
    :param message: Message to be decrypted
    :param key: Decryption key 
    :return: Decrypted Message
    '''
    Decrypted_message: List[str] = ['']
    key = key.upper()
    keyLen: int = len(key)

    id: int = 0
    nonLetterCnt: int = 0
    for id in range(len(message)):
        if message[id].upper() in LETTER_SET:
            subKey: str = key[(id - nonLetterCnt) % keyLen]
            shift: int = DictOfKeys[subKey]
            currentLetterId: int = DictOfKeys[message[id].upper()]
            if message[id].isupper():
                Decrypted_message.append(ALPHABET_STR[(currentLetterId - shift) % ALPHABET_LEN])
            else:
               Decrypted_message.append(ALPHABET_STR[(currentLetterId - shift) % ALPHABET_LEN].lower())
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
    
    for letter in message.upper():
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

# BruteForce Hack Script (via keys) #

MAX_KEY_LEN:   int = 16
SUBKEY_MAXLEN: int = 4
NONLETTERS_PATTERN = RECompile('[^A-Z]')

def findRepeatedSequences(message: str) -> dict:
    '''
    Finds any 3-4-5-letters repeated sequences

    :return: Dictionary: Sequence -> List of Repetition Interval  
    '''
    # Removing NON-Letters Symbols
    message = NONLETTERS_PATTERN.sub('', message.upper())

    # Sequence -> Interval of Repetition
    seqSpacings: dict = {} 

    msgLen: int = len(message)
    for seqLen in range(3, 6):
        for seqStart in range(msgLen - seqLen):
            sequence: str = message[seqStart : seqStart + seqLen]

            for i in range(seqStart + seqLen, msgLen - seqLen):
                if message[i : i + seqLen] == sequence:
                    if sequence not in seqSpacings:
                        seqSpacings[sequence] = []
                    seqSpacings[sequence].append(i - seqStart) # ! WAS A MISTAKE
    return seqSpacings

def getUsefulFactors(num: int) -> List[int | None]:
    if num < 2: return []

    factors: List[int] = []
    for i in range(2, MAX_KEY_LEN + 1):
        if num % i == 0:
            factors.append(i)
            otherFactor: int = num // i
            if MAX_KEY_LEN >= otherFactor and otherFactor > 1: 
                factors.append(otherFactor)
    return list(set(factors))

def getCommonFactors(seqFactors: dict) -> List:
    '''
    For given seqFactors dictionary: \nLetter Sequence -> List of Repetition Factors \n\n
    Makes a dictionary: \nFactor -> Repetition Counter
    
    :return: List with Tuple: [ (Factor, How many times that Factor was seen), ...]
    '''
    factorsCNT: dict = {}

    for sequence in seqFactors:
        factors = seqFactors[sequence]
        for factor in factors:
            if factor not in factorsCNT:
                factorsCNT[factor] = 0
            factorsCNT[factor] += 1
    
    # Dict -> Tuple (Factor, Counter)
    factorsByCount = []
    for factor in factorsCNT:
        if factor <= MAX_KEY_LEN:
            factorsByCount.append( (factor, factorsCNT[factor]) )
    
    factorsByCount.sort(key=lambda x: x[1], reverse=True)

    return factorsByCount

def kasiskiExamination(encryptedMessage: str) -> List[str]:
    '''
    Finds all Likely to be Keys for given Encrypted Message and returns it as List
    '''
    repeatedSequences: dict = findRepeatedSequences(encryptedMessage)

    # seqFactors is a dictionary: \nLetter Sequence -> List of Repetition Factors
    seqFactors: dict = {}
    for sequence in repeatedSequences:
        seqFactors[sequence] = []
        for spacing in repeatedSequences[sequence]:
            seqFactors[sequence].extend(getUsefulFactors(spacing))

    factorsByCount = getCommonFactors(seqFactors)

    possibleKeyLengths = []
    for item in factorsByCount:
        possibleKeyLengths.append(item[0])
    
    return possibleKeyLengths

def getNthLetterSubstring(message: str, nth: int, keyLen: int) -> str:
    '''
    For given message splits it into parts of length 'keyLen'\n
    Takes every n-th letter in those parts\n

    :return: Substring of n-th letters
    '''
    i = nth - 1
    substring: List[str] = []
    while i < len(message):
        substring.append(message[i])
        i += keyLen
    return ''.join(substring)


def attemptHackKeyLen(encryptedMessage: str, possibleKeyLength: int) -> str | None:
    '''
    This function attempts to Hack given Encrypted message with given Possible Key Length

    :param encryptedMessage: Message to be decrypted while hacking
    :param possibleKeyLength: Length of possible Encryption Key
    :return: Either Decrypted Message or None (cannot be encrypted with given key)
    '''
    encryptedMessageUP = encryptedMessage.upper()
    messageLen: int = len(encryptedMessage)
    
    allFreqScores: List[int] = []
    for nth in range(1, possibleKeyLength + 1):
        nthSubstring = getNthLetterSubstring(encryptedMessage, nth, possibleKeyLength)
        
        # List like: [ (letter, frequency match score), ...]
        freqScores = []
        for letter in ALPHABET_STR:
            decryptedMessage: str = decryptVigenere(message=nthSubstring, key=letter)
            key_freq = (letter, getEngFrequencyMatchScore(message=decryptedMessage))
            freqScores.append(key_freq)
        # Sorting based on Frequency Analysis Score  # ! WAS A MISTAKE
        freqScores.sort(key=lambda x: x[1], reverse=True)

        allFreqScores.append(freqScores[:SUBKEY_MAXLEN])
    
    ########################################################

    # print(allFreqScores)
    # print(f"Possible Key Length : {possibleKeyLength}")
    for id in iterProduct(range(SUBKEY_MAXLEN), repeat=possibleKeyLength):
        possibleKey: str = ''
        for i in range(possibleKeyLength):
            possibleKey += allFreqScores[i][id[i]][0]
        
        # print(f"ID: {id} | Possible key : {possibleKey}\n")

        decryptedMessage: str = decryptVigenere(encryptedMessageUP, possibleKey)

        if isEnglish(decryptedMessage):
            # Returning upper-lower case as it was orginally
            origCase: List[str]
            for i in range(messageLen):
                if encryptedMessage[i].isupper():
                    origCase.append(decryptedMessage[i].upper())
                else:
                    origCase.append(decryptedMessage[i].lower())
            decryptedMessage = ''.join(origCase)

            ##############

            print(f"Possible Decrypted Message (with key: \"{possibleKey}\"):")
            print(decryptedMessage[:150], '\n')

            print("Do you wish to Continue - 'C' bruteforcing message?\n")
            print("Continue - 'C'\nOr\nQuit - 'Q'\n???")
            response = input(" > ")
            if not response.strip().upper().startswith('C'):
                add_clipboard(decryptedMessage)
                print("\nLast possible decryption was copied into Clipboard\n")
                return decryptedMessage
    
    ########################################################

    return None

def bruteForceKeyHack(encryptedMessage: str) -> str | None:
    '''
    This function uses Frequency Analisys and some other cool algorithms 
    to make BruteForce attack viable/usable

    :param encryptedMessage: Message to be decrypted while hacking
    :return: Either Decrypted Message or None (cannot be encrypted with given key)
    '''
    allPossibleKeyLens = kasiskiExamination(encryptedMessage)
    hackedMessage: str | None = None

    for keyLen in allPossibleKeyLens:
        if keyLen > 6: continue
        hackedMessage = attemptHackKeyLen(encryptedMessage, keyLen)
        if hackedMessage != None:
            return hackedMessage
    
    print(f"Kasiski Method Failed to success...")
    print("Do you wish to Continue - 'C' bruteforcing message?\n")
    print("Continue - 'C'\nOr\nQuit - 'Q'\n???")
    response = input(" > ")
    if not response.strip().upper().startswith('C'):
        return None
    
    os.system("cls")
    
    for keyLen in range(1, MAX_KEY_LEN + 1):
        if keyLen not in allPossibleKeyLens:
            hackedMessage = attemptHackKeyLen(encryptedMessage, keyLen)
            if hackedMessage != None:
                return hackedMessage
    
    return None


def getUserMessage() -> str:
    message: str = input("Enter a message to be decrypted using bruteforce:\n")
    return message[:len(message)]

   
if __name__ == "__main__":
    main()