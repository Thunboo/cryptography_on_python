from typing import List
import os

ALPHABET_STR: str = "abcdefghijklmnopqrstuvwxyz"
LETTERS_SPACES: str = ALPHABET_STR + ALPHABET_STR.upper() + " \t\n"
LETTERS_SPACES_SET: set = set(LETTERS_SPACES)
# # # ADD function that allows to import Alphabet => All Valid Symbols from .txt

def loadDictionary() -> dict:
    """
    Loads a Dictionary into memory
    :return: Loaded Dictionary
    """
    dictionaryFileRoot: str = "script/dictionary.txt"
    if not os.path.exists(dictionaryFileRoot):
        print(f"{dictionaryFileRoot} \ndoes not exist...")
        return
    
    englishWords: dict = {}
    with open(file=dictionaryFileRoot) as dictionaryFile:
        for word in dictionaryFile.read().split('\n'):
            englishWords[word] = None
    return englishWords


def removeNonValidChars(message: str, validChars: set = LETTERS_SPACES_SET) -> str:
    """
    Removes all Non-Valid (unknown) characters from given string

    :param message: String to be edited
    :param validChars: All symbols which considered to be valid.\nBy DEFAULT only English Alphabet letters (upper and lower case) and spaces ('*space*', '\\t', '\\n') are considered to be "VALID"

    :return: Edited string
    """
    validString: List[str] = ['']
    for symbol in message:
        if symbol in validChars:
            validString.append(symbol)
    return ''.join(validString)


def countEngWordsPercentage(message: str) -> float:
    """
    Count percentage (%) of all known (via Dictionary) English words in given String
    :param message: String being checked
    :return: Percentage (%) : Counted / All_Words
    """
    ENGLISH_WORDS = loadDictionary()
    
    message = message.upper() # Our dictionary of Eng words are all UPPER written
    message = removeNonValidChars(message=message)
    possibleWords: List[str] = message.split()

    if possibleWords == []: # If there is no English Words
        return 0
    
    counter: int = 0
    for word in possibleWords:
        if word in ENGLISH_WORDS:
            counter += 1
    
    return counter / len(possibleWords)


def isEnglish(message: str, wordPercentage: float = 20, lettersPercentage: float = 75) -> bool:
    """
    Checks whether the given message is written in English

    ! NOTE:
    Message is treated as "English" if:

        1) There is at least 20% of English words in Message

        2) At least 85% of Symbols in Message are English alphabet characters

    :param message: String being checked
    :return: True ? False | Message either is English or not
    """
    wordsMatch: bool = countEngWordsPercentage(message=message) * 100 >= wordPercentage # Comparing calculated (%) to the searching (%)
    lettersCounter = len(removeNonValidChars(message=message))    # All valid letters counted
    lettersRatio: float = lettersCounter / len(message)           # Ratio Valid / All letters
    lettersMatch: bool  = lettersRatio * 100 >= lettersPercentage # Comparing calculated (%) to the searching (%)
    # print(f"WM : {countEngWordsPercentage(message=message)}\nLM : {lettersRatio}") # FOR DEBUGGING
    return wordsMatch and lettersMatch

# ^ Check for English words part ###############################

def getWordPattern(word: str) -> str | None:
    """
    Counts occurancies of each english letter in given Word

    Example: 
            Puppy -> 0.1.0.0.2

            Transformator -> 0.1.2.3.4.5.6.1.7.2.0.6.1

            M3ss4g3 -> None (explanation: '3' and '4' are not letters in English Alphabet)
    """
    pattern: str = ""
    added_letter: dict = {}
    cnt: int = 0
    
    if any(symbol not in set(ALPHABET_STR) for symbol in set(word.lower())):
        return None

    for letter in word.lower():
        if letter not in added_letter:
            added_letter[letter] = cnt
            cnt += 1
        pattern += str(added_letter[letter]) + '.'
    
    pattern = pattern[:len(pattern) - 1]
    return pattern


def createPatternsDictionary(createFile: bool = True) -> dict:
    """
    This function creates a Dictionary of patterns of all words from local English Words Dictionary

    For each word is sets corresponding Word Pattern (getWordPattern function) as a Key

    Then each word that matches this pattern will correspond to this pattern as a Value for Key in python dictionary
    
    :return: Dictionary : Key (or pattern) -> [Words]
    """
    if createFile:
        patternsFileRoot: str = "script/patterns_dictionary.txt"
        patternsFile = open(file=patternsFileRoot, mode="w")

    ENGLISH_WORDS = loadDictionary()
    patternsDictionary: dict = {}

    for word in ENGLISH_WORDS:
        wordPattern = getWordPattern(word)
        try:
            patternsDictionary[wordPattern].append(word)
        except KeyError:
            patternsDictionary[wordPattern] = []
            patternsDictionary[wordPattern].append(word)
    
    if createFile:
        for key, value in patternsDictionary.items():
            patternsFile.write(f"{key}|{value}\n")
        patternsFile.close()
    
    return patternsDictionary


def getPatternsDictionary() -> dict:
    """
    Parces a data from already existing Dictionary of Patterns

    If Dictionary does not exist (.txt file) - creates one via createPatternsDictionary() function

    :return: Dictionary of Patterns : Key (pattern) -> [Words]
    """
    dictionaryFileRoot: str = "script/patterns_dictionary.txt"

    if not os.path.exists(dictionaryFileRoot) or (open(file=dictionaryFileRoot).readline() == ""):
        print("There is no Patterns Dictionary")
        print("Creating One...")
        return createPatternsDictionary()        
    else:
        patternsDictionary: dict = {}
        patternsFile = open(file=dictionaryFileRoot)
        for line in patternsFile:
            Key, Value = line[:-1].split("|")
            Value = Value.replace('[', '').replace(']', '').replace(' ','').replace('\'', '')
            Value = list(Value.split(','))
            patternsDictionary[Key] = Value
        patternsFile.close()
        return patternsDictionary

# ^ Check for words patterns part ##############################

def main():
    message: str = "Is th15 4n 3nGl15h sentence 0r it is not?"
    print(f"Message \"{message}\"\nIs English: {isEnglish(message=message, lettersPercentage=70)}")

    puppy: str = "puppy"
    world: str = "world"
    print(f"{puppy} -> {getWordPattern(puppy)}")
    print(f"{world} -> {getWordPattern(world)}")

    PD: dict = getPatternsDictionary()
    print(PD[getWordPattern("this")])
    print(PD[getWordPattern("secret")])
    print(PD[getWordPattern("message")])
    print(PD[getWordPattern("man")])
    try:
        print(PD["0.1"])
    except KeyError:
        print("NONE")



if __name__ == "__main__":
    main()