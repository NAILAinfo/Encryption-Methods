import socket
import rsa
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode

# 🔐 AES decrypt
def decrypt_aes(cipher_text, key, iv):
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    decrypted = cipher.decrypt(b64decode(cipher_text))
    return unpad(decrypted, AES.block_size).decode()

# 🔐 RSA decrypt
def decrypt_rsa(cipher_text, private_key):
    return rsa.decrypt(b64decode(cipher_text), private_key).decode()

# 🔐 ElGamal decrypt (simplifié)
def decrypt_elgamal(cipher_pair, private_key):
    a, b = map(int, cipher_pair.split(','))
    s = pow(a, private_key, 467)
    plain = (b * pow(s, -1, 467)) % 467
    return chr(plain)

# 📡 Connexion
client = socket.socket()
client.connect(('localhost', 12345))

# 🔑 Clés
with open('client_keys/private.pem', 'rb') as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

print("🔐 Client connecté avec succès au serveur.")

while True:
    print("\n--- NOUVELLE COMMUNICATION ---")

    # 🔸 Choisir l'algorithme
    algo = input("🛡 Méthode (RSA / AES / ElGamal) : ").strip().lower()
    if algo not in ['rsa', 'aes', 'elgamal']:
        print("❌ Méthode non supportée.")
        continue

    message = input("💬 Entrez le message à envoyer : ")
    client.send(algo.encode())
    client.send(message.encode())

    # 🕒 Attente de réponse
    response_flag = client.recv(1024).decode()
    if response_flag == 'no_response':
        print("🔕 Le serveur a choisi de ne pas répondre.")
    else:
        print("📩 Le serveur souhaite répondre. Réception...")

        response = client.recv(4096).decode()
        if algo == 'rsa':
            try:
                decrypted = decrypt_rsa(response, private_key)
                print(f"🔓 Message déchiffré (RSA) : {decrypted}")
            except Exception as e:
                print("❌ Erreur RSA :", e)

        elif algo == 'aes':
            try:
                data = json.loads(response)
                decrypted = decrypt_aes(data['cipher'], data['key'], data['iv'])
                print(f"🔓 Message déchiffré (AES) : {decrypted}")
            except Exception as e:
                print("❌ Erreur AES :", e)

        elif algo == 'elgamal':
            try:
                decrypted = decrypt_elgamal(response, 127)  # 🔐 clé privée ElGamal (à adapter)
                print(f"🔓 Message déchiffré (ElGamal) : {decrypted}")
            except Exception as e:
                print("❌ Erreur ElGamal :", e)

    # 🔁 Recommencer ou quitter
    again = input("\n🔁 Voulez-vous envoyer un autre message ? (o/n) : ").lower()
    client.send(b"yes" if again == 'o' else b"no")
    if again != 'o':
        print("🚪 Fin de la communication.")
        break

client.close()
