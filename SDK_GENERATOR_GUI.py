import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess
import threading
import time

# Import existing generators
from gui_generator import GuiGenerator
from backend_generator import BackendGenerator

class SdkGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🚀 REST API Full-Stack Generator (ACID Edition)")
        self.geometry("600x450")
        self.configure(bg="#1a1a2e")
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#1a1a2e")
        self.style.configure("TLabel", background="#1a1a2e", foreground="#e0e0e0", font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10)
        self.style.configure("Header.TLabel", background="#1a1a2e", foreground="#00d2ff", font=("Segoe UI", 16, "bold"))
        
        self._build_ui()

    def _build_ui(self):
        main_frame = ttk.Frame(self, padding=30)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="🛠️ Générateur d'Écosystème API", style="Header.TLabel").pack(pady=(0, 20))
        
        ttk.Label(main_frame, text="Sélectionnez votre contrat OpenAPI (YAML ou JSON) :").pack(anchor="w")
        
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill="x", pady=10)
        
        self.path_var = tk.StringVar()
        self.entry_path = ttk.Entry(file_frame, textvariable=self.path_var, width=50)
        self.entry_path.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        ttk.Button(file_frame, text="Parcourir...", command=self._browse).pack(side="right")

        # Options
        self.check_run = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Lancer l'écosystème après génération", variable=self.check_run).pack(anchor="w", pady=10)

        # Action Button
        self.btn_generate = ttk.Button(main_frame, text="✨ GÉNÉRER & LANCER", command=self._start_process)
        self.btn_generate.pack(fill="x", pady=20)

        # Console Output
        self.console = tk.Text(main_frame, height=8, bg="#0d1117", fg="#58a6ff", font=("Consolas", 9), state="disabled")
        self.console.pack(fill="both", expand=True)

    def _log(self, message):
        self.console.config(state="normal")
        self.console.insert("end", f">>> {message}\n")
        self.console.see("end")
        self.console.config(state="disabled")
        self.update_idletasks()

    def _browse(self):
        path = filedialog.askopenfilename(filetypes=[("OpenAPI Files", "*.yaml *.yml *.json"), ("All Files", "*.*")])
        if path:
            self.path_var.set(path)

    def _start_process(self):
        spec_path = self.path_var.get()
        if not spec_path or not os.path.exists(spec_path):
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier OpenAPI valide.")
            return

        self.btn_generate.config(state="disabled")
        threading.Thread(target=self._generate_and_run, args=(spec_path,), daemon=True).start()

    def _generate_and_run(self, spec_path):
        try:
            self._log("Démarrage de la génération...")
            
            # 1. Frontend
            self._log("Génération du Frontend (Tkinter)...")
            gui_gen = GuiGenerator(spec_path)
            gui_gen.generate("generated_gui.py")
            
            # 2. Backend
            self._log("Génération du Backend (Flask ACID)...")
            back_gen = BackendGenerator(spec_path)
            back_gen.generate("generated_backend")

            self._log("✅ Génération terminée avec succès !")

            # 3. Installation dépendances
            self._log("Vérification des dépendances Python...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors", "PyJWT", "PyYAML", "pyopenssl", "requests", "urllib3"])
            self._log("✅ Dépendances à jour !")

            if self.check_run.get():
                self._log("🚀 Lancement de l'écosystème...")
                
                # Start Backend
                backend_script = os.path.join("generated_backend", "generated_app.py")
                subprocess.Popen([sys.executable, backend_script], cwd=".")
                
                self._log("⏳ Attente du serveur (3s)...")
                time.sleep(3)
                
                # Start Frontend
                self._log("Lancement du GUI...")
                subprocess.Popen([sys.executable, "generated_gui.py"])
                
                self._log("✨ Système opérationnel !")
                messagebox.showinfo("Succès", "L'écosystème a été généré et lancé !\nLe backend tourne en HTTPS sur le port 5000.")
            
        except Exception as e:
            self._log(f"❌ ERREUR : {str(e)}")
            messagebox.showerror("Erreur Critique", f"Une erreur est survenue :\n{e}")
        finally:
            self.btn_generate.config(state="normal")

if __name__ == "__main__":
    app = SdkGeneratorApp()
    app.mainloop()
