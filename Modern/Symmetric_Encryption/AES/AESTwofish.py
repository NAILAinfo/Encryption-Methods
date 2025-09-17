import tkinter as tk
from tkinter import messagebox

def twofish_encrypt(key, plaintext):
    # Cette version simplifiée effectue un chiffrement basique (juste pour illustration).
    ciphertext = "".join([chr((ord(char) + len(key)) % 256) for char in plaintext])
    return ciphertext

def twofish_decrypt(key, ciphertext):
    # Déchiffrement correspondant à la version simplifiée.
    plaintext = "".join([chr((ord(char) - len(key)) % 256) for char in ciphertext])
    return plaintext

# --- Interface Utilisateur avec Tkinter ---
def handle_action():
    action = action_var.get()
    key = key_entry.get()
    text = text_entry.get()

    if not key or not text:
        messagebox.showerror("Erreur", "Veuillez saisir une clé et un texte valide.")
        return

    if action == "Chiffrer":
        result = twofish_encrypt(key, text)
        result_label.config(text=f"Texte chiffré : {result}")
    elif action == "Déchiffrer":
        result = twofish_decrypt(key, text)
        result_label.config(text=f"Texte déchiffré : {result}")
    else:
        messagebox.showerror("Erreur", "Action inconnue.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Chiffrement/Déchiffrement Twofish")
root.geometry("400x300")

# Widgets de l'interface utilisateur
action_var = tk.StringVar(value="Chiffrer")

# Titre
title_label = tk.Label(root, text="Twofish Encryption", font=("Helvetica", 16))
title_label.pack(pady=10)

# Option : Chiffrer ou Déchiffrer
action_frame = tk.Frame(root)
action_frame.pack(pady=5)

encrypt_radio = tk.Radiobutton(action_frame, text="Chiffrer", variable=action_var, value="Chiffrer")
encrypt_radio.pack(side=tk.LEFT, padx=10)

decrypt_radio = tk.Radiobutton(action_frame, text="Déchiffrer", variable=action_var, value="Déchiffrer")
decrypt_radio.pack(side=tk.LEFT, padx=10)

# Saisie de la clé
key_label = tk.Label(root, text="Clé :")
key_label.pack()
key_entry = tk.Entry(root, show="*", width=30)
key_entry.pack(pady=5)

# Saisie du texte
text_label = tk.Label(root, text="Texte :")
text_label.pack()
text_entry = tk.Entry(root, width=30)
text_entry.pack(pady=5)

# Bouton d'action
process_button = tk.Button(root, text="Exécuter", command=handle_action)
process_button.pack(pady=10)

# Résultat
default_result_text = "Résultat affiché ici."
result_label = tk.Label(root, text=default_result_text, wraplength=300, justify="center", font=("Helvetica", 10))
result_label.pack(pady=10)

# Lancer l'application
root.mainloop()
