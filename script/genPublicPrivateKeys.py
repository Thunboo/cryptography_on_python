import random, sys, os
from . import primeNums #random -> secrets
from .affine_script import (
    greatestCommonDivisor as GCD,
    findModInverse        as FMI
    )


def generateKey(keysize: int = 1024) -> tuple[int, int]:
    '''
    :param keysize: Amount of bits given to key generator
    :return: Tuple containing both Public and Private Keys
    '''

    # Making Public and Private keys with length of (keysize) bits
    p, q = 0, 0

    # Step 1: Generating 2 prime nums (p and q)
    # Calculate n = p * q
    while p == q:
        p = primeNums.generateLargePrime(keysize)
        q = primeNums.generateLargePrime(keysize)
    n = p * q

    # Step 2: Making number 'e' co-prime to (p-1)*(q-1)
    while True:
        e = random.randrange( pow(2, keysize - 1), pow(2, keysize) )
        if GCD(e, (p-1)*(q-1)) == 1:
            break
    
    # Step 3: Calculating 'd' - module inverse to 'e'
    d = FMI(e, (p-1)*(q-1))

    publicKey  = (n, e)
    privateKey = (n, d)

    return (publicKey, privateKey)


def makeKeyFiles(name: str = 'new', keysize: int = 1024):
    '''
    Makes TWO files with both PUBLIC and PRIVATE keys

    :param name: Name of the files: \'name_public.txt\' and \'name_private.txt\'
    :param keysize: Amount of bits given to key generator
    '''
    if not os.path.exists('./keys/'):
        if os.getcwd() != 'C:\\WINDOWS\\system32':
            os.mkdir("keys")
        else:
            print("WARNING !!!\n\
                OPENED IN 'C:\\WINDOWS\\system32'\n\
                PLEASE, RUN THIS SCRIPT VIA CMD, OPENED IN CURRENT DIRECTORY.\n")
            os.system("pause")
            sys.exit()
        
    elif (os.path.exists('./keys/%s_publicKey.txt' % (name)) or
        os.path.exists('./keys/%s_privateKey.txt' % (name))):
        
        print('WARNING !!!\n\
            The file "%s_publicKey.txt" or "%s_privateKey.txt" already exists! \n\
            Use different name or delete these files. \n\
            Then You can rerun key generating program. \n' % (name, name))
        os.system("pause")
        sys.exit()


    publicKey, privateKey = generateKey(keysize)
    
    # Saving Public Key into a File
    filename: str = './keys/' + name + '_publicKey.txt'
    
    file_obj = open(file=filename, mode='w')
    file_obj.write(f"Key Size: {keysize}\nPublic Key Parts:\n\
                   {publicKey[0]}\n_____________\n{publicKey[1]}")
    file_obj.close()

    # Saving Private Key into a File
    filename: str = './keys/' + name + '_privateKey.txt'
    
    file_obj = open(file=filename, mode='w')
    file_obj.write(f"Key Size: {keysize}\nPrivate Key Parts:\n\
                   {privateKey[0]}\n_____________\n{privateKey[1]}")
    file_obj.close()


def getName() -> str:
    name: str = input("Enter Name for keys files:\n > ")
    return name[:len(name)]


def getKeysize() -> int:
    print("Enter a keysize for key generator:\n\
([128-4096] is preferable)\n\
You can also just hit 'ENTER' to use basic 1024 bits")
    keysize: str = input(" > ")
    try:
        keysize = int(keysize)
        if keysize <= 4096:
            return keysize
        else:
            print("Value is TOO BIG !\nUsing 1024 Bits\n")
            return 1024
    except Exception:
        return 1024


def main():
    print("Generating two keys...")
    makeKeyFiles(name=getName(), keysize=getKeysize())
    print("Done!")


if __name__ == "__main__":
    main()