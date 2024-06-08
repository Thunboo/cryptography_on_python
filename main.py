import os
from Caesar.main_caesar import main_caesar
from Transposition.main_transposition import main_transposition

def main():
    option: int = -1
    while (True):
        os.system("cls")
        print("""Welcome to Universal Cipher Master!
    Pick an option:
    0) Leave...
    1) Caesar Cipher
    2) Transposition Cipher
    3) ...""")

        option = int(input()[:1])
        os.system("cls")
        if option == 0: break
        else:
            if option == 1: main_caesar()
            elif option == 2: main_transposition()
            elif option == 3: print("Nothing here yet...\n")
            os.system("pause")


if __name__ == "__main__":
    main()