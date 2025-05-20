import tkinter as tk
from tkinter import messagebox, ttk

def modexp(base, exp, mod):
    return pow(base, exp, mod)

def xor_crypt(message, key):
    return ''.join(chr(ord(c) ^ (key % 256)) for c in message)

def calculate_keys():
    try:
        p = int(entry_p.get())
        g = int(entry_g.get())
        a = int(entry_a.get())
        b = int(entry_b.get())

        A = modexp(g, a, p)
        B = modexp(g, b, p)
        shared_key = modexp(B, a, p)

        entry_A.config(state="normal")
        entry_B.config(state="normal")
        entry_key.config(state="normal")

        entry_A.delete(0, tk.END)
        entry_A.insert(0, str(A))

        entry_B.delete(0, tk.END)
        entry_B.insert(0, str(B))

        entry_key.delete(0, tk.END)
        entry_key.insert(0, str(shared_key))

        entry_A.config(state="readonly")
        entry_B.config(state="readonly")
        entry_key.config(state="readonly")

        messagebox.showinfo("Clé partagée générée", f"Clé secrète : {shared_key}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Entrées invalides : {e}")

def encrypt_message():
    try:
        key = int(entry_key.get())
        message = entry_msg.get()
        encrypted = xor_crypt(message, key)
        entry_encrypted.delete(0, tk.END)
        entry_encrypted.insert(0, encrypted.encode('utf-8').hex())
    except Exception as e:
        messagebox.showerror("Erreur de chiffrement", str(e))

def decrypt_message():
    try:
        key = int(entry_key.get())
        hex_encrypted = entry_encrypted.get()
        encrypted = bytes.fromhex(hex_encrypted).decode('utf-8')
        decrypted = xor_crypt(encrypted, key)
        entry_decrypted.delete(0, tk.END)
        entry_decrypted.insert(0, decrypted)
    except Exception as e:
        messagebox.showerror("Erreur de déchiffrement", str(e))

# Interface girly
root = tk.Tk()
root.title("🌸 Diffie-Hellman - Crypto Girly 🌸")
root.geometry("550x700")
root.configure(bg="#ffe6f0")

style = ttk.Style()
style.configure("TLabel", background="#ffe6f0", foreground="#cc0066", font=("Comic Sans MS", 10, "bold"))
style.configure("TButton", font=("Comic Sans MS", 10, "bold"), background="#ff99cc")
style.configure("TEntry", font=("Comic Sans MS", 10))

title = ttk.Label(root, text="💖 Diffie-Hellman 💖", font=("Comic Sans MS", 16, "bold"))
title.pack(pady=10)

frame_top = ttk.Frame(root)
frame_top.pack(pady=5)

def add_field(label_text, parent, readonly=False):
    label = ttk.Label(parent, text=label_text)
    label.pack()
    entry = ttk.Entry(parent, width=40)
    entry.pack(pady=3)
    if readonly:
        entry.config(state="readonly")
    return entry

# Partie du haut : paramètres publics et clés privées
entry_p = add_field("Nombre premier p :", frame_top)
entry_g = add_field("Base g :", frame_top)
entry_a = add_field("Clé privée Alice (a) :", frame_top)
entry_b = add_field("Clé privée Bob (b) :", frame_top)

# Bouton pour générer les clés
ttk.Button(root, text="🔐 Générer Clés", command=calculate_keys).pack(pady=10)

# Partie du bas : clés publiques et clé partagée
frame_bottom = ttk.Frame(root)
frame_bottom.pack(pady=5)

entry_A = add_field("Clé publique Alice (A) :", frame_bottom, readonly=True)
entry_B = add_field("Clé publique Bob (B) :", frame_bottom, readonly=True)
entry_key = add_field("Clé secrète partagée K :", frame_bottom, readonly=True)

# Chiffrement / Déchiffrement
ttk.Label(root, text="Message à chiffrer :").pack()
entry_msg = ttk.Entry(root, width=50)
entry_msg.pack(pady=3)

ttk.Button(root, text="💌 Chiffrer", command=encrypt_message).pack(pady=5)

ttk.Label(root, text="Message chiffré (hex) :").pack()
entry_encrypted = ttk.Entry(root, width=50)
entry_encrypted.pack(pady=3)

ttk.Button(root, text="💖 Déchiffrer", command=decrypt_message).pack(pady=5)

ttk.Label(root, text="Message déchiffré :").pack()
entry_decrypted = ttk.Entry(root, width=50)
entry_decrypted.pack(pady=3)

root.mainloop()
