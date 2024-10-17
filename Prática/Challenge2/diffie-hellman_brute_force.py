from Crypto.PublicKey import DSA
from Crypto.Math.Numbers import Integer

# Given values
p = Integer(31415926541)
r = Integer(10)
A = Integer(5728872032)  # Alice's public key
B = Integer(22727460975)  # Bob's public key


# Brute force method to find alpha or beta using modular arithmetic
def discrete_log_brute_force(r, A, p):
    # Try all possible values of alpha
    for alpha in range(1, p):
        if pow(r, alpha, p) == A:
            return alpha
    return None


# Finding alpha and beta
alpha = discrete_log_brute_force(r, A, p)
beta = discrete_log_brute_force(r, B, p)

if alpha is not None:
    print(f"Found alpha: {alpha}")
else:
    print("Could not find alpha using brute force.")

if beta is not None:
    print(f"Found beta: {beta}")
else:
    print("Could not find beta using brute force.")

# Calculate the shared secret S
if alpha is not None:
    S = pow(B, alpha, p)  # B^alpha % p
    print(f"Shared secret S = {S}")
else:
    print("Could not compute shared secret without alpha or beta.")
