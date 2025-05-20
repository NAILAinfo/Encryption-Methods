import customtkinter as ctk

def diffie_hellman(p, g, a, b):
    A = pow(g, a, p)
    B = pow(g, b, p)
    key = pow(B, a, p)
    return key

def xor_decrypt(encrypted_bytes, key):
    key_bytes = key.to_bytes((key.bit_length() + 7) // 8, byteorder='big')
    return ''.join([chr(b ^ key_bytes[i % len(key_bytes)]) for i, b in enumerate(encrypted_bytes)])

class DechiffrementInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Déchiffrement - Diffie-Hellman")
        self.geometry("700x400")
        ctk.set_appearance_mode("dark")

        self.label = ctk.CTkLabel(self, text="Collez le message chiffré (hexadécimal) :", font=("Arial", 16))
        self.label.pack(pady=10)

        self.input_entry = ctk.CTkEntry(self, width=500, height=40, font=("Arial", 14))
        self.input_entry.pack(pady=10)

        self.button = ctk.CTkButton(self, text="Déchiffrer", command=self.dechiffrer_message)
        self.button.pack(pady=20)

        self.output_label = ctk.CTkLabel(self, text="", font=("Arial", 14), wraplength=600)
        self.output_label.pack(pady=10)

        self.copy_button = ctk.CTkButton(self, text="📋 Copier", command=self.copier_resultat, state="disabled")
        self.copy_button.pack(pady=10)

        self.message_dechiffre = ""

    def dechiffrer_message(self):
        encrypted_hex = self.input_entry.get()
        if not encrypted_hex:
            self.output_label.configure(text="❌ Veuillez entrer un message chiffré.")
            self.copy_button.configure(state="disabled")
            return

        try:
            encrypted_bytes = bytes.fromhex(encrypted_hex)
        except ValueError:
            self.output_label.configure(text="❌ Format hexadécimal invalide.")
            self.copy_button.configure(state="disabled")
            return

        p, g, a, b = 23, 5, 6, 15
        key = diffie_hellman(p, g, a, b)
        self.message_dechiffre = xor_decrypt(encrypted_bytes, key)

        self.output_label.configure(text=f"🔓 Message déchiffré :\n{self.message_dechiffre}")
        self.copy_button.configure(state="normal")

    def copier_resultat(self):
        self.clipboard_clear()
        self.clipboard_append(self.message_dechiffre)
        self.output_label.configure(text=f"✅ Copié dans le presse-papiers :\n{self.message_dechiffre}")

if __name__ == "__main__":
    app = DechiffrementInterface()
    app.mainloop()
