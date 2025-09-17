import base64
import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

# Simuler une "clé Serpent"
def derive_key(password):
    return SHA256.new(password.encode()).digest() 

def encrypt(plaintext, key):
    plaintext = pad(plaintext)  
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    ciphertext = base64.b64encode(iv + cipher.encrypt(plaintext.encode())).decode()
    return ciphertext

def decrypt(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:]).decode()
    return unpad(plaintext)

def pad(text):
    return text + (AES.block_size - len(text) % AES.block_size) * chr(AES.block_size - len(text) % AES.block_size)

def unpad(text):
    return text[:-ord(text[len(text) - 1:])]

# Interface utilisateur (GUI)
def on_encrypt():
    plaintext = entry_text.get("1.0", tk.END).strip()
    password = entry_key.get().strip()
    if not plaintext or not password:
        messagebox.showerror("Erreur", "Veuillez entrer le texte et la clé.")
        return
    key = derive_key(password)
    encrypted_text = encrypt(plaintext, key)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, encrypted_text)

def on_decrypt():
    ciphertext = entry_text.get("1.0", tk.END).strip()
    password = entry_key.get().strip()
    if not ciphertext or not password:
        messagebox.showerror("Erreur", "Veuillez entrer le texte et la clé.")
        return
    key = derive_key(password)
    decrypted_text = decrypt(ciphertext, key)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, decrypted_text)

# Création de la fenêtre Tkinter
window = tk.Tk()
window.title("Chiffrement et Déchiffrement Serpent Simulé")
window.geometry("500x400")

# Widgets Tkinter
tk.Label(window, text="Texte à chiffrer/déchiffrer :").pack()
entry_text = tk.Text(window, height=5)
entry_text.pack()

tk.Label(window, text="Clé (mot de passe) :").pack()
entry_key = tk.Entry(window, show="*")
entry_key.pack()

tk.Button(window, text="Chiffrer", command=on_encrypt).pack(pady=5)
tk.Button(window, text="Déchiffrer", command=on_decrypt).pack(pady=5)

result_label = tk.Label(window, text="Résultat :")
result_label.pack()
result_text = tk.Text(window, height=5)
result_text.pack()

# Boucle principale Tkinter
window.mainloop()
