import math, random # random -> secrets
from typing import List

def main():
    # Test
    print(primeSieve(109))


def isPrimeTrivial(num: int) -> bool:
    '''
    Trivial check whether given NUMBER is PRIME or NOT

    It checks all integers up to sqrt(num), including it whole part

    :param num: Number being checked
    :return: True (is indeed PRIME) or False (not a PRIME) 
    '''

    if num < 2: return False

    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False

    return True


def primeSieve(size: int) -> List[int]:
    '''
    Makes a Sieve of Eratosthenes using SIZE numbers (0, 1, ..., SIZE)

    :param size: Largest integer being checked
    :return: List of prime numbers <= Size
    '''
    size += 1

    sieve: List[bool] = [True] * size
    sieve[0], sieve[1] = False, False # 0 and 1 are not PRIMES

    for i in range(2, int(math.sqrt(size)) + 1):
        pointer = i * 2
        while pointer < size:
            sieve[pointer] = False
            pointer += i
    
    primes: List[int] = []
    
    for i in range(size):
        if sieve[i] == True:
            primes.append(i)
    
    return primes


def RabinMillerTest(num: int) -> bool:
    '''
    Checks whether given NUMBER is PRIME or NOT using Rabin-Miller Algorithm

    :param num: Number being checked
    :return: True (is indeed PRIME) or False (not a PRIME) 
    '''

    if num % 2 == 0 or num < 2: return False
    if num == 3:                return True

    temp = num - 1
    times = 0

    while temp % 2 == 0:
        temp = temp // 2
        times += 1
    
    for _ in range(5): # Checking 5 times
        RNGint = random.randrange(2, num - 1)
        v = pow(RNGint, temp, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == (times - 1):
                    return False
                else:
                    i = i + 1
                    v = pow(v, 2, num)
    
    return True


LOW_PRIMES = primeSieve(1000)

def isPrime(num: int) -> bool:
    '''
    :param num: Number being checked
    :return: True (is indeed PRIME) or False (not a PRIME) 
    '''
    if num < 2: return False
    
    for prime in LOW_PRIMES:
        if num == prime:
            return True
        if num % prime == 0:
            return False
    
    return RabinMillerTest(num)

    
def generateLargePrime(keysize: int = 1024) -> int:
    '''
    Generates a random (keysize) bit PRIME integer
    
    :param keysize: Amount of bits given to generating integer
    :return: Large Prime Integer (keysize) bits size
    '''
    while True:
        num = random.randrange( pow(2, keysize - 1), pow(2, keysize) )
        if isPrime(num):
            return num


if __name__ == "__main__":
    main()
