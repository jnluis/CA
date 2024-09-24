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
