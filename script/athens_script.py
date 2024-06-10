from pyperclip import copy as add_clipboard
import os
from . import menu_options as menu
from .caesar_script import SYMBOLS, encryptCaesar

def greatestCommonDivisor(a: int, b: int):
    """
    Finds Greatest Common Divisor of 2 numbers using Euclid's algorithm

    :param a: First number
    :param b: Second number
    """
    while a != 0:
        a, b = b % a, a
    return b


def multiplicativeEncryption(message: str, key_A: int, key_B: int):
    """
    Encrypts given string "message" with given "keys"
    :param message: Message to be encrypted
    :param key_A: Key for multiplicational encryption
    :param key_A: Key for Caesar Cipher encryption
    """
    newSymbols: str = ""
    length: int = len(SYMBOLS)

    if key_A == 0:
        print("Key_A cannot be 0")
        return
    if greatestCommonDivisor(key_A, length) != 1:
        print("Key is not coprime with amount of Symbols")
        print(f"{key_A} and {length}\n")
        return
    
    TranslationDictionary: dict = {}
    for id in range(length):
        shiftedId = (id * key_A + key_B) % length
        TranslationDictionary[SYMBOLS[id]] =  SYMBOLS[shiftedId]