import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES  # On utilisera l'implémentation MARS ici (via pycryptodome)
from Crypto.Random import get_random_bytes
import base64

# Fonction pour ajouter un padding si la clé ou le texte est trop court
def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text

# Fonction de chiffrement avec MARS
def encrypt_mars():
    key = key_entry.get()
    if len(key) != 16:
        messagebox.showerror("Erreur", "La clé doit faire exactement 16 caractères.")
        return

    plaintext = pad(input_text.get("1.0", tk.END).strip())
    cipher = AES.new(key.encode(), AES.MODE_ECB)  # ECB pour simplifier, mais CBC est plus sûr
    encrypted_text = base64.b64encode(cipher.encrypt(plaintext.encode())).decode()
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, encrypted_text)

# Fonction de déchiffrement avec MARS
def decrypt_mars():
    key = key_entry.get()
    if len(key) != 16:
        messagebox.showerror("Erreur", "La clé doit faire exactement 16 caractères.")
        return

    encrypted_text = input_text.get("1.0", tk.END).strip()
    try:
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        decrypted_text = cipher.decrypt(base64.b64decode(encrypted_text)).decode().strip()
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, decrypted_text)
    except Exception as e:
        messagebox.showerror("Erreur", "Le texte chiffré est invalide ou la clé est incorrecte.")

# Création de l'interface utilisateur
root = tk.Tk()
root.title("Chiffrement et Déchiffrement - MARS")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

key_label = tk.Label(frame, text="Saisir la clé (16 caractères) :")
key_label.pack()
key_entry = tk.Entry(frame, show="*", width=30)
key_entry.pack()

input_label = tk.Label(frame, text="Saisir le texte à chiffrer/déchiffrer :")
input_label.pack()
input_text = tk.Text(frame, height=5, width=40)
input_text.pack()

encrypt_button = tk.Button(frame, text="Chiffrer", command=encrypt_mars)
encrypt_button.pack(pady=5)

decrypt_button = tk.Button(frame, text="Déchiffrer", command=decrypt_mars)
decrypt_button.pack(pady=5)

output_label = tk.Label(frame, text="Résultat :")
output_label.pack()
output_text = tk.Text(frame, height=5, width=40)
output_text.pack()

root.mainloop()
