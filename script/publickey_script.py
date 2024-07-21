import os, sys, math
from typing import List
from pyperclip import copy as add_clipboard
from .genPublicPrivateKeys import SEPARATOR


# Defining the Alphabet and the Encryptable Symbols
ALPHABET_STR: str = "abcdefghijklmnopqrstuvwxyz"
SYMBOLS: str = ALPHABET_STR.upper() + ALPHABET_STR + "1234567890" + " !?."
SYMBOLS_LEN: int = len(SYMBOLS)
SYMBOLS_DICT: dict = {}
for i in range(SYMBOLS_LEN):
    SYMBOLS_DICT[SYMBOLS[i]] = i


def main():
    option: int = -1
    while (True):
        os.system("cls")
        print("""Welcome to Public Key Cipher Master!
    Pick an option:
    0) Leave...
    1) Encrypt a message
    2) Decrypt a message with known key
    -----------------
    3) Encrypt a file
    4) Decrypt a file with known key""")

        option = int(input()[:1])
        os.system("cls")
        if option == 0: break
        else:
            if option == 1:   encryptMessage(message=getUserMessage('Message'), 
                                             key=getKeys(operation='Encrypt'), 
                                             blockSize=getBlockSize())
            elif option == 2: decryptMessage(message=getEncryptedBlocks(), 
                                             messageLength=getUserMessage('Message Length'), 
                                             key=getKeys(operation='Decrypt'), 
                                             blockSize=getBlockSize())
            elif option == 3: encryptFile(messageFilename=getFilename("Message"), 
                                          keyFilename=getFilename("Keys"), 
                                          blockSize=getBlockSize())
            elif option == 4: decryptFile(messageFilename=getFilename("Message"), 
                                          keyFilename=getFilename("Keys"))
            print("DONE !")
            os.system("pause")


def getBlocksFromText(message: str, blockSize: int) -> List[int]:
    '''
    Divides given message into Blocks with given blockSize

    Each block represents given STRING text in INTEGER type data

    All block then represented as an ARRAY of INTs
    '''
    for symbol in message:
        if symbol not in SYMBOLS_DICT:
            print(f"ERROR !!!\n\
            There is no '{symbol}' in symbols set\n\
            Exiting the program...\n")

            sys.exit()
    
    blockInts: List[int] = []
    msgLen: int = len(message)
    for blockStart in range(0, msgLen, blockSize):
        blockInt: int = 0
        for i in range(blockStart, min(blockStart + blockSize, msgLen)):
            blockInt += SYMBOLS_DICT[message[i]] * (SYMBOLS_LEN ** (i % blockSize))
        blockInts.append(blockInt)
    
    return blockInts


def getTextFromBlocks(blockInts: List[int], messageLength: int, blockSize: int) -> str:
    '''
    With given ARRAY of INTs representing Blocks of initial message 
    
    Each block is limited with given blockSize

    Each block represents initial STRING text in INTEGER type data

    Using given initial message length translates Blocks back to readable STRING text
    '''
    message: List[str] = []
    
    for blockInt in blockInts:
        blockMessage: List[str] = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                charIndex = blockInt // (SYMBOLS_LEN ** i)
                blockInt %= (SYMBOLS_LEN ** i)
                blockMessage.insert(0, SYMBOLS[charIndex])
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message: str, key: tuple[int, int], blockSize: int | None) -> List[int]:
    '''
    Encrypts Message with Public Key and given blockSize

    NOTE: If not given, encrypts data with 256 BlockSize
    '''
    if blockSize == None: blockSize = 256

    encryptedBlocks: List[int] = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        # Ciphertext = Message ^ e mod n
        encryptedBlocks.append( pow(block, e, n) )
    
    return encryptedBlocks


def decryptMessage(encryptedBlocks: List[int], messageLength: int, key: tuple[int, int], blockSize: int | None) -> str:
    '''
    Decrypts Encrypted Message represented as ARRAY of Encypted INTs 
    Using Private Key, Length of Initial Message and blockSize

    NOTE: If not given, encrypts data with 256 BlockSize
    '''
    if blockSize == None: blockSize = 256
    
    decryptedBlocks: List[int] = []
    n, d = key

    for block in encryptedBlocks:
        # Message = Ciphertext ^ d mod n
        decryptedBlocks.append( pow(block, d, n) )
    
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFromFile(keyFilename: str) -> tuple[int, int, int]:
    '''
    File should be formated as if it was created using genPublicPrivateKeys.py script !
    
    :return: Tuple with either Public or Private keys
    ''' 
    file_obj = open("./keys/" + keyFilename)
    content: List[str] = file_obj.read().replace('\n', '').split(SEPARATOR)
    keySize: int = int(content[0].split(' ')[-1])
    keyType: str = content[1].split(' ')[0]
    n: int = int(content[2])

    if keyType == "Public":
        e: int = int(content[3])
        return (keySize, n, e)
    elif keyType == "Private":
        d: int = int(content[3])
        return (keySize, n, d)
    

