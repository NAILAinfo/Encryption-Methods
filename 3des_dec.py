import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad
import base64
import customtkinter as ctk

class TripleDESDecryptor:
    def __init__(self, root):
        self.root = root
        self.root.title("Déchiffrement Triple DES")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.key_var = tk.StringVar()
        self.input_text = tk.StringVar()
        self.output_text = tk.StringVar()
        self.mode_var = tk.StringVar(value="ECB")  # Mode par défaut
        
        # Style
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=('Arial', 10))
        
       # Frame principal
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)  # Ajoutez ici un espacement externe (padding)
        
        # Section clé
        key_frame = ctk.CTkFrame(main_frame)
        key_frame.pack(fill=ctk.X, pady=10)
        
        ctk.CTkLabel(key_frame, text="Clé Triple DES (charger ou coller):").pack(side=ctk.LEFT)
        key_entry = ctk.CTkEntry(key_frame, textvariable=self.key_var, width=30)
        key_entry.pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(key_frame, text="Charger clé", command=self.load_key).pack(side=ctk.LEFT)
        
       # Section mode de chiffrement
        mode_frame = ttk.Frame(main_frame)
        mode_frame.pack(fill=tk.X, pady=5)

        ttk.Label(mode_frame, text="Mode:").pack(side=tk.LEFT)
        modes = ["ECB", "CBC"]
        mode_combo = ctk.CTkComboBox(mode_frame, values=modes, state="readonly", width=5)
        mode_combo.set("ECB")  # Valeur par défaut
        mode_combo.pack(side=tk.LEFT, padx=5)
        # Section texte d'entrée
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill=ctk.BOTH, expand=True, pady=10)
        
        self.input_area = ctk.CTkTextbox(input_frame, height=8, width=40, wrap=ctk.WORD)
        self.input_area.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)
        
        # Section boutons
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill=ctk.X, pady=10)
        
        ctk.CTkButton(buttons_frame, text="Déchiffrer", command=self.decrypt).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(buttons_frame, text="Effacer", command=self.clear).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(buttons_frame, text="Charger texte chiffré", command=self.load_ciphertext).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(buttons_frame, text="Sauvegarder texte déchiffré", command=self.save_plaintext).pack(side=ctk.LEFT, padx=5)
        
        # Section texte de sortie
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(fill=ctk.BOTH, expand=True, pady=10)
        
        self.output_area = ctk.CTkTextbox(output_frame, height=8, width=40, wrap=ctk.WORD)
        self.output_area.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

    def load_key(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Fichiers clé", "*.key"), ("Tous les fichiers", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    key = f.read().strip()
                self.key_var.set(key)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement de la clé: {str(e)}")
    
    def load_ciphertext(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Fichiers chiffrés", "*.enc"), ("Tous les fichiers", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    ciphertext = f.read().strip()
                self.input_area.delete("1.0", ctk.END)
                self.input_area.insert("1.0", ciphertext)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement du texte chiffré: {str(e)}")
    
    def get_key(self):
        key_str = self.key_var.get().strip()
        if not key_str:
            messagebox.showerror("Erreur", "Veuillez entrer une clé")
            return None
        
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

    def decrypt(self):
        key = self.get_key()
        if not key:
            return
            
        try:
            # Décoder depuis base64
            ciphertext = base64.b64decode(self.input_area.get("1.0", ctk.END).strip())
            if not ciphertext:
                messagebox.showerror("Erreur", "Veuillez entrer un texte chiffré valide (encodé en base64)")
                return
                
            if self.mode_var.get() == "ECB":
                cipher = DES3.new(key, DES3.MODE_ECB)
                iv = b''  # Pas d'IV en mode ECB
            else:  # CBC
                # Extraire le IV des 8 premiers octets
                iv = ciphertext[:8]
                ciphertext = ciphertext[8:]
                cipher = DES3.new(key, DES3.MODE_CBC, iv)
                
            # Déchiffrer et enlever le padding
            padded_plaintext = cipher.decrypt(ciphertext)
            plaintext = unpad(padded_plaintext, DES3.block_size)
            
            # Afficher le résultat
            self.output_area.delete("1.0", ctk.END)
            self.output_area.insert("1.0", plaintext.decode('utf-8'))
            
        except Exception as e:
            messagebox.showerror("Erreur de déchiffrement", str(e))

    def save_plaintext(self):
        plaintext = self.output_area.get("1.0", ctk.END).strip()
        if not plaintext:
            messagebox.showerror("Erreur", "Aucun texte déchiffré à sauvegarder")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(plaintext)
                messagebox.showinfo("Succès", f"Texte déchiffré sauvegardé dans {file_path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")

    def clear(self):
        self.input_area.delete("1.0", ctk.END)
        self.output_area.delete("1.0", ctk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TripleDESDecryptor(root)
    root.mainloop()
