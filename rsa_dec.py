import tkinter as tk
from tkinter import ttk, messagebox

def decrypt(cipher, d, n):
    return ''.join([chr(pow(int(char), d, n)) for char in cipher])

root = tk.Tk()
root.title("🔓 RSA Decryption")
root.geometry("700x400")
root.configure(bg="#f0f4f7")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("TLabel", font=("Segoe UI", 11), background="#f0f4f7")
style.configure("TEntry", font=("Segoe UI", 11))

ttk.Label(root, text="Enter cipher (e.g. [123, 456]):").pack(pady=10)
entry_cipher = ttk.Entry(root, width=60)
entry_cipher.pack(pady=5)

ttk.Label(root, text="Enter private key d:").pack(pady=10)
entry_d = ttk.Entry(root, width=50)
entry_d.pack(pady=5)

ttk.Label(root, text="Enter modulus n:").pack(pady=10)
entry_n = ttk.Entry(root, width=50)
entry_n.pack(pady=5)

decrypted_var = tk.StringVar()

def on_decrypt():
    try:
        cipher = eval(entry_cipher.get())
        d = int(entry_d.get())
        n = int(entry_n.get())
        result = decrypt(cipher, d, n)
        decrypted_var.set("Decrypted: " + result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

ttk.Button(root, text="Decrypt", command=on_decrypt).pack(pady=20)
ttk.Label(root, textvariable=decrypted_var, foreground="#cc0000", wraplength=600).pack(pady=10)

root.mainloop()
