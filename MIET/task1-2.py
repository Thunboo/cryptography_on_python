###################
# Квадрат Полибия #
###################
from vars import (TEXT, 
                  ALPHABET, 
                  ALPHABET_LENGTH,
                  SEPARATION_PERIOD, 
                  prepare_text)
from math import ceil, sqrt

n = ALPHABET_LENGTH
new = []
size = ceil(sqrt(n))
for i in range(0, n, size):
    tmp = []
    for j in range(i, i + size):
         if j >= n: break
         tmp.append(ALPHABET[j])
    new.append(tmp)

translation = {}
for i in range(size):
    for j in range(size):
        try:
            translation[new[i][j]] = f'{i+1}{j+1}'
        except IndexError:
            break

def polybius_encode_text(text: str):
    text = prepare_text(text)
    new_text = []
    cnt = 0
    for letter in text:
        new_text.append(translation[letter])
        new_text.append(' ')
    return ''.join(new_text)

inv_translation = {v: k for k, v in translation.items()}
def polybius_decode_text(text: str):
    text = prepare_text(text)
    new_text = []
    cnt = 0
    for i in range(0, len(text), 2):
        new_text.append(inv_translation[text[i:i+2]])
        cnt += 1
        if cnt == SEPARATION_PERIOD:
            new_text.append(' ')
            cnt = 0
    return ''.join(new_text)

if __name__ == '__main__':
    print(polybius_encode_text(TEXT))
    print(polybius_decode_text(polybius_encode_text(TEXT)))