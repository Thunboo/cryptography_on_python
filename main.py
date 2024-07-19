import os
import script.caesar_script as caesar
import script.transposition_script as transposition
import script.affine_script as affine
import script.simplesub_script as simpSub
import script.vigenere_script as vigenere
import script.genPublicPrivateKeys as generateKeys
import script.publickey_script as publicKey

def main():
    option: int = -1
    while (True):
        os.system("cls")
        # print(os.getcwd())
        print("""Welcome to Universal Cipher Master!
    Pick an option:
    0) Leave...
    1) Caesar Cipher
    2) Transposition Cipher
    3) Affine Cipher
    4) Simple Substitution Cipher
    5) Vigenere Cipher
    6) Public Key Cipher
    7) Key Generator""")

        option = int(input()[:1])
        os.system("cls")
        if option == 0: break
        else:
            if option == 1: caesar.main()
            elif option == 2: transposition.main()
            elif option == 3: affine.main()
            elif option == 4: simpSub.main()
            elif option == 5: vigenere.main()
            elif option == 6: publicKey.main()
            elif option == 7: generateKeys.main()


if __name__ == "__main__":
    main()