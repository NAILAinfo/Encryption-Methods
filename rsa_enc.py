import tkinter as tk
from tkinter import ttk, messagebox
import random
from sympy import isprime

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

def generate_keys(bits=8):
    while True:
        p = random.randint(2**(bits-1), 2**bits - 1)
        if isprime(p): break
    while True:
        q = random.randint(2**(bits-1), 2**bits - 1)
        if isprime(q) and q != p: break
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while gcd(e, phi) != 1:
        e += 2
    d = modinv(e, phi)
    return e, d, n

def encrypt(message, e, n):
    return [pow(ord(char), e, n) for char in message]

root = tk.Tk()
root.title("🔐 RSA Encryption")
root.geometry("700x400")
root.configure(bg="#f0f4f7")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("TLabel", font=("Segoe UI", 11), background="#f0f4f7")
style.configure("TEntry", font=("Segoe UI", 11))

ttk.Label(root, text="Enter message to encrypt:").pack(pady=10)
entry_msg = ttk.Entry(root, width=50)
entry_msg.pack(pady=5)

def on_encrypt():
    msg = entry_msg.get()
    if not msg:
        messagebox.showerror("Error", "Please enter a message.")
        return
    e, d, n = generate_keys()
    c = encrypt(msg, e, n)
    encrypted_var.set(str(c))
    pubkey_var.set(f"e = {e}\nn = {n}")
    privkey_var.set(f"d = {d}\nn = {n}")

ttk.Button(root, text="Encrypt", command=on_encrypt).pack(pady=15)

ttk.Label(root, text="Encrypted Message:").pack(pady=(10,3))
encrypted_var = tk.StringVar()
ttk.Label(root, textvariable=encrypted_var, wraplength=600, foreground="green").pack()

ttk.Label(root, text="Public Key:").pack(pady=(15, 3))
pubkey_var = tk.StringVar()
ttk.Label(root, textvariable=pubkey_var, foreground="#0052cc").pack()

ttk.Label(root, text="Private Key:").pack(pady=(15, 3))
privkey_var = tk.StringVar()
ttk.Label(root, textvariable=privkey_var, foreground="#cc0000").pack()

root.mainloop()
