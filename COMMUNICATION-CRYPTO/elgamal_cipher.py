import random

# Calcul de l'inverse modulaire (Extended Euclidean Algorithm)
def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Exponentiation rapide modulaire
def modexp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

# Génération des clés ElGamal (p, g, x) → privé, y → public
def elgamal_generate_keys():
    # Petit p pour la simplicité en démo. En vrai, utiliser des grands nombres sûrs
    p = 467  # nombre premier
    g = 2    # générateur
    x = random.randint(2, p-2)        # clé privée
    y = modexp(g, x, p)               # y = g^x mod p (clé publique)
    public_key = (p, g, y)
    private_key = (p, x)
    return public_key, private_key

# Chiffrement ElGamal
def elgamal_encrypt(message: str, public_key: tuple) -> list:
    p, g, y = public_key
    encrypted = []
    for char in message:
        m = ord(char)
        k = random.randint(2, p-2)
        a = modexp(g, k, p)
        b = (m * modexp(y, k, p)) % p
        encrypted.append((a, b))
    return encrypted  # liste de tuples (a, b)

# Déchiffrement ElGamal
def elgamal_decrypt(ciphertext: list, private_key: tuple) -> str:
    p, x = private_key
    decrypted = ''
    for a, b in ciphertext:
        s = modexp(a, x, p)
        m = (b * modinv(s, p)) % p
        decrypted += chr(m)
    return decrypted