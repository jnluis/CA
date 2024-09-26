# João Luís, CA, September 2024

import sys
from ciphers import *
from stats import *


def main():
    # receives an argument from the command line
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <arg>")
        sys.exit(1)
    argtext = readfile(sys.argv[1])

    # Menu for user options
    print("Choose an option:\n")
    print("1. Analyse the text")
    print("2. Analyse the text, encrypt, and analyse the encrypted text")
    print("3. Analyse ciphertext, decrypt, and analyse the plaintext")
    print("4. Kasiski Examination for Vigenère ciphertext")
    print("5. Index of Coincidence for Vigenère ciphertext\n")

    option = input("Option: ")

    if option == "1":
        print("Frequency analysis of the plaintext:")
        frequency_and_n_grams(argtext)

    elif option == "2":
        print("Frequency analysis of the plaintext:")
        frequency_and_n_grams(argtext)

        # Encrypt the text
        print("\nChoose a cipher for encryption. Press q to exit.\n")
        print("1. Caesar")
        print("2. Vigenère\n")

        cipher_choice = input("Cipher: ")
        if cipher_choice.lower() == "q":
            print("No cipher chosen. Exiting program.")
            sys.exit(0)

        if cipher_choice == "1":
            rotation = int(input("Rotation: "))
            encrypted_text = Caesar_encrypt_decrypt(rotation, argtext)
            with open("Caesar_encrypted.txt", "w") as file:
                file.write(encrypted_text)
            print("Encrypted text written to Caesar_encrypted.txt")

            print("\nFrequency analysis of the encrypted text:")
            frequency_and_n_grams(encrypted_text)

        elif cipher_choice == "2":
            key = input("Enter the Vigenère cipher key: ")
            encrypted_text = Vigenere_cipher_encrypt(key, argtext)
            with open("Vigenere_encrypted.txt", "w") as file:
                file.write(encrypted_text)
            print("Encrypted text written to Vigenere_encrypted.txt")

            print("\nFrequency analysis of the encrypted text:")
            frequency_and_n_grams(encrypted_text)

        else:
            print("Invalid cipher choice. Exiting.")
            sys.exit(1)

    elif option == "3":
        ciphertext = readfile(input("Enter the path of the ciphertext file: "))

        print("Frequency analysis of the ciphertext:")
        frequency_and_n_grams(ciphertext)

        # Decrypt the text
        print("\nChoose a cipher for decryption. Press q to exit.\n")
        print("1. Caesar")
        print("2. Vigenère\n")

        cipher_choice = input("Cipher: ")
        if cipher_choice.lower() == "q":
            print("No cipher chosen. Exiting program.")
            sys.exit(0)

        if cipher_choice == "1":
            rotation = int(input("Rotation: "))
            decrypted_text = Caesar_encrypt_decrypt(
                -rotation, ciphertext
            )  # In Caesar cipher, decrypting is the same as encrypting with a negative rotation
            with open("Caesar_decrypted.txt", "w") as file:
                file.write(decrypted_text)
            print("Decrypted text written to Caesar_decrypted.txt")

            print("\nFrequency analysis of the decrypted text:")
            frequency_and_n_grams(decrypted_text)

        elif cipher_choice == "2":
            key = input("Enter the Vigenère cipher key: ")
            decrypted_text = Vigenere_cipher_decrypt(key, ciphertext)
            with open("Vigenere_decrypted.txt", "w") as file:
                file.write(decrypted_text)
            print("Decrypted text written to Vigenere_decrypted.txt")

            print("\nFrequency analysis of the decrypted text:")
            frequency_and_n_grams(decrypted_text)

        else:
            print("Invalid cipher choice. Exiting.")
            sys.exit(1)

    elif option == "4":
        numbers = input(
            "\nIntroduce the minimum and maximum numbers of n_grams to analyse, separated by a space: "
        )
        n_gram_min, n_gram_max = numbers.split()

        print("Kasiski examination:")
        kasiski_exam(argtext, int(n_gram_min), int(n_gram_max))

    elif option == "5":
        max_key_length = int(
            input("\nIntroduce the maximum number of key lengths to analyse: ")
        )

        print("Index of Coincidence:")
        index_of_coincidence(argtext, max_key_length)
        Ioc_plot()


if __name__ == "__main__":
    main()
