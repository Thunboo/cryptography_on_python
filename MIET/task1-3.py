###################
# Шифр Цезаря     #
###################
from vars import (TEXT, 
                  ALPHABET, 
                  ALPHABET_LENGTH,
                  SEPARATION_PERIOD, 
                  prepare_text)

letter_to_number = {}
for i in range(ALPHABET_LENGTH):
    letter_to_number[ALPHABET[i]] = i
number_to_letter = {v:k for k,v in letter_to_number.items()}

def get_key() -> int:
    try:
        key = int(input("Enter a Key: (int)\n> "))
        return key
    except Exception:
        print('wrong input')
        return get_key()
    
def caesar_cipher(text: str, key: int) -> str:
    output = []
    cnt = 0
    for letter in prepare_text(text):
        cnt += 1
        id = (letter_to_number[letter] + key) % ALPHABET_LENGTH
        output.append(number_to_letter[id])
        if cnt == SEPARATION_PERIOD:
            cnt = 0
            output.append(' ')
    return ''.join(output)

if __name__ == '__main__':
    while True:
        keyType = input("(C)ustom key or (D)efault key?\n> ")
        if keyType.capitalize().startswith('C'):
            key =  get_key()
            break
        elif keyType.capitalize().startswith('D'):
            key = 3
            break
    print(caesar_cipher(TEXT, key))
    print(caesar_cipher(caesar_cipher(TEXT, key), -1*key))