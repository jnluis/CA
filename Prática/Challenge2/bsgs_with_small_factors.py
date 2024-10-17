# p= 3141592653589793239
# r =6
# A= 2408130236552768716
# B= 434542471090467423

# p= 31415926541
# r =10
# A= 5728872032
# B= 22727460975

import math


def mod_inverse(a, m):
    return pow(a, -1, m)


def find_small_factor(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return i
    return None


def baby_step_giant_step(g, b, q, p):
    d = pow(g, q, p)
    table = {}
    for j in range(q):
        table[pow(d, j, p)] = j

    x = 0
    while x < b:
        x += q
        if x >= p:
            x -= p
        if x in table:
            return x
    return None


def compute_shared_key(p, g, A, B):
    q = find_small_factor(p)
    if q is None:
        raise ValueError("p is not a bad prime")

    # Deduce private keys
    a_private = baby_step_giant_step(g, A, q, p)
    b_private = baby_step_giant_step(g, B, q, p)

    if a_private is None or b_private is None:
        raise ValueError("Could not deduce private keys")

    # Compute shared key
    shared_key = (pow(g, a_private, p) * pow(g, b_private, p)) % p
    return shared_key


p = 9459040338068898689261456459355656735760126665215411768729930709057649580926326656219024573411869732770921533628486688534108189813533765746159096301632668722327  # Prime modulus
g = 5  # Base (generator)
A = 4273882268770451042535779967439697351016686492206027478809543375227950930138924865543470033644860424586440579542980690863469253402996371905611340139885738693080  # Alice's public key
B = 3847640689624364711664886026800290793265399414700736841705321414309213654447740358930872088921683993690069628098925077346749794347163383463395658935649932413838  # Bob's public key


try:
    shared_key = compute_shared_key(p, g, A, B)
    print(f"Computed shared key: {shared_key}")
except Exception as e:
    print(f"Error computing shared key: {e}")
