# TRANSPOSITION CIPHER BruteForce Hack File #
#############################################

from transposition_cipher import decryptTransposition

def bruteforce_hack_transposition(message: str) -> None:
    """
    BruteForces given string "message" with all possible "key"
    Then prints out all possible outcomes of unencrypted "message"
    :param message: message to be decrypted
    """
    max_len = len(message) # Amount of symbols <=> possible keys
    formated = len(str(max_len))
    print("All possible translations:\n")
    for key in range(1, max_len):
        print(f"Key = {key:{formated}.0f} | {decryptTransposition(message=message, key=key)}")


def main():
    message: str = input("Enter your encrypted message:\n")
    message = message[:len(message)]
    bruteforce_hack_transposition(message=message)


if __name__ == "__main__":
    main()