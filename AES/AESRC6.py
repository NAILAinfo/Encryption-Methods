import tkinter as tk
from tkinter import messagebox
import base64
from Crypto.Cipher import ARC4  # RC4 utilisé temporairement pour simuler (RC6 vrai non disponible)
from Crypto.Random import get_random_bytes

# Fonction de chiffrement RC6 (simulé avec RC4)
def encrypt_rc6(key, plaintext):
    cipher = ARC4.new(key.encode('utf-8'))  # Simule avec RC4 faute de librairie RC6
    encrypted_bytes = cipher.encrypt(plaintext.encode('utf-8'))
    encrypted_text = base64.b64encode(encrypted_bytes).decode('utf-8')
    return encrypted_text

# Fonction de déchiffrement RC6 (simulé avec RC4)
def decrypt_rc6(key, ciphertext):
    try:
        cipher = ARC4.new(key.encode('utf-8'))  # Simule avec RC4 faute de librairie RC6
        decrypted_bytes = cipher.decrypt(base64.b64decode(ciphertext))
        decrypted_text = decrypted_bytes.decode('utf-8')
        return decrypted_text
    except Exception as e:
        return f"Erreur de déchiffrement : {str(e)}"

# Fonction à exécuter lors du clic sur le bouton Chiffrer/Déchiffrer
def perform_action():
    action = action_var.get()
    key = entry_key.get()
    text = entry_text.get()

    if not key or not text:
        messagebox.showwarning("Erreur", "La clé et le texte doivent être renseignés.")
        return

    if len(key) < 5:  # Pour éviter un chiffrement faible
        messagebox.showwarning("Erreur", "La clé doit comporter au moins 5 caractères.")
        return

    if action == "Chiffrer":
        result = encrypt_rc6(key, text)
    else:
        result = decrypt_rc6(key, text)

    entry_result.delete(0, tk.END)
    entry_result.insert(0, result)

# Interface graphique avec Tkinter
root = tk.Tk()
root.title("Chiffrement et Déchiffrement RC6 (Simulé)")

# Sélecteur de mode
action_var = tk.StringVar(value="Chiffrer")
frame_mode = tk.Frame(root)
tk.Radiobutton(frame_mode, text="Chiffrer", variable=action_var, value="Chiffrer").pack(side=tk.LEFT)
tk.Radiobutton(frame_mode, text="Déchiffrer", variable=action_var, value="Déchiffrer").pack(side=tk.LEFT)
frame_mode.pack(pady=10)

# Entrée pour la clé
tk.Label(root, text="Clé :").pack()
entry_key = tk.Entry(root, show="*")
entry_key.pack(padx=10, pady=5)

# Entrée pour le texte à chiffrer/déchiffrer
tk.Label(root, text="Texte à chiffrer/déchiffrer :").pack()
entry_text = tk.Entry(root, width=40)
entry_text.pack(padx=10, pady=5)

# Champ pour afficher le résultat
tk.Label(root, text="Résultat :").pack()
entry_result = tk.Entry(root, width=40)
entry_result.pack(padx=10, pady=5)

# Bouton pour exécuter l'action
btn_execute = tk.Button(root, text="Exécuter", command=perform_action)
btn_execute.pack(pady=10)

# Boucle principale de l'interface
root.mainloop()
