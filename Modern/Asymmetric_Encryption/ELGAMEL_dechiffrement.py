import tkinter as tk
from tkinter import messagebox

def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

def decrypt(p, x, a, b):
    s = mod_exp(a, x, p)
    s_inv = pow(s, -1, p)
    m = (b * s_inv) % p
    return m

def do_decrypt():
    try:
        p = int(entry_p.get())
        x = int(entry_x.get())
        a = int(entry_a.get())
        b = int(entry_b.get())

        m = decrypt(p, x, a, b)
        messagebox.showinfo("Résultat 💌", f"🔓 Message déchiffré : {m}")
    except Exception as e:
        messagebox.showerror("Erreur ❌", str(e))

# Interface
root = tk.Tk()
root.title("💖 Déchiffrement ElGamal 💖")
root.geometry("400x300")
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
entry_x = add_label_entry("Clé privée x :", 1)
entry_a = add_label_entry("Valeur a :", 2)
entry_b = add_label_entry("Valeur b :", 3)

btn = tk.Button(root, text="🌸 Déchiffrer 🌸", command=do_decrypt,
                bg="#ff99cc", fg="white", activebackground="#ff66b3",
                font=font_button, relief="groove")
btn.grid(row=4, columnspan=2, pady=20)

root.mainloop()
