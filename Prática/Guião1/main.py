# João Luís, CA, September 2024

import sys
from collections import Counter
from ciphers import *
import re
from unicodedata import normalize

letters = "abcdefghijklmnopqrstuvwxyz"


def frequency_and_n_grams(cleantext):
    total_number_of_letters = 0
    letter_dict = {letter: 0 for letter in letters}
    for letter in cleantext:
        if letter in letter_dict:
            letter_dict[letter.lower()] += 1

    sorted_pairs = sorted(
        [(value, key) for (key, value) in letter_dict.items()], reverse=True
    )
    total_number_of_letters = sum(
        letter_dict.values()
    )  # Como já não tem espaços e pontuação, também podíamos fazer a length do texto

    for value, letter in sorted_pairs:
        percentage = value / total_number_of_letters
        print(f"{letter}: {value} ({percentage:.3%})")

    # Count and print n-grams (digrams and trigrams)
    for n in [2, 3]:  # For both digrams and trigrams
        ngrams = [cleantext[i : i + n] for i in range(len(cleantext) - n + 1)]
        ngram_counts = Counter(ngrams)
        sorted_ngrams = sorted(ngram_counts.items(), key=lambda x: x[1], reverse=True)

        print(f"\n{n}-gram Frequencies:")
        for ngram, count in sorted_ngrams:
            percentage = count / sum(ngram_counts.values())
            if (
                " " in ngram
            ):  # Como não tirei os espaços do texto (se for suposto, meter na função readfile ), meti aqui este if
                continue
            if (
                percentage > 0.01
            ):  # Só interessa os n-grams que têm uma frequência superior a 1%
                print(f"{ngram}: {count} ({percentage:.3%})")


def readfile(pathfile):
    cleantext = ""
    with open(pathfile, "r", encoding="utf-8") as file:
        for line in file:
            nfkd = normalize("NFKD", line)
            cleantext += "".join([c for c in nfkd if c.isalpha()]).lower()

            # cleantext = (
            #     line.strip()
            # )  # não sei se é preciso tirar a pontuação e os espaços ou se mantemos tudo como o original
    return cleantext


def main():
    # receives an argument from the command line
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <arg>")
        sys.exit(1)
    cleantext = readfile(sys.argv[1])

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
        frequency_and_n_grams(cleantext)

    elif option == "2":
        print("Frequency analysis of the plaintext:")
        frequency_and_n_grams(cleantext)

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
            encrypted_text = Caesar_encrypt_decrypt(rotation, cleantext)
            with open("Caesar_encrypted.txt", "w") as file:
                file.write(encrypted_text)
            print("Encrypted text written to Caesar_encrypted.txt")

            print("\nFrequency analysis of the encrypted text:")
            frequency_and_n_grams(encrypted_text)

        elif cipher_choice == "2":
            key = input("Enter the Vigenère cipher key: ")
            encrypted_text = Vigenere_cipher_encrypt(key, cleantext)
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
        ciphertext = readfile(input("Enter the path of the ciphertext file: "))
        numbers = input(
            "\nIntroduce the minimum and maximum numbers of n_grams to analyse, separated by a space: "
        )
        n_gram_min, n_gram_max = numbers.split()

        print("Kasiski examination:")
        kasiski_exam(ciphertext, int(n_gram_min), int(n_gram_max))

    elif option == "5":
        ciphertext = readfile(input("Enter the path of the ciphertext file: "))

        print("Index of Coincidence:")


if __name__ == "__main__":
    main()
