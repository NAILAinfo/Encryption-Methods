def caesar_encrypt(text, shift):
    return ''.join(chr((ord(c) - 32 + shift) % 95 + 32) if 32 <= ord(c) <= 126 else c for c in text)

def caesar_decrypt(text, shift):
    return ''.join(chr((ord(c) - 32 - shift) % 95 + 32) if 32 <= ord(c) <= 126 else c for c in text)
