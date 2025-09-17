import tkinter as tk
from tkinter import ttk, messagebox
import random

# === Paramètres de la courbe (courbe simple pour démo) ===
p = 97
a = 2
b = 3
G = (3, 6)

# === Fonctions ECC ===

def is_on_curve(P):
    if P is None:
        return True
    x, y = P
    return (y**2 - (x**3 + a*x + b)) % p == 0

def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        s = (3 * x1**2 + a) * pow(2 * y1, -1, p) % p
    else:
        s = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (s**2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mult(k, P):
    R = None
    while k > 0:
        if k % 2 == 1:
            R = point_add(R, P)
        P = point_add(P, P)
        k //= 2
    return R

def generate_keys():
    d = random.randint(1, p - 1)
    Q = scalar_mult(d, G)
    return d, Q

def encode_char(c):
    x = ord(c)
    for y in range(p):
        if is_on_curve((x, y)):
            return (x, y)
    raise ValueError(f"Impossible d'encoder le caractère '{c}'. Aucun point valide trouvé.")

def decode_point(P):
    if P is None:
        return '?'
    x, _ = P
    try:
        return chr(x)
    except:
        return '?'

def encrypt(Pm, Q):
    k = random.randint(1, p - 1)
    C1 = scalar_mult(k, G)
    kQ = scalar_mult(k, Q)
    C2 = point_add(Pm, kQ)
    return C1, C2

def decrypt(C1, C2, d):
    dC1 = scalar_mult(d, C1)
    inv = (dC1[0], (-dC1[1]) % p)
    return point_add(C2, inv)

# === Interface graphique ===

root = tk.Tk()
root.title("🌸 ECC Crypto Girly 🌸")
root.geometry("600x600")
root.configure(bg="#fff0f5")

style = ttk.Style()
style.configure("TLabel", background="#fff0f5", foreground="#cc3399", font=("Comic Sans MS", 10, "bold"))
style.configure("TButton", font=("Comic Sans MS", 10, "bold"))
style.configure("TEntry", font=("Comic Sans MS", 10))

ttk.Label(root, text="💖 ECC ElGamal - Démo Girly", font=("Comic Sans MS", 16, "bold")).pack(pady=10)

frame = ttk.Frame(root)
frame.pack(pady=10)

# Champs de saisie
ttk.Label(frame, text="Lettre à chiffrer :").grid(row=0, column=0, sticky="w")
entry_msg = ttk.Entry(frame, width=40)
entry_msg.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Point C1 :").grid(row=1, column=0, sticky="w")
entry_c1 = ttk.Entry(frame, width=40)
entry_c1.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Point C2 :").grid(row=2, column=0, sticky="w")
entry_c2 = ttk.Entry(frame, width=40)
entry_c2.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Lettre déchiffrée :").grid(row=3, column=0, sticky="w")
entry_decrypted = ttk.Entry(frame, width=40)
entry_decrypted.grid(row=3, column=1, pady=5)

# Clés globales
private_key = None
public_key = None

def do_generate_keys():
    global private_key, public_key
    private_key, public_key = generate_keys()
    messagebox.showinfo("Clés ECC générées", f"🔐 Clé privée : {private_key}\n🔓 Clé publique : {public_key}")

def do_encrypt():
    msg = entry_msg.get().strip()
    if not msg or len(msg) != 1:
        messagebox.showerror("Erreur", "Saisis UNE seule lettre.")
        return
    if public_key is None:
        messagebox.showwarning("Attention", "Génère les clés d'abord.")
        return
    try:
        Pm = encode_char(msg)
        C1, C2 = encrypt(Pm, public_key)
        entry_c1.delete(0, tk.END)
        entry_c2.delete(0, tk.END)
        entry_c1.insert(0, str(C1))
        entry_c2.insert(0, str(C2))
    except Exception as e:
        messagebox.showerror("Erreur chiffrement", str(e))

def do_decrypt():
    if private_key is None:
        messagebox.showwarning("Attention", "Génère les clés d'abord.")
        return
    try:
        C1 = eval(entry_c1.get())
        C2 = eval(entry_c2.get())
        if not isinstance(C1, tuple) or not isinstance(C2, tuple):
            raise ValueError("Entrée invalide pour C1 ou C2.")
        Pm = decrypt(C1, C2, private_key)
        decoded = decode_point(Pm)
        entry_decrypted.delete(0, tk.END)
        entry_decrypted.insert(0, decoded)
    except Exception as e:
        messagebox.showerror("Erreur déchiffrement", str(e))

# Boutons
ttk.Button(root, text="🔑 Générer les clés", command=do_generate_keys).pack(pady=5)
ttk.Button(root, text="💌 Chiffrer", command=do_encrypt).pack(pady=5)
ttk.Button(root, text="💖 Déchiffrer", command=do_decrypt).pack(pady=5)

root.mainloop()
