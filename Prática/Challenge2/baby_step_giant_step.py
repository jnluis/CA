from math import ceil, sqrt


def bsgs(g, h, p):
    """
    Solve for x in h = g^x mod p given a prime p using Baby Step Giant Step algorithm.
    """
    N = ceil(sqrt(p - 1))  # N is approximately the square root of (p - 1)

    # Baby step: Store hashmap of g^{1...N} (mod p)
    tbl = {pow(g, i, p): i for i in range(N)}

    # Fermat's Little Theorem: Compute g^(-N) mod p
    c = pow(g, N * (p - 2), p)  # g^{-N} mod p using Fermat's Little Theorem

    # Giant step: Check if h * g^{-jN} mod p is in the baby steps table
    for j in range(N):
        y = (h * pow(c, j, p)) % p
        if y in tbl:
            return j * N + tbl[y]

    # Solution not found
    return None


# Given values for Diffie-Hellman key exchange
p = 3141592653589793239  # Prime modulus
r = 6  # Base (generator)
A = 2408130236552768716  # Alice's public key
B = 434542471090467423  # Bob's public key

# Step 1: Find alpha such that r^alpha ≡ A (mod p)
alpha = bsgs(r, A, p)
print(f"Private key alpha = {alpha}")

# Step 2: Find beta such that r^beta ≡ B (mod p)
beta = bsgs(r, B, p)
print(f"Private key beta = {beta}")

# Step 3: Compute the shared secret S = B^alpha mod p (or S = A^beta mod p)
S = pow(B, alpha, p)  # Shared secret
print(f"Shared secret S = {S}")


# Fez bastante rápido os penúltimos valores do Slide 42 (r=10), mas deu killed para os numeros do sor.
