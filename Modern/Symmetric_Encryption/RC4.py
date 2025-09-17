import customtkinter as ctk
from tkinter import messagebox

# RC4 - KSA
def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

# RC4 - PRGA
def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

# RC4 - Main
def RC4(key, data):
    key = [ord(c) for c in key]
    S = KSA(key)
    keystream = PRGA(S)
    return bytearray([b ^ next(keystream) for b in data])

# Fonctions bouton
def chiffrer():
    texte = texte_input.get("0.0", "end").strip()
    cle = cle_input.get().strip()
    if not texte or not cle:
        messagebox.showerror("Erreur", "Le texte et la clé doivent être renseignés.")
        return
    resultat = RC4(cle, texte.encode())
    resultat_output.delete("0.0", "end")
    resultat_output.insert("0.0", resultat.hex())

def dechiffrer():
    texte_hex = texte_input.get("0.0", "end").strip()
    cle = cle_input.get().strip()
    if not texte_hex or not cle:
        messagebox.showerror("Erreur", "Le texte chiffré et la clé doivent être renseignés.")
        return
    try:
        data = bytes.fromhex(texte_hex)
        resultat = RC4(cle, data)
        resultat_output.delete("0.0", "end")
        resultat_output.insert("0.0", resultat.decode(errors="replace"))
    except ValueError:
        messagebox.showerror("Erreur", "Le texte entré n'est pas un hexadécimal valide.")

# Apparence et thème
ctk.set_appearance_mode("System")  # "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # blue, green, dark-blue

# Fenêtre principale
app = ctk.CTk()
app.title("🔐 RC4 - Chiffrement / Déchiffrement")
app.geometry("600x600")

# Conteneur principal
frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(padx=20, pady=20, expand=True, fill="both")

# Widgets
label_texte = ctk.CTkLabel(frame, text="Texte ou texte chiffré (hex) :", font=ctk.CTkFont(size=14))
label_texte.pack(pady=(10, 0))
texte_input = ctk.CTkTextbox(frame, height=100)
texte_input.pack(padx=10, pady=10, fill="x")

label_cle = ctk.CTkLabel(frame, text="Clé :", font=ctk.CTkFont(size=14))
label_cle.pack()
cle_input = ctk.CTkEntry(frame, show="*", width=300)
cle_input.pack(pady=5)

btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
btn_frame.pack(pady=15)
chiff_btn = ctk.CTkButton(btn_frame, text="🔒 Chiffrer", command=chiffrer)
chiff_btn.pack(side="left", padx=10)
dechiff_btn = ctk.CTkButton(btn_frame, text="🔓 Déchiffrer", command=dechiffrer)
dechiff_btn.pack(side="left", padx=10)

label_resultat = ctk.CTkLabel(frame, text="Résultat :", font=ctk.CTkFont(size=14))
label_resultat.pack(pady=(10, 0))
resultat_output = ctk.CTkTextbox(frame, height=100)
resultat_output.pack(padx=10, pady=10, fill="x")

# Lancer l'app
app.mainloop()
