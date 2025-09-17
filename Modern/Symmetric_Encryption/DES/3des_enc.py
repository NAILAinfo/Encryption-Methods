import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import os
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64

class TripleDESEncryptor:
    def __init__(self, root):
        self.root = root
        self.root.title("Chiffrement Triple DES")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.key_var = ctk.StringVar()
        self.input_text = ctk.StringVar()
        self.output_text = ctk.StringVar()
        self.mode_var = ctk.StringVar(value="ECB")  # Mode par défaut
        
        # Style
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=('Arial', 10))
        
        # Frame principal
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        # Section clé
        key_frame = ctk.CTkFrame(main_frame)
        key_frame.pack(fill=ctk.X, pady=10)
        
        ctk.CTkLabel(key_frame, text="Clé Triple DES (24 caractères ou laisser vide pour générer):").pack(side=ctk.LEFT)
        key_entry = ctk.CTkEntry(key_frame, textvariable=self.key_var, width=30)
        key_entry.pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(key_frame, text="Générer", command=self.generate_key).pack(side=ctk.LEFT)
        
        # Section mode de chiffrement
        mode_frame = ctk.CTkFrame(main_frame)
        mode_frame.pack(fill=ctk.X, pady=5)
        
        ctk.CTkLabel(mode_frame, text="Mode:").pack(side=ctk.LEFT)
        modes = ["ECB", "CBC"]
        mode_combo = ctk.CTkComboBox(mode_frame, variable=self.mode_var, values=modes, state="readonly", width=5)
        mode_combo.pack(side=ctk.LEFT, padx=5)
        
        # Section texte d'entrée
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill=ctk.BOTH, expand=True, pady=10)

        ctk.CTkLabel(input_frame, text="Texte à chiffrer").pack(side=ctk.TOP)
        self.input_area = ctk.CTkTextbox(input_frame, height=8, width=40, wrap=ctk.WORD)
        self.input_area.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)
        
        # Section boutons
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill=ctk.X, pady=10)
        
        ctk.CTkButton(buttons_frame, text="Chiffrer", command=self.encrypt).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(buttons_frame, text="Effacer", command=self.clear).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(buttons_frame, text="Sauvegarder clé", command=self.save_key).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(buttons_frame, text="Sauvegarder texte chiffré", command=self.save_ciphertext).pack(side=ctk.LEFT, padx=5)
        
        # Section texte de sortie
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(fill=ctk.BOTH, expand=True, pady=10)

        ctk.CTkLabel(output_frame, text="Texte chiffré").pack(side=ctk.TOP)
        self.output_area = ctk.CTkTextbox(output_frame, height=8, width=40, wrap=ctk.WORD)
        self.output_area.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

    def generate_key(self):
        # Génère une clé valide pour Triple DES (24 octets)
        key = DES3.adjust_key_parity(get_random_bytes(24))
        # Convertit en base64 pour l'affichage
        key_str = base64.b64encode(key).decode('utf-8')
        self.key_var.set(key_str)
        
    def get_key(self):
        key_str = self.key_var.get().strip()
        if not key_str:
            # Si aucune clé n'est fournie, en générer une
            key = DES3.adjust_key_parity(get_random_bytes(24))
            key_str = base64.b64encode(key).decode('utf-8')
            self.key_var.set(key_str)
            return key
        
        try:
            # Essayer de décoder la clé depuis base64
            key = base64.b64decode(key_str)
            if len(key) != 24:
                raise ValueError("La clé doit faire 24 octets après décodage base64")
            return DES3.adjust_key_parity(key)
        except:
            # Si ce n'est pas du base64, utiliser la chaîne brute
            if len(key_str) != 24:
                messagebox.showerror("Erreur", "La clé doit faire exactement 24 caractères")
                return None
            return DES3.adjust_key_parity(key_str.encode('utf-8'))

    def encrypt(self):
        key = self.get_key()
        if not key:
            return
            
        plaintext = self.input_area.get("1.0", ctk.END).strip().encode('utf-8')
        if not plaintext:
            messagebox.showerror("Erreur", "Veuillez entrer un texte à chiffrer")
            return
            
        try:
            if self.mode_var.get() == "ECB":
                cipher = DES3.new(key, DES3.MODE_ECB)
                iv = b''  # Pas d'IV pour le mode ECB
            else:  # CBC
                iv = get_random_bytes(8)
                cipher = DES3.new(key, DES3.MODE_CBC, iv)
                
            # Ajouter du padding pour avoir une longueur multiple de 8
            padded_data = pad(plaintext, DES3.block_size)
            ciphertext = cipher.encrypt(padded_data)
            
            # Préfixer le IV pour le mode CBC
            if self.mode_var.get() == "CBC":
                result = iv + ciphertext
            else:
                result = ciphertext
                
            # Encoder en base64 pour l'affichage
            output = base64.b64encode(result).decode('utf-8')
            self.output_area.delete("1.0", ctk.END)
            self.output_area.insert("1.0", output)
            
        except Exception as e:
            messagebox.showerror("Erreur de chiffrement", str(e))

    def save_key(self):
        key = self.key_var.get().strip()
        if not key:
            messagebox.showerror("Erreur", "Aucune clé à sauvegarder")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".key",
            filetypes=[("Fichiers clé", "*.key"), ("Tous les fichiers", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(key)
                messagebox.showinfo("Succès", f"Clé sauvegardée dans {file_path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")

    def save_ciphertext(self):
        ciphertext = self.output_area.get("1.0", ctk.END).strip()
        if not ciphertext:
            messagebox.showerror("Erreur", "Aucun texte chiffré à sauvegarder")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".enc",
            filetypes=[("Fichiers chiffrés", "*.enc"), ("Tous les fichiers", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(ciphertext)
                messagebox.showinfo("Succès", f"Texte chiffré sauvegardé dans {file_path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")

    def clear(self):
        self.input_area.delete("1.0", ctk.END)
        self.output_area.delete("1.0", ctk.END)

if __name__ == "__main__":
    root = ctk.CTk()
    app = TripleDESEncryptor(root)
    root.mainloop()
