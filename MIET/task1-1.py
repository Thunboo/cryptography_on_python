##############
# Шифр АТБАШ #
##############
from vars import (TEXT, 
                  ALPHABET, 
                  ALPHABET_LENGTH, 
                  SEPARATION_PERIOD,
                  prepare_text)


################
# Делаем словарь однозначной замены по шифру АТБАШ
translation = {}
n = ALPHABET_LENGTH
for i in range(n):
    translation[ALPHABET[i]] = ALPHABET[n-i-1]

def atbash_translate_text(text: str):
    text = prepare_text(text)
    new_text = []
    cnt = 0
    for letter in text:
        new_text.append(translation[letter])
        cnt += 1
        if cnt == SEPARATION_PERIOD:
            new_text.append(' ')
            cnt = 0
    return ''.join(new_text)

if __name__ == '__main__':
    print(atbash_translate_text(TEXT))
    print(atbash_translate_text(atbash_translate_text(TEXT)))