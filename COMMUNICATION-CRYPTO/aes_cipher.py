from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import json

def generate_aes_key():
    key = get_random_bytes(16)
    return base64.b64encode(key).decode()

def aes_encrypt(message, key_base64):
    key = base64.b64decode(key_base64)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    result = {
        'nonce': base64.b64encode(cipher.nonce).decode(),
        'ciphertext': base64.b64encode(ciphertext).decode(),
        'tag': base64.b64encode(tag).decode()
    }
    return json.dumps(result)

def aes_decrypt(encrypted_json, key_base64):
    data = json.loads(encrypted_json)
    key = base64.b64decode(key_base64)
    nonce = base64.b64decode(data['nonce'])
    ciphertext = base64.b64decode(data['ciphertext'])
    tag = base64.b64decode(data['tag'])
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode()