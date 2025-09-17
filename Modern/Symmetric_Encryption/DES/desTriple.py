import customtkinter as ctk
from tkinter import messagebox
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os
import binascii

# Fonction utilitaire pour préparer une clé (exactement 8 octets)
def prepare_key(key_str):
    return key_str.encode().ljust(8, b'\0')[:8]

# Chiffrement Multi-key DES (3 sous-clés)
def encrypt_multi_des(message, key1, key2, key3):
    key1, key2, key3 = prepare_key(key1), prepare_key(key2), prepare_key(key3)
    iv = os.urandom(8)

    cipher1 = DES.new(key1, DES.MODE_CBC, iv)
    step1 = cipher1.encrypt(pad(message.encode(), DES.block_size))

    cipher2 = DES.new(key2, DES.MODE_CBC, iv)
    step2 = cipher2.decrypt(step1)

    cipher3 = DES.new(key3, DES.MODE_CBC, iv)
    encrypted = cipher3.encrypt(step2)

    return binascii.hexlify(iv).decode(), binascii.hexlify(encrypted).decode()

# Déchiffrement Multi-key DES (3 sous-clés)
def decrypt_multi_des(encrypted_hex, key1, key2, key3, iv_hex):
    key1, key2, key3 = prepare_key(key1), prepare_key(key2), prepare_key(key3)
    iv = binascii.unhexlify(iv_hex)
    encrypted = binascii.unhexlify(encrypted_hex)

    cipher3 = DES.new(key3, DES.MODE_CBC, iv)
    step1 = cipher3.decrypt(encrypted)

    cipher2 = DES.new(key2, DES.MODE_CBC, iv)
    step2 = cipher2.encrypt(step1)

    cipher1 = DES.new(key1, DES.MODE_CBC, iv)
    decrypted = unpad(cipher1.decrypt(step2), DES.block_size)

    return decrypted.decode()

def chiffrer():
    texte = texte_input.get("0.0", "end").strip()
    k1, k2, k3 = key1_input.get().strip(), key2_input.get().strip(), key3_input.get().strip()
    if not texte or not k1 or not k2 or not k3:
        messagebox.showerror("Erreur", "Le texte et les trois clés doivent être renseignés.")
        return

    try:
        iv, result = encrypt_multi_des(texte, k1, k2, k3)
        resultat_output.delete("0.0", "end")
        resultat_output.insert("0.0", f"{result}")
        iv_output.delete("0.0", "end")
        iv_output.insert("0.0", iv)
        messagebox.showinfo("Information", f"IV à conserver pour le déchiffrement : {iv}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def dechiffrer():
    texte = texte_input.get("0.0", "end").strip()
    k1, k2, k3 = key1_input.get().strip(), key2_input.get().strip(), key3_input.get().strip()
    iv = iv_input.get().strip()
    if not texte or not k1 or not k2 or not k3 or not iv:
        messagebox.showerror("Erreur", "Texte, IV et les trois clés doivent être renseignés.")
        return

    try:
        decrypted = decrypt_multi_des(texte, k1, k2, k3, iv)
        resultat_output.delete("0.0", "end")
        resultat_output.insert("0.0", f"{decrypted}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# Configuration de l’interface
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🔐 Multi-Key DES - Chiffrement / Déchiffrement")
app.geometry("650x800")

frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(padx=20, pady=20, expand=True, fill="both")

# Widgets
widgets = [
    ("Texte clair ou chiffré (hex) :", "texte_input", "CTkTextbox", {"height": 100}),
    ("Clé 1 (8 caractères max) :", "key1_input", "CTkEntry", {"width": 300}),
    ("Clé 2 (8 caractères max) :", "key2_input", "CTkEntry", {"width": 300}),
    ("Clé 3 (8 caractères max) :", "key3_input", "CTkEntry", {"width": 300}),
    ("Vecteur d'initialisation (IV) :", "iv_input", "CTkEntry", {"width": 300}),
]

for text, var_name, widget_type, kwargs in widgets:
    label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=14))
    label.pack(pady=(10, 0))
    widget = getattr(ctk, widget_type)(frame, **kwargs)
    widget.pack(pady=5)
    globals()[var_name] = widget

# Boutons
btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
btn_frame.pack(pady=15)
chiff_btn = ctk.CTkButton(btn_frame, text="🔒 Chiffrer", command=chiffrer)
chiff_btn.pack(side="left", padx=10)
dechiff_btn = ctk.CTkButton(btn_frame, text="🔓 Déchiffrer", command=dechiffrer)
dechiff_btn.pack(side="left", padx=10)

# Résultats
result_widgets = [
    ("Résultat (hex) :", "resultat_output", {"height": 100}),
    ("IV généré :", "iv_output", {"height": 40}),
]

for text, var_name, kwargs in result_widgets:
    label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=14))
    label.pack(pady=(10, 0))
    widget = ctk.CTkTextbox(frame, **kwargs)
    widget.pack(padx=10, pady=10, fill="x")
    globals()[var_name] = widget

app.mainloop()
