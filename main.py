import os
import script.caesar_script as caesar
import script.transposition_script as transposition
import script.affine_script as affine

def main():
    option: int = -1
    while (True):
        os.system("cls")
        print(os.getcwd())
        print("""Welcome to Universal Cipher Master!
    Pick an option:
    0) Leave...
    1) Caesar Cipher
    2) Transposition Cipher
    3) Affine Cipher
    4) ...""")

        option = int(input()[:1])
        os.system("cls")
        if option == 0: break
        else:
            if option == 1: caesar.main()
            elif option == 2: transposition.main()
            elif option == 3: affine.main()
            elif option == 4: 
                print("Nothing here yet...\n")
                os.system("pause")


if __name__ == "__main__":
    main()