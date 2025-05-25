from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Inverse modulaire inexistant')
    else:
        return x % m

def compute_private_key(n, e, p, q):
    phi = (p-1)*(q-1)
    d = modinv(e, phi)
    return (n, d)

def generate_keys():
    key = RSA.generate(2048)
    private = key.export_key()
    public = key.publickey().export_key()
    return private, public

def rsa_encrypt(message: str, pub_key: tuple[int, int]) -> list[int]:
    n, e = pub_key
    encrypted = []
    for char in message:
        m = ord(char)          # convertir caractère en entier
        c = pow(m, e, n)       # chiffrement RSA : c = m^e mod n
        encrypted.append(c)
    return encrypted

def rsa_decrypt(ciphertext: list[int], priv_key: tuple[int, int]) -> str:
    n, d = priv_key
    decrypted = ''
    for c in ciphertext:
        m = pow(c, d, n)       # déchiffrement RSA : m = c^d mod n
        decrypted += chr(m)
    return decrypted

# Hypothèse dans rsa_cipher.py
def compute_private_key(n, e, p, q):
    # Calcule d = e^(-1) mod phi(n)
    # phi(n) = (p-1)*(q-1)
    phi = (p-1)*(q-1)
    d = modinv(e, phi)  # modinv est la fonction d'inverse modulaire
    return (n, d)
