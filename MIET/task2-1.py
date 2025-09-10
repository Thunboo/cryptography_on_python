###################
# Шифр Третимия   #
###################
from vars import (TEXT, 
                  ALPHABET, 
                  ALPHABET_LENGTH,
                  SEPARATION_PERIOD, 
                  prepare_text)


letter_to_number = {}
for i in range(ALPHABET_LENGTH):
    letter_to_number[ALPHABET[i]] = i + 1
number_to_letter = {v:k for k, v in letter_to_number.items()}

def encode(text: str) -> str:
    output = []
    cnt = 0
    text = prepare_text(text)
    for i in range(len(text)):
        cnt += 1
        output.append(number_to_letter[
                (letter_to_number[text[i]] + i) % ALPHABET_LENGTH + 1
            ])
        if cnt == SEPARATION_PERIOD:
            cnt = 0
            output.append(' ')
    return ''.join(output)


if __name__ == '__main__':
    print(encode(TEXT))