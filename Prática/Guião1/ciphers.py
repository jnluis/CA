# João Luís, CA, September 2024


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


def Vigenere_cipher_encrypt(
    key, text, rotate_increment=False
):  # Ex5 feito com esta função também
    encrypted_text = ""
    key = key.lower()
    key_index = 0
    key_length = len(key)

    for i, char in enumerate(text):
        if char.isalpha():
            if char.islower():
                encrypted_text += chr(
                    (ord(char) - 97 + ord(key[key_index]) - 97) % 26 + 97
                )
            else:
                encrypted_text += chr(
                    (ord(char) - 65 + ord(key[key_index]) - 97) % 26 + 65
                )
            key_index = (key_index + 1) % key_length

            if rotate_increment and (i + 1) % key_length == 0:
                key = rotate_and_increment_key(key)
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
                decrypted_text += chr(
                    (ord(char) - 97 - (ord(key[key_index]) - 97)) % 26 + 97
                )
            else:
                decrypted_text += chr(
                    (ord(char) - 65 - (ord(key[key_index]) - 97)) % 26 + 65
                )
            key_index = (key_index + 1) % len(key)
        else:
            decrypted_text += char
    return decrypted_text


def rotate_and_increment_key(key):
    key = (
        key[1:] + key[0]
    )  # Os caracteres andam todos para trás uma casa, e o primeiro caractere passa a ser o último
    last_char = chr((ord(key[-1]) - 97 + 1) % 26 + 97)  # modulo 26 plus 'a'
    key = key[:-1] + last_char
    return key
