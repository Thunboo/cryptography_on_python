from typing import List

ALPHABET_STR: str = "abcdefghijklmnopqrstuvwxyz"
LETTERS_SPACES: str = ALPHABET_STR + ALPHABET_STR.upper() + " \t\n"
LETTERS_SPACES_SET: set = set(LETTERS_SPACES)
# # # ADD function that allows to import Alphabet => All Valid Symbols from .txt

def loadDictioanary() -> dict:
    """
    Loads a Dictionary into memory
    :return: Loaded Dictionary
    """
    englishWords: dict = {}
    with open(file="script/dictionary.txt") as dictionaryFile:
        for word in dictionaryFile.read().split('\n'):
            englishWords[word] = None
    return englishWords


def removeNonValidChars(message: str) -> str:
    """
    Removes all Non-Valid (unknown) characters from given string
    :param message: String to be edited
    :return: Edited string
    """
    validString: List[str] = ['']
    for symbol in message:
        if symbol in LETTERS_SPACES_SET:
            validString.append(symbol)
    return ''.join(validString)


def countEngWordsPercentage(message: str) -> float:
    """
    Count percentage (%) of all known (via Dictionary) English words in given String
    :param message: String being checked
    :return: Percentage (%) : Counted / All_Words
    """
    ENGLISH_WORDS = loadDictioanary()
    
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


def isEnglish(message: str, wordPercentage: float = 20, lettersPercentage: float = 85) -> bool:
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
    return wordsMatch and lettersMatch


def main():
    message: str = "Is th15 4n 3nGl15h sentence 0r it is not?"
    print(f"Message \"{message}\"\nIs English: {isEnglish(message=message, lettersPercentage=70)}")


if __name__ == "__main__":
    main()