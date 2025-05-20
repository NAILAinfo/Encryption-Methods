import customtkinter as ctk

def diffie_hellman(p, g, a, b):
    A = pow(g, a, p)
    B = pow(g, b, p)
    key = pow(B, a, p)
    return key

def xor_encrypt(message, key):
    key_bytes = key.to_bytes((key.bit_length() + 7) // 8, byteorder='big')
    return bytes([ord(c) ^ key_bytes[i % len(key_bytes)] for i, c in enumerate(message)])

class ChiffrementInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chiffrement - Diffie-Hellman")
        self.geometry("700x400")
        ctk.set_appearance_mode("dark")

        self.label = ctk.CTkLabel(self, text="Entrez le message à chiffrer :", font=("Arial", 16))
        self.label.pack(pady=10)

        self.message_entry = ctk.CTkEntry(self, width=500, height=40, font=("Arial", 14))
        self.message_entry.pack(pady=10)

        self.button = ctk.CTkButton(self, text="Chiffrer", command=self.chiffrer_message)
        self.button.pack(pady=20)

        self.output_label = ctk.CTkLabel(self, text="", font=("Arial", 14), wraplength=600)
        self.output_label.pack(pady=10)

        self.copy_button = ctk.CTkButton(self, text="📋 Copier", command=self.copier_resultat, state="disabled")
        self.copy_button.pack(pady=10)

        self.message_chiffre = ""  # Pour stocker le résultat à copier

    def chiffrer_message(self):
        message = self.message_entry.get()
        if not message:
            self.output_label.configure(text="❌ Veuillez entrer un message.")
            self.copy_button.configure(state="disabled")
            return

        p, g, a, b = 23, 5, 6, 15
        key = diffie_hellman(p, g, a, b)
        encrypted = xor_encrypt(message, key)

        self.message_chiffre = encrypted.hex()
        self.output_label.configure(text=f"🔐 Message chiffré (hex) :\n{self.message_chiffre}")
        self.copy_button.configure(state="normal")

    def copier_resultat(self):
        self.clipboard_clear()
        self.clipboard_append(self.message_chiffre)
        self.output_label.configure(text=f"✅ Copié dans le presse-papiers :\n{self.message_chiffre}")

if __name__ == "__main__":
    app = ChiffrementInterface()
    app.mainloop()
