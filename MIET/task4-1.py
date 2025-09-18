###################
# Шифр Виженера 1 #
###################
from vars import (TEXT, 
                  ALPHABET, 
                  ALPHABET_LENGTH,
                  SEPARATION_PERIOD, 
                  prepare_text)

#
# Каждой цифре алфавита ставится в соответствие число от 0 до 31 - мощность алфавита - 32
# Пример последующего использования:
# АБВ + ХАБВ = (А+Х)(Б+А)(В+Б) = (0 + 21)(1+0)(2+1) = ХБГ
letter_to_number = {}
for i in range(ALPHABET_LENGTH):
    letter_to_number[ALPHABET[i]] = i
number_to_letter = {v:k for k, v in letter_to_number.items()}

def encode(text: str, key: str) -> str:
    key = key.lower()
    output = []
    cnt = 0
    text = prepare_text(text)
    gamma = key + text
    for i in range(len(text)):
        cnt += 1
        output.append(number_to_letter[
                (letter_to_number[text[i]] + letter_to_number[gamma[i]]) % ALPHABET_LENGTH
            ])
        if cnt == SEPARATION_PERIOD:
            cnt = 0
            output.append(' ')
    return ''.join(output)

def decode(ciphertext: str, key: str) -> str:
    key = key.lower()
    output = [key]
    ciphertext = prepare_text(ciphertext)
    for i in range(len(ciphertext)):
        # print(ciphertext[i], output[i])
        output.append(number_to_letter[
                (letter_to_number[ciphertext[i]] - letter_to_number[output[i]]) % ALPHABET_LENGTH
            ])
    return ''.join(output[1:])

def ciph_encode(text, key1, key2: str) -> str:
    ciphertext = prepare_text(encode(text, key1))
    text = prepare_text(text)
    output = []
    cnt = 0
    gamma = key2.lower() + ciphertext
    for i in range(len(text)):
        cnt += 1
        output.append(number_to_letter[
                (letter_to_number[text[i]] + letter_to_number[gamma[i]]) % ALPHABET_LENGTH
            ])
        # print(f"{gamma[i]} + {text[i]} = {output[-1]}")
        if cnt == SEPARATION_PERIOD:
            cnt = 0
            output.append(' ')
    return ''.join(output)

def ciph_decode(ciphertext, key1, key2: str) -> str:
    ciphertext = prepare_text(ciphertext)
    output = []
    gamma  = [key2.lower()]
    gamma2 = [key1.lower()]
    
    for i in range(len(ciphertext)):
        output.append(number_to_letter[
                (letter_to_number[ciphertext[i]] - letter_to_number[gamma[i]]) % ALPHABET_LENGTH
            ])
        gamma.append(number_to_letter[
                (letter_to_number[output[i]] + letter_to_number[gamma2[i]]) % ALPHABET_LENGTH
            ])
        gamma2.append(output[-1])
        # print(f"{ciphertext[i]} - {gamma[-2]} = {output[-1]} + {gamma2[-2]} = {gamma[-1]}")
#         print(f"{letter_to_number[ciphertext[i]]} - {letter_to_number[gamma[-2]]} \
# = {letter_to_number[output[-1]]} + {letter_to_number[gamma2[-2]]} = \
# {letter_to_number[gamma[-1]]}")
        # input()
    return ''.join(output)

if __name__ == '__main__':
    txt = TEXT
    print(encode(txt, 'А')) 
    
    print(ciph_encode(txt, 'А', 'А'))
    print(ciph_decode(ciph_encode(txt, 'А', 'А'), 'А', 'А'))
    # print(ciph_decode('ыджжу яалхс фжаяс ьпяир вкбнп жшэци шычбк дфион ркмцр пшзиг цтдчу', 'Д', 'О'))
    # print(decode(encode(txt, 'Х'), 'Х'))
    # print(encode(encode(txt, 'Б'), 'Б'))
    # print(decode(decode(encode(encode(txt, 'Б'), 'Б'), 'Б'), 'Б')) 
    