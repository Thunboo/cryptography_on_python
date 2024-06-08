# TRANSPOSITION CIPHER File #
#############################
from math import ceil
from typing import List


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
    Encrypted_message: str = ""
    for column in range(key):
        for row in range(ceil(length / key)):
            index: int = row * key + column
            if index < length:
                Encrypted_message += message[index]
    
    return Encrypted_message


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


def main():
    message: str = "Common sense is not so common."
    
    print(encryptTransposition(message = message, key = 8))
    print(decryptTransposition(message=encryptTransposition(message=message, key = 8), key = 8))

if __name__ == "__main__":
    main()