# João Luís, CA, September 2024

from collections import Counter
from unicodedata import normalize
import math
import matplotlib.pyplot as plt

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

    return cleantext


def prime_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n // i
    if n > 2:
        factors.append(n)
    return factors


def kasiski_exam(ciphertext, min_n, max_n):
    for n in range(min_n, max_n + 1):  # Loop over the range of n-gram lengths
        print(f"\nAnalyzing {n}-grams:")

        # Find all repeated n-grams in the ciphertext
        repeated_ngrams = {}
        for i in range(len(ciphertext) - n + 1):
            ngram = ciphertext[i : i + n]

            if " " in ngram or "," in ngram:
                continue

            if ngram in repeated_ngrams:
                repeated_ngrams[ngram].append(i)
            else:
                repeated_ngrams[ngram] = [i]

        # Filter out n-grams that don't repeat
        repeated_ngrams = {
            ngram: positions
            for ngram, positions in repeated_ngrams.items()
            if len(positions) > 1
        }

        if not repeated_ngrams:
            print(f"No repeated {n}-grams found.")
            continue

        # Calcular a distância entre os n-grams repetidos
        ngram_distances = []
        for positions in repeated_ngrams.values():
            for i in range(len(positions) - 1):
                distance = positions[i + 1] - positions[i]
                ngram_distances.append(distance)

        # Para ver quais são os n-grams encontrados
        # print("Repeated n-grams and their positions:")
        # for ngram, positions in repeated_ngrams.items():
        #    print(f"{ngram}: {positions}")

        distance_counts = Counter(ngram_distances)

        print(
            "\nDistance frequencies (most common distances may indicate the key length):"
        )
        for distance, count in distance_counts.most_common():
            print(f"Distance: {distance}, Count: {count}")

        # Para os 5 mais comuns, calcular os fatores primos
        print("\nPrime factorization of top 5 distances:")
        for distance, count in distance_counts.most_common(5):
            factors = prime_factors(distance)
            factorization = " * ".join(map(str, factors))
            print(f"{distance} = {factorization}")

    return distance_counts


# Este algoritmo segue a ideia deste vídeo: https://www.youtube.com/watch?v=zmKCaKYkBMU&t=222s
def index_of_coincidence(text, max_key_length):
    with open("IoC.txt", "w") as file:
        for key_length in range(2, max_key_length + 1):  # Key lengths starting from 2
            substrings = [text[i::key_length] for i in range(key_length)]

            # Primeiro calculamos o indíce de coincidência para cada substring
            indices_of_coincidence = []
            for substring in substrings:
                n = len(substring)
                letter_counts = Counter(substring)
                ioc = sum(count * (count - 1) for count in letter_counts.values()) / (
                    n * (n - 1)
                )  # Fórmula do Wikipédia, sem o C do número de carateres do alfabeto
                indices_of_coincidence.append(ioc)

            # Depois calculamos a média dos índices de coincidência daquele grupo
            if indices_of_coincidence:
                average_ioc = sum(indices_of_coincidence) / len(indices_of_coincidence)
                print(f"Average IoC for key length {key_length}: {average_ioc:.5f}")
                file.write(f"{key_length} {average_ioc:.5f}\n")


def Ioc_plot():
    key_lengths = []
    iocs = []
    with open("IoC.txt", "r") as file:
        for line in file:
            key_length, avg_IoC = line.split()
            key_lengths.append(int(key_length))
            iocs.append(float(avg_IoC))

    plt.plot(key_lengths, iocs)
    plt.xlabel("Key length")
    plt.ylabel("Average IoC")
    plt.title("Index of Coincidence")
    plt.savefig("IoC_plot.png")
