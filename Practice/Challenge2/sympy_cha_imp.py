from sympy.ntheory import discrete_log
from sympy.ntheory.modular import crt

# Values for Diffie-Hellman
p = 9459040338068898689261456459355656735760126665215411768729930709057649580926326656219024573411869732770921533628486688534108189813533765746159096301632668722327
r = 5
A = 4273882268770451042535779967439697351016686492206027478809543375227950930138924865543470033644860424586440579542980690863469253402996371905611340139885738693080
B = 3847640689624364711664886026800290793265399414700736841705321414309213654447740358930872088921683993690069628098925077346749794347163383463395658935649932413838

# Manually input the factorization of p-1 as a dictionary
factorization = {
    2: 1,
    5531790401440711: 1,
    7456838241168989: 1,
    8515259982369671: 1,
    8745786245782841: 1,
    9499742089305047: 1,
    9700182083860057: 1,
    10364391344477629: 1,
    11426445140881751: 1,
    11607899603171899: 1,
    12153450212629753: 1,
}


def pohlig_hellman(p, g, A, factorization):
    residues = []
    moduli = []

    for q, e in factorization.items():
        q_power = q**e
        g_q = pow(g, (p - 1) // q_power, p)  # g^((p-1)/q) mod p
        A_q = pow(A, (p - 1) // q_power, p)  # A^((p-1)/q) mod p

        # Solve discrete log for g_q^x = A_q (mod p)
        x_q = discrete_log(p, A_q, g_q, order=q_power)

        residues.append(x_q)
        moduli.append(q_power)

    # Combine results using Chinese Remainder Theorem (CRT)
    x, _ = crt(moduli, residues)
    return x


alpha = pohlig_hellman(p, r, A, factorization)

print(f"Private key 'alpha': {alpha}")

shared_key = pow(B, alpha, p)

print(f"Shared key: {shared_key}")
