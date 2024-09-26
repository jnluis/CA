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


def Vigenere_cipher_encrypt(key, text):
    encrypted_text = ""
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            if char.islower():
                encrypted_text += chr(
                    (ord(char) - 97 + ord(key[key_index]) - 97) % 26 + 97
                )
            else:
                encrypted_text += chr(
                    (ord(char) - 65 + ord(key[key_index]) - 97) % 26 + 65
                )
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