def encryptFile(messageFilename: str, keyFilename: str, blockSize: int | None = None):
    '''
    Encrypts text from given messageFile using keys from keyFile\n
    Then Encrypted "text" (bunch of numbers) being written into "new" file

    NOTE 1: messageFile should be in '/messages/' directory
    NOTE 2: keyFile should be in '/keys/' directory

    :param messageFilename: Name of .txt file containing a message, that is going to be encrypted
    :param keyFilename: Name of .txt file containing keySize and Two more KEYS
    :param blockSize: Size of single chunk of numbers
    '''
    if not os.path.exists("./keys/"):
        if os.getcwd() != 'C:\\WINDOWS\\system32':
            print("ERROR !\nNo 'keys' directory was found\nWant to create one?")
            print("Yes - 'Y'\nor\nNo - 'N'")
            userInput = input(" > ")[:1]
            if userInput.strip().upper().startswith('Y'):
                os.mkdir("keys")
                print("Directory 'keys' was created")
                os.system("pause")
            return
        else:
            print("WARNING !!!\n\
                OPENED IN 'C:\\WINDOWS\\system32'\n\
                PLEASE, RUN THIS SCRIPT VIA CMD, OPENED IN CURRENT DIRECTORY.\n")
            os.system("pause")
            sys.exit()

    if not os.path.exists("./keys/" + keyFilename):
        print(f"ERROR !\n'{keyFilename}' does not exist in '/keys/' directory !")
        os.system("pause")
        return

    if not os.path.exists("./messages/"):
        if os.getcwd() != 'C:\\WINDOWS\\system32':
            print(f"ERROR !\nNo 'messages' directory was found\nWant to create one?")
            print("Yes - 'Y'\nor\nNo - 'N'")
            userInput = input(" > ")[:1]
            if userInput.strip().upper().startswith('Y'):
                os.mkdir("messages")
                print("Directory 'messages' was created")
                os.system("pause")
            return
        else:
            print("WARNING !!!\n\
                OPENED IN 'C:\\WINDOWS\\system32'\n\
                PLEASE, RUN THIS SCRIPT VIA CMD, OPENED IN CURRENT DIRECTORY.\n")
            os.system("pause")
            sys.exit()

    if not os.path.exists("./messages/" + messageFilename):
        print(f"ERROR !\n'{messageFilename}' does not exist in '/messages/' directory !")
        os.system("pause")
        return
    
    encryptedMessageFilename: str = messageFilename[:-4] + "_encrypted.txt"
    if os.path.exists("./messages/" + encryptedMessageFilename):
        print(f"This function will re-write already existing file:")
        print(f"'{encryptedMessageFilename}'")
        print("\nDo you wish to CONTINUE (re-writing file)?\n")
        print("Yes - 'Y'\nor\nNo - 'N'")
        userInput = input(" > ")[:1]
        if not userInput.strip().upper().startswith('Y'):
            return

    keySize, n, e = readKeyFromFile(keyFilename)
    if blockSize == None:
        blockSize = int(math.log(2 ** keySize, SYMBOLS_LEN))
    
    # Checking if keyLen is enough for given Block Size
    elif int(math.log(2 ** keySize, SYMBOLS_LEN)) < blockSize:
        print("ERROR !!!\nBlock size is too large for the key and symbol set size.")
        sys.exit()

    file_obj = open("./messages/" + messageFilename, 'r')
    message: str = file_obj.read()
    file_obj.close()

    encryptedBlocks = encryptMessage(message, (n, e), blockSize)
    # Transforming ints to strings to then write them into .txt
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    
    # Editing all content so that it contains needed information
    encryptedContent = ','.join(encryptedBlocks)
    encryptedContent = f"{len(message)}_{blockSize}_{encryptedContent}"

    file_obj = open("./messages/" + encryptedMessageFilename, 'w')
    file_obj.write(encryptedContent)
    file_obj.close()

    print("\nDo you wish to add encrypted message to a Clipboard?\n")
    print("Yes - 'Y'\nor\nNo - 'N'")
    userInput = input(" > ")[:1]
    if userInput.strip().upper().startswith('Y'):
       add_clipboard(encryptedContent)
    return    


