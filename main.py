import os
# import sys
# # Get the parent directory
# parent_dir = os.path.dirname(os.path.realpath(__file__))

# # Add the parent directory to sys.path
# sys.path.append(parent_dir)

# Import the module from the parent directory
import script.menu_options as menu
import script.caesar_script as caesar
import script.transposition_script as transposition

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
    3) ...""")

        option = int(input()[:1])
        os.system("cls")
        if option == 0: break
        else:
            if option == 1: caesar.main()
            elif option == 2: transposition.main()
            elif option == 3: 
                print("Nothing here yet...\n")
                os.system("pause")


if __name__ == "__main__":
    main()