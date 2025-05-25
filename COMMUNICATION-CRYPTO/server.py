# Voici la version corrigee du server.py avec boucle question-reponse
import socket
import json
from base64 import b64encode
from rsa_cipher import rsa_decrypt, compute_private_key, rsa_encrypt
from aes_cipher import aes_decrypt, aes_encrypt
from elgamal_cipher import elgamal_decrypt, elgamal_encrypt

HOST = '127.0.0.1'
PORT = 9999

def serialize_key(key):
    return json.dumps(key)

def deserialize_key(key_str):
    try:
        return tuple(map(int, json.loads(key_str)))
    except:
        return json.loads(key_str)

def handle_encryption(method, message, client_key):
    if method == 'rsa':
        return json.dumps(rsa_encrypt(message, client_key))
    elif method == 'aes':
        return aes_encrypt(message, client_key['aes_key'])
    elif method == 'elgamal':
        p, g, y = client_key['p'], client_key['g'], client_key['y']
        return json.dumps(elgamal_encrypt(message, (p, g, y)))

def handle_decryption(method, encrypted_str, priv_key, aes_key=None):
    if method == 'rsa':
        return rsa_decrypt(json.loads(encrypted_str), priv_key)
    elif method == 'aes':
        return aes_decrypt(encrypted_str, aes_key)
    elif method == 'elgamal':
        return elgamal_decrypt(json.loads(encrypted_str), priv_key)

def main():
    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Serveur en ecoute sur {HOST}:{PORT}")

    conn, addr = server.accept()
    print(f"Connexion de {addr}")

    while True:
        method_bytes = conn.recv(1024)
        if not method_bytes:
            print("Fin de connexion.")
            break
        method = method_bytes.decode().lower()
        print(f"\n[MESSAGE RECU] Methode: {method}")

        # Envoi de la cle publique du serveur
        if method == 'rsa':
            n = int(input("Entrez votre n : "))
            e = int(input("Entrez votre e : "))
            p, q = map(int, input("Entrez p et q : ").split())
            pub_key = (n, e)
            priv_key = compute_private_key(n, e, p, q)
            conn.send(serialize_key(pub_key).encode())
        elif method == 'aes':
            raw_key = input("Entrez la cle AES (16 caracteres) : ")
            while len(raw_key) != 16:
                raw_key = input("Reessayer : ")
            aes_key = b64encode(raw_key.encode()).decode()
            pub_key = {'aes_key': aes_key}
            conn.send(json.dumps(pub_key).encode())
        elif method == 'elgamal':
            p = int(input("Entrez p : "))
            x = int(input("Entrez votre cle privee x : "))
            g = 2
            y = pow(g, x, p)
            priv_key = (p, x)
            pub_key = {'p': p, 'g': g, 'y': y}
            conn.send(json.dumps(pub_key).encode())

        # Reception message chiffre
        encrypted_bytes = conn.recv(8192)
        encrypted_str = encrypted_bytes.decode()
        print("Message chiffre recu:", encrypted_str)

        try:
            if method == 'aes':
                message = handle_decryption(method, encrypted_str, None, aes_key)
            else:
                message = handle_decryption(method, encrypted_str, priv_key)
            print("\n✅ Message dechiffre:", message)
        except Exception as e:
            print("❌ Erreur de dechiffrement:", e)
            conn.send(b"no_response")
            continue

        # Choix de repondre ou non
        reply = input("\nSouhaitez-vous repondre ? (o/n) : ").lower()
        if reply != 'o':
            conn.send(b"no_response")
        else:
            conn.send(b"response")
            # Methode de reponse
            method = input("Choisissez methode de reponse (rsa/aes/elgamal) : ").lower()
            conn.send(method.encode())

            print("Attente de la cle publique du client...")
            client_key_bytes = conn.recv(4096)
            client_key = deserialize_key(client_key_bytes.decode())

            response = input("Entrez votre message : ")
            encrypted_response = handle_encryption(method, response, client_key)
            conn.send(encrypted_response.encode())

        # Verifier si client veut continuer
        try:
            again = conn.recv(1024).decode()
            if again != 'yes':
                print("Fin de session par le client.")
                break
        except:
            break

    conn.close()
    server.close()

if __name__ == "__main__":
    main()
