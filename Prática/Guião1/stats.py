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
            if " " in ngram:
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
    for n in range(min_n, max_n + 1):
        print(f"\nAnalyzing {n}-grams:")

        repeated_ngrams = {}
        for i in range(len(ciphertext) - n + 1):
            ngram = ciphertext[i : i + n]

            if " " in ngram or "," in ngram:
                continue

            if ngram in repeated_ngrams:
                repeated_ngrams[ngram].append(i)
            else:
                repeated_ngrams[ngram] = [i]

        # Tirar fora n-grams que não se repetem
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


def determine_original_language(ciphertext, key_length):
    # Fontes: Inglês -> https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
    #        Francês -> https://www.sttmedia.com/characterfrequency-french
    #       Espanhol -> https://es.wikipedia.org/wiki/Frecuencia_de_aparici%C3%B3n_de_letras
    #      Português -> https://pt.wikipedia.org/wiki/Frequ%C3%AAncia_de_letras
    known_frequencies = {
        "english": {
            "e": 11.1607,
            "a": 8.4966,
            "r": 7.5809,
            "i": 7.5448,
            "o": 7.1635,
            "t": 6.9509,
            "n": 6.6544,
            "s": 5.7351,
            "l": 5.4893,
            "c": 4.5388,
            "u": 3.6308,
            "d": 3.3844,
            "p": 3.1671,
            "m": 3.0129,
            "h": 3.0034,
            "g": 2.4705,
            "b": 2.072,
        },
        "french": {
            "e": 15.1,
            "a": 8.13,
            "s": 7.91,
            "t": 7.11,
            "i": 6.94,
            "r": 6.43,
            "n": 6.42,
            "u": 6.05,
            "l": 5.68,
            "o": 5.27,
            "d": 3.55,
            "m": 3.23,
            "c": 3.15,
            "p": 3.03,
        },
        "spanish": {
            "e": 13.68,
            "a": 12.53,
            "o": 8.68,
            "s": 7.98,
            "r": 6.87,
            "n": 6.71,
            "i": 6.25,
            "d": 5.86,
            "l": 4.97,
            "c": 4.68,
            "t": 4.63,
            "u": 3.93,
            "m": 3.15,
            "p": 2.51,
        },
        "portuguese": {
            "a": 14.63,
            "e": 12.57,
            "o": 10.73,
            "s": 7.81,
            "r": 6.53,
            "i": 6.18,
            "n": 5.05,
            "d": 4.99,
            "m": 4.74,
            "u": 4.63,
            "t": 4.34,
            "c": 3.88,
            "l": 2.78,
            "p": 2.52,
        },
    }  # abaixo dos 2% não considerei porque já é terreno mais suscetível a ruído

    slices = [
        "" for _ in range(key_length)
    ]  # o underscore é uma convenção para variáveis que não são usadas
    slice_frequencies = []

    # Tem de ser assim, não pode ser com divisão normal ou //
    for i, char in enumerate(ciphertext):
        slices[i % key_length] += char

    for slice_index, slice in enumerate(slices):
        slice_freqs = Counter(slice)
        total_letters = sum(slice_freqs.values())

        # Normalize the frequencies
        slice_freqs = {
            letter: (count / total_letters) * 100
            for letter, count in slice_freqs.items()
        }
        slice_frequencies.append(slice_freqs)

        # dar uncomment deste bloco para ver que as frequências de cada slice são bastante similares
        # sorted_freqs = sorted(slice_freqs.items(), key=lambda x: x[1], reverse=True)
        # print(f"Slice {slice_index} frequency distribution (sorted):")
        # for letter, freq in sorted_freqs:
        #     print(f"{letter}: {freq:.2f}%")
        # print("\n")

    slice_language_scores = {}
    for slice_index, slice_freqs in enumerate(slice_frequencies):
        slice_language_scores[slice_index] = {}
        for language, freqs in known_frequencies.items():
            score = 0
            for letter, freq in freqs.items():
                score += abs(slice_freqs.get(letter, 0) - freq)
            slice_language_scores[slice_index][language] = score

    slice_language_assignments = {}
    for slice_index, language_scores in slice_language_scores.items():
        slice_language_assignments[slice_index] = min(
            language_scores, key=language_scores.get
        )
        # print(f"Slice {slice_index} is most likely {slice_language_assignments[slice_index]}")

    language_counts = Counter(
        slice_language_assignments.values()
    )  # Contar o número de vezes que cada língua aparece em cada slice
    most_likely_language = max(
        language_counts, key=language_counts.get
    )  # A língua que aparece mais vezes é a mais provável

    return most_likely_language
