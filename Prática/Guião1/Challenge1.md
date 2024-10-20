# Non-cyclic Vigenère cipher
## João Luís, NMEC 107403

encryption key: joaoluis

Q: Explain the relevance of the key length for the robustness of this encryption algorithm against the Kasiski test.

A: Although we increment the last letter every N-letters, which introduces additional variation,
choosing a key with a small size can lead to patterns being found, as the key will be repeated 
more often throughout the cryptogram, especially if the cryptogram is a long text.
These patterns can be detected by the Kasiski test, which tries to predict the size of the key.

Note: To run the program, do this on terminal: ```python3 main.py <path_to_file>```