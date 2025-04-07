import customtkinter as ctk
from tkinter import messagebox
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii

# Fonction pour chiffrer un message avec DES
def encrypt_message(message, key):
    key = key.ljust(8, b'\0')[:8]  # S'assurer que la clé est de 8 octets
    cipher = DES.new(key, DES.MODE_CBC)
    padded_message = pad(message.encode(), DES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return binascii.hexlify(cipher.iv).decode(), binascii.hexlify(encrypted_message).decode()

# Fonction pour déchiffrer un message avec DES
def decrypt_message(encrypted_message, key, iv):
    key = key.ljust(8, b'\0')[:8]
    iv = binascii.unhexlify(iv)
    encrypted_message = binascii.unhexlify(encrypted_message)
    cipher = DES.new(key, DES.MODE_CBC, iv=iv)
    decrypted_message = unpad(cipher.decrypt(encrypted_message), DES.block_size)
    return decrypted_message.decode()

# Fonction bouton pour chiffrer
def chiffrer():
    texte = texte_input.get("0.0", "end").strip()
    cle = cle_input.get().strip()
    if not texte or not cle:
        messagebox.showerror("Erreur", "Le texte et la clé doivent être renseignés.")
        return
    iv, resultat = encrypt_message(texte, cle.encode())
    resultat_output.delete("0.0", "end")
    resultat_output.insert("0.0", f"Texte chiffré (en hex) : {resultat}")
    iv_output.delete("0.0", "end")
    iv_output.insert("0.0", f"Vecteur d'initialisation (IV) : {iv}")
    
    # Ajouter une boîte de dialogue pour afficher l'IV
    messagebox.showinfo("Information sur l'IV", f"Vecteur d'initialisation (IV) : {iv}\n\nVeuillez copier cette valeur pour le déchiffrement.")

# Fonction bouton pour déchiffrer
def dechiffrer():
    texte_hex = texte_input.get("0.0", "end").strip()
    cle = cle_input.get().strip()
    iv = iv_input.get().strip()
    if not texte_hex or not cle or not iv:
        messagebox.showerror("Erreur", "Le texte chiffré, la clé et le vecteur d'initialisation doivent être renseignés.")
        return
    try:
        decrypted_message = decrypt_message(texte_hex, cle.encode(), iv)
        resultat_output.delete("0.0", "end")
        resultat_output.insert("0.0", f"Texte déchiffré : {decrypted_message}")
    except (ValueError, binascii.Error) as e:
        messagebox.showerror("Erreur", f"Erreur lors du déchiffrement: {str(e)}\nVérifiez que le texte est un hexadécimal valide.")

# Apparence et thème
ctk.set_appearance_mode("System")  # "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # blue, green, dark-blue

# Fenêtre principale
app = ctk.CTk()
app.title("🔐 DES - Chiffrement / Déchiffrement")
app.geometry("600x700")  # Augmenté la hauteur pour assurer la visibilité de tous les éléments

# Conteneur principal
frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(padx=20, pady=20, expand=True, fill="both")

# Widgets
label_texte = ctk.CTkLabel(frame, text="Texte ou texte chiffré (hex) :", font=ctk.CTkFont(size=14))
label_texte.pack(pady=(10, 0))
texte_input = ctk.CTkTextbox(frame, height=100)
texte_input.pack(padx=10, pady=10, fill="x")

label_cle = ctk.CTkLabel(frame, text="Clé (8 caractères max) :", font=ctk.CTkFont(size=14))
label_cle.pack()
cle_input = ctk.CTkEntry(frame, show="*", width=300)
cle_input.pack(pady=5)

label_iv = ctk.CTkLabel(frame, text="Vecteur d'initialisation (IV) (pour déchiffrement) :", font=ctk.CTkFont(size=14))
label_iv.pack()
iv_input = ctk.CTkEntry(frame, width=300)
iv_input.pack(pady=5)

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

label_iv_output = ctk.CTkLabel(frame, text="Vecteur d'initialisation (IV) pour le chiffrement :", font=ctk.CTkFont(size=14))
label_iv_output.pack(pady=(10, 0))
iv_output = ctk.CTkTextbox(frame, height=40)
iv_output.pack(padx=10, pady=10, fill="x")

# Lancer l'app
app.mainloop()