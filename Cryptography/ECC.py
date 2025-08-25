# Nicolas Urrea
# FSUID: NU22C
# Due Date: 07/29/2025
# The program in this file is the individual work of Nicolas Urrea
import math
def modinv(a, p):
    if a == 0:
        return None
    lm, hm = 1, 0
    low, high = a % p, p
    while low > 1:
        r = high // low
        nm, new = hm - lm * r, high - low * r
        lm, low, hm, high = nm, new, lm, low
    return lm % p

def add_points(P, Q, a, p):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0: return None
    if P != Q:
        m = ((y2 - y1) * modinv((x2 - x1) % p, p)) % p
    else:
        m = ((3 * x1 * x1 + a) * modinv((2 * y1) % p, p)) % p
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mult(k, P, a, p):
    result = None
    while k > 0:
        if k & 1:
            result = add_points(result, P, a, p)
        P = add_points(P, P, a, p)
        k >>= 1
    return result

# Input values as described
a = int(input("Enter a: "))
b = int(input("Enter b: "))
p = int(input("Enter p: "))
gx = int(input("Enter generator x: "))
gy = int(input("Enter generator y: "))
G = (gx, gy)

alice_priv = int(input("Enter Alice’s private key: "))
bob_priv = int(input("Enter Bob’s private key: "))

# Compute public keys
alice_pub = scalar_mult(alice_priv, G, a, p)
bob_pub = scalar_mult(bob_priv, G, a, p)

print("Public Keys:")
print("Alice:", alice_pub)
print("Bob:", bob_pub)

# Shared keys
alice_shared = scalar_mult(bob_priv, alice_pub, a, p)
bob_shared = scalar_mult(alice_priv, bob_pub, a, p)

print("Agreed Upon Keys:")
print("Alice:", alice_shared[0] if alice_shared else "Point at infinity")
print("Bob:", bob_shared[0] if bob_shared else "Point at infinity")