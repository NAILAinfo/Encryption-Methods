import tkinter as tk
from tkinter import ttk, messagebox
import random

# --- Utils math ---

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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r = 3
    while r*r <= n:
        if n % r == 0:
            return False
        r += 2
    return True

def generate_large_prime(bits=16):
    while True:
        p = random.randint(2**(bits-1), 2**bits -1)
        if is_prime(p):
            return p

def find_generator(p):
    # Simplifié: on teste g de 2 à p-1, on retourne le premier qui convient
    for g in range(2, p):
        # vérifier que g est générateur : g^((p-1)/2) mod p != 1 (p premier donc groupe cyclique)
        if pow(g, (p-1)//2, p) != 1:
            return g
    return 2  # fallback

def simple_hash(message):
    return sum(ord(c) for c in message) % (10**6)  # modulo pour éviter trop grand

# --- ElGamal Signature ---

def generate_keys(bits=16):
    p = generate_large_prime(bits)
    g = find_generator(p)
    x = random.randint(1, p-2)  # clé privée
    y = pow(g, x, p)            # clé publique
    return p, g, x, y

def sign(message, p, g, x):
    h = simple_hash(message)
    while True:
        k = random.randint(1, p-2)
        if gcd(k, p-1) == 1:
            break
    r = pow(g, k, p)
    k_inv = modinv(k, p-1)
    s = (k_inv * (h - x * r)) % (p - 1)
    return r, s

# --- Interface girly ---

root = tk.Tk()
root.title("💖 ElGamal Signature Girly 💖")
root.geometry("600x450")
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
    p, g, x, y = generate_keys()
    r, s = sign(msg, p, g, x)
    signature_var.set(f"(r, s) = ({r}, {s})")
    pubkey_var.set(f"p = {p}\ng = {g}\ny = {y}")
    privkey_var.set(f"x = {x}")

ttk.Button(root, text="Signer", command=on_sign).pack(pady=15)

ttk.Label(root, text="Signature :").pack(pady=(10, 3))
ttk.Label(root, textvariable=signature_var, foreground="#d6006e", wraplength=550).pack()

ttk.Label(root, text="Clé publique :").pack(pady=(15, 3))
ttk.Label(root, textvariable=pubkey_var, foreground="#9b0056").pack()

ttk.Label(root, text="Clé privée :").pack(pady=(15, 3))
ttk.Label(root, textvariable=privkey_var, foreground="#9b0056").pack()

root.mainloop()
