# João Luís, CA, September 2024

from collections import Counter

def Caesar_encrypt_decrypt(rotation, text):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                encrypted_text += chr((ord(char) - 97 + rotation) % 26 + 97)
            else:
                encrypted_text += chr((ord(char) - 65 + rotation) % 26 + 65)
        else:
            encrypted_text += char
    return encrypted_text

def Vigenere_cipher_encrypt(key, text):
    encrypted_text = ""
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            if char.islower():
                encrypted_text += chr((ord(char) - 97 + ord(key[key_index]) - 97) % 26 + 97)
            else:
                encrypted_text += chr((ord(char) - 65 + ord(key[key_index]) - 97) % 26 + 65)
            key_index = (key_index + 1) % len(key)
        else:
            encrypted_text += char
    return encrypted_text

def Vigenere_cipher_decrypt(key, text):
    decrypted_text = ""
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            if char.islower():
                decrypted_text += chr((ord(char) - 97 - (ord(key[key_index]) - 97)) % 26 + 97)
            else:
                decrypted_text += chr((ord(char) - 65 - (ord(key[key_index]) - 97)) % 26 + 65)
            key_index = (key_index + 1) % len(key)
        else:
            decrypted_text += char
    return decrypted_text

def kasiski_exam(ciphertext, min_n, max_n):
    ciphertext=ciphertext.replace(" ", "")
    for n in range(min_n, max_n + 1):  # Loop over the range of n-gram lengths
        print(f"\nAnalyzing {n}-grams:\n")

        # Find all repeated n-grams in the ciphertext
        repeated_ngrams = {}
        for i in range(len(ciphertext) - n + 1):
            ngram = ciphertext[i:i+n]

            if ' ' in ngram or ',' in ngram:
                continue
            
            if ngram in repeated_ngrams:
                repeated_ngrams[ngram].append(i)
            else:
                repeated_ngrams[ngram] = [i]
         
        # Filter out n-grams that don't repeat
        repeated_ngrams = {ngram: positions for ngram, positions in repeated_ngrams.items() if len(positions) > 1}

        if not repeated_ngrams:
            print(f"No repeated {n}-grams found.")
            continue

        # Calculate the distances between the repeated n-grams
        ngram_distances = []
        for positions in repeated_ngrams.values():
            for i in range(len(positions) - 1):
                distance = positions[i + 1] - positions[i]
                ngram_distances.append(distance)

        # Output the results
        print("Repeated n-grams and their positions:")
        for ngram, positions in repeated_ngrams.items():
            print(f"{ngram}: {positions}")

        # print("\nDistances between repeated n-grams:")
        # for distance in ngram_distances:
        #     print(distance)

        # Perform a frequency analysis on the distances to find common divisors
        distance_counts = Counter(ngram_distances)

        print("\nDistance frequencies (most common distances may indicate the key length):")
        for distance, count in distance_counts.most_common():
            print(f"Distance: {distance}, Count: {count}")

    return distance_counts