def decryptFile(messageFilename: str, keyFilename: str):
    '''
    Decrypts text from given messageFile using keys from keyFile\n
    Then Decrypted text being written into "new" file

    NOTE 1: messageFile should be in '/messages/' directory
    NOTE 2: keyFile should be in '/keys/' directory

    :param messageFilename: Name of .txt file containing: 
        1) Length of initial message\n
        2) Size of single block of numbers\n
        3) Message, that is going to be decrypted\n
    :param keyFilename: Name of .txt file containing keySize and Two more KEYS
    '''
    if not os.path.exists("./keys/"):
        if os.getcwd() != 'C:\\WINDOWS\\system32':
            print("ERROR !\nNo 'keys' directory was found\nWant to create one?")
            print("Yes - 'Y'\nor\nNo - 'N'")
            userInput = input(" > ")[:1]
            if userInput.strip().upper().startswith('Y'):
                os.mkdir("keys")
                print("Directory 'keys' was created")
                os.system("pause")
            return
        else:
            print("WARNING !!!\n\
                OPENED IN 'C:\\WINDOWS\\system32'\n\
                PLEASE, RUN THIS SCRIPT VIA CMD, OPENED IN CURRENT DIRECTORY.\n")
            os.system("pause")
            sys.exit()

    if not os.path.exists("./keys/" + keyFilename):
        print(f"ERROR !\n'{keyFilename}' does not exist in '/keys/' directory !")
        os.system("pause")
        return

    if not os.path.exists("./messages/"):
        if os.getcwd() != 'C:\\WINDOWS\\system32':
            print(f"ERROR !\nNo 'messages' directory was found\nWant to create one?")
            print("Yes - 'Y'\nor\nNo - 'N'")
            userInput = input(" > ")[:1]
            if userInput.strip().upper().startswith('Y'):
                os.mkdir("messages")
                print("Directory 'messages' was created")
                os.system("pause")
            return
        else:
            print("WARNING !!!\n\
                OPENED IN 'C:\\WINDOWS\\system32'\n\
                PLEASE, RUN THIS SCRIPT VIA CMD, OPENED IN CURRENT DIRECTORY.\n")
            os.system("pause")
            sys.exit()

    if not os.path.exists("./messages/" + messageFilename):
        print(f"ERROR !\n'{messageFilename}' does not exist in '/messages/' directory !")
        os.system("pause")
        return
    
    decryptedMessageFilename: str = messageFilename[:-4] + "_decrypted.txt"
    if os.path.exists("./messages/" + decryptedMessageFilename):
        print(f"This function will re-write already existing file:")
        print(f"'{decryptedMessageFilename}'")
        print("\nDo you wish to CONTINUE (re-writing file)?\n")
        print("Yes - 'Y'\nor\nNo - 'N'")
        userInput = input(" > ")[:1]
        if not userInput.strip().upper().startswith('Y'):
            return

    keySize, n, d = readKeyFromFile(keyFilename)

    file_obj = open("./messages/" + messageFilename, 'r')
    content: str = file_obj.read()
    file_obj.close()
    msgLen, blockSize, encryptedMessage = content.split('_')
    msgLen = int(msgLen)
    blockSize = int(blockSize)

    if int(math.log(2 ** keySize, SYMBOLS_LEN)) < blockSize:
        print("ERROR !!!\nBlock size is too large for the key and symbol set size.")
        print("Cannot decrypt with given keys")
        return

    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))
    
    message: str = decryptMessage(encryptedBlocks, msgLen, (n, d), blockSize)

    file_obj = open("./messages/" + decryptedMessageFilename, 'w')
    file_obj.write(message)
    file_obj.close()

    print("\nDo you wish to add message to a Clipboard?\n")
    print("Yes - 'Y'\nor\nNo - 'N'")
    userInput = input(" > ")[:1]
    if userInput.strip().upper().startswith('Y'):
       add_clipboard(message)
    return    

########################

def getUserMessage(purpose: str) -> str | int:
    '''
    :param purpose: Either 'Message' or 'Message Length'
    '''
    print(f"Enter a {purpose}")
    message: str = input(" > ")
    if purpose == "Message":
        return message[:len(message)]
    if purpose == "Message Length":
        try:
            return int(message)
        except Exception:
            raise Exception
            # sys.exit()

def getEncryptedBlocks() -> List[int]:
    print("Enter Encrypted Blocks one-by-one\n'ENTER' key to stop\n")
    userInput: str = '_'
    encryptedBlocks: List[int] = []
    while userInput != '':
        userInput = input(" > ")
        try:
            encryptedBlocks.append(int(userInput))
        except Exception:
            print("Wrong input (NAN)")

def getKeys(operation: str) -> tuple[int, int]:
    '''
    :param operation: Either 'Encrypt' or 'Decrypt'
    '''
    print("Enter 'n' key", end='')
    n: int = int(input(" > "))

    if operation == 'Encrypt':
        print("Enter 'e' key", end='')
        e: int = int(input(" > "))
        return (n, e)
    if operation == 'Decrypt':
        print("Enter 'd' key", end='')
        d: int = int(input(" > "))
        return (n, d)

def getFilename(purpose: str) -> str:
    '''
    :param purpose: Either 'Message' or 'Keys'
    '''
    print(f"Enter {purpose} .txt file filename\n(without .txt part)")
    filename: str = input(" > ")
    return filename + ".txt"

def getBlockSize() -> int | None:
    print("Enter a BlockSize for encryption:\n\
You can also just hit 'ENTER' to use basic size") # 'ENTER' key => Exception
    keysize: str = input(" > ")
    try:
        keysize = int(keysize)
        if keysize <= 2**11:
            return keysize
        else:
            print("Value is TOO BIG !\nUsing 256 Bits\n")
            return 256
    except Exception:
        return None

########################

if __name__ == "__main__":
    main()
    