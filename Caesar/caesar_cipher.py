# CAESAR CIPHER File #
######################

# Defining the Alphabet and the Encryptable Symbols
ALPHABET_STR: str = "ABCDEFGHIJKLMNOPRSTVQWXYZ"
SYMBOLS: str = ALPHABET_STR + ALPHABET_STR.lower() + "1234567890" + " .,?!"
SYMBOLS_SET: set = set(SYMBOLS)


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
    if any(Symbol not in SYMBOLS_SET for Symbol in set(message)):
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
    Decrypted_message: str = ""
    for i in range(len(message)):
        Decrypted_message += Translation_Dictionary[message[i]]

    return Decrypted_message


def main():
    My_Message: str = "This is a 1st secret message from Gleb"
    my_key = 2
    print(My_Message)
    print("- Transforms into: -")
    print(encryptCaesar(message=My_Message, key=my_key))
    print("- Reversed operation: -")
    print(decryptCaesar(message=encryptCaesar(message=My_Message, key=my_key), key=my_key))


if __name__ == "__main__":
    main()
