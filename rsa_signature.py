import tkinter as tk
from tkinter import ttk, messagebox
import random
from sympy import isprime

# --- Fonctions RSA ---

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 % m0

def generate_keys(bits=12):
    while True:
        p = random.randint(2**(bits-1), 2**bits - 1)
        if isprime(p): break
    while True:
        q = random.randint(2**(bits-1), 2**bits - 1)
        if isprime(q) and q != p: break
    n = p * q
    phi = (p -1) * (q -1)
    e = 3
    while gcd(e, phi) != 1:
        e += 2
    d = modinv(e, phi)
    return e, d, n

def simple_hash(message):
    # Un hash très simple (pas sécurisé, juste pour démo)
    return sum(ord(c) for c in message)

def sign(message, d, n):
    h = simple_hash(message)
    return pow(h, d, n)

# --- Interface Girly ---

root = tk.Tk()
root.title("💖 RSA Signature Girly 💖")
root.geometry("600x400")
root.configure(bg="#ffe6f0")

style = ttk.Style()
style.configure("TButton", font=("Comic Sans MS", 13, "bold"), padding=8)
style.configure("TLabel", font=("Comic Sans MS", 13), background="#ffe6f0")
style.configure("TEntry", font=("Comic Sans MS", 13))

ttk.Label(root, text="Entrez un message à signer :").pack(pady=15)
entry_msg = ttk.Entry(root, width=50)
entry_msg.pack(pady=5)

signature_var = tk.StringVar()
pubkey_var = tk.StringVar()
privkey_var = tk.StringVar()

def on_sign():
    msg = entry_msg.get()
    if not msg:
        messagebox.showerror("Erreur", "Veuillez entrer un message.")
        return
    e, d, n = generate_keys()
    signature = sign(msg, d, n)
    signature_var.set(str(signature))
    pubkey_var.set(f"e = {e}\nn = {n}")
    privkey_var.set(f"d = {d}\nn = {n}")

ttk.Button(root, text="Signer", command=on_sign).pack(pady=15)

ttk.Label(root, text="Signature :").pack(pady=(10, 3))
ttk.Label(root, textvariable=signature_var, foreground="#d6006e", wraplength=550).pack()

ttk.Label(root, text="Clé publique :").pack(pady=(15, 3))
ttk.Label(root, textvariable=pubkey_var, foreground="#9b0056").pack()

ttk.Label(root, text="Clé privée :").pack(pady=(15, 3))
ttk.Label(root, textvariable=privkey_var, foreground="#9b0056").pack()

root.mainloop()
