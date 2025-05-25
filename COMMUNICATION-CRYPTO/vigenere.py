def vigenere_encrypt(text, key):
    key = key * (len(text) // len(key)) + key[:len(text) % len(key)]
    return ''.join(chr((ord(t) + ord(k)) % 256) for t, k in zip(text, key))

def vigenere_decrypt(text, key):
    key = key * (len(text) // len(key)) + key[:len(text) % len(key)]
    return ''.join(chr((ord(t) - ord(k)) % 256) for t, k in zip(text, key))
