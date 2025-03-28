import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES
import base64

# Fonction pour ajuster la clé à la longueur correcte
def ajuster_cle(cle):
    return cle.ljust(32)[:32]  # Remplit ou tronque à 32 caractères (256 bits)

# Fonction de chiffrement AES
def chiffrer():
    texte = entree_texte.get("1.0", tk.END).strip()
    cle = entree_cle.get().strip()
    
    if not texte or not cle:
        messagebox.showwarning("Avertissement", "Veuillez saisir le texte et la clé.")
        return

    cle = ajuster_cle(cle)
    cipher = AES.new(cle.encode('utf-8'), AES.MODE_ECB)
    texte_chiffre = cipher.encrypt(texte.encode('utf-8').ljust(32))
    texte_chiffre_base64 = base64.b64encode(texte_chiffre).decode('utf-8')

    sortie_texte.config(state=tk.NORMAL)
    sortie_texte.delete("1.0", tk.END)
    sortie_texte.insert(tk.END, texte_chiffre_base64)
    sortie_texte.config(state=tk.DISABLED)

# Fonction de déchiffrement AES
def dechiffrer():
    texte_chiffre_base64 = entree_texte.get("1.0", tk.END).strip()
    cle = entree_cle.get().strip()
    
    if not texte_chiffre_base64 or not cle:
        messagebox.showwarning("Avertissement", "Veuillez saisir le texte chiffré et la clé.")
        return

    cle = ajuster_cle(cle)
    cipher = AES.new(cle.encode('utf-8'), AES.MODE_ECB)
    texte_chiffre = base64.b64decode(texte_chiffre_base64)
    texte_dechiffre = cipher.decrypt(texte_chiffre).decode('utf-8').strip()

    sortie_texte.config(state=tk.NORMAL)
    sortie_texte.delete("1.0", tk.END)
    sortie_texte.insert(tk.END, texte_dechiffre)
    sortie_texte.config(state=tk.DISABLED)

# Création de l'interface utilisateur
fenetre = tk.Tk()
fenetre.title("AES (Rijndael) - Chiffrement et Déchiffrement")

# Zone de saisie du texte à chiffrer/déchiffrer
label_texte = tk.Label(fenetre, text="Texte à chiffrer ou déchiffrer :")
label_texte.pack()
entree_texte = tk.Text(fenetre, height=5, width=50)
entree_texte.pack()

# Saisie de la clé
label_cle = tk.Label(fenetre, text="Clé AES (16, 24 ou 32 caractères) :")
label_cle.pack()
entree_cle = tk.Entry(fenetre, width=40)
entree_cle.pack()

# Boutons de chiffrement et de déchiffrement
bouton_chiffrer = tk.Button(fenetre, text="Chiffrer", command=chiffrer)
bouton_chiffrer.pack(pady=5)
bouton_dechiffrer = tk.Button(fenetre, text="Déchiffrer", command=dechiffrer)
bouton_dechiffrer.pack(pady=5)

# Zone de sortie du résultat
label_sortie = tk.Label(fenetre, text="Résultat :")
label_sortie.pack()
sortie_texte = tk.Text(fenetre, height=5, width=50, state=tk.DISABLED)
sortie_texte.pack()

# Boucle principale Tkinter
fenetre.mainloop()
