import tkinter as tk
from tkinter import messagebox
import random

def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

def generate_keys(p, g):
    x = random.randint(1, p - 2)
    y = mod_exp(g, x, p)
    return (p, g, y), x

def encrypt(p, g, y, m):
    k = random.randint(1, p - 2)
    a = mod_exp(g, k, p)
    b = (m * mod_exp(y, k, p)) % p
    return a, b

def do_encrypt():
    try:
        p = int(entry_p.get())
        g = int(entry_g.get())
        m = int(entry_message.get())

        public_key, private_key = generate_keys(p, g)
        a, b = encrypt(p, g, public_key[2], m)

        result = f"Clé publique: (p={p}, g={g}, y={public_key[2]})\n"
        result += f"Clé privée: x={private_key}\n"
        result += f"Chiffre: a={a}, b={b}"

        with open("chiffre.txt", "a") as f:
           f.write("---- Nouveau chiffrement ----\n")
           f.write(f" nombre premier : {p}, generateur :{g}, cle public: {public_key[2]}, cle prive: {private_key}\n")
           f.write(f" message chiffre :({a}, {b})\n\n")


        messagebox.showinfo("Chiffrement réussi 💖", result + "\n\nDonnées sauvegardées dans 'chiffre.txt'")
    except Exception as e:
        messagebox.showerror("Erreur ❌", str(e))

# Interface stylée
root = tk.Tk()
root.title("💗 Chiffrement ElGamal 💗")
root.geometry("400x280")
root.configure(bg="#ffe6f0")

font_label = ("Comic Sans MS", 10)
font_entry = ("Comic Sans MS", 10)
font_button = ("Comic Sans MS", 11, "bold")

def add_label_entry(text, row):
    label = tk.Label(root, text=text, bg="#ffe6f0", font=font_label)
    label.grid(row=row, column=0, padx=10, pady=5, sticky='w')
    entry = tk.Entry(root, font=font_entry, width=30)
    entry.grid(row=row, column=1, padx=10, pady=5)
    return entry

entry_p = add_label_entry("Nombre premier p :", 0)
entry_g = add_label_entry("Racine primitive g :", 1)
entry_message = add_label_entry("Message (entier) à chiffrer :", 2)

btn = tk.Button(root, text="✨ Chiffrer ✨", command=do_encrypt,
                bg="#ff99cc", fg="white", activebackground="#ff66b3",
                font=font_button, relief="groove")
btn.grid(row=3, columnspan=2, pady=20)

root.mainloop()
