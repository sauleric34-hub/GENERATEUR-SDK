import yaml
import json
import os
import sys

class GuiGenerator:
    def __init__(self, spec_path):
        self.spec_path = spec_path
        with open(spec_path, 'r', encoding='utf-8') as f:
            if spec_path.endswith('.yaml') or spec_path.endswith('.yml'):
                self.spec = yaml.safe_load(f)
            else:
                self.spec = json.load(f)
        
        self.title = self.spec.get('info', {}).get('title', 'API SDK')
        # UTILISATION DE 127.0.0.1 AU LIEU DE LOCALHOST POUR PLUS DE COMPATIBILITÉ
        self.base_url = "https://127.0.0.1:5000/api/v1"

    def resolve_ref(self, ref):
        if not ref or not ref.startswith('#/'): return {}
        parts = ref.split('/')
        curr = self.spec
        for part in parts[1:]:
            curr = curr.get(part, {})
        return curr

    def get_props(self, schema):
        if '$ref' in schema:
            schema = self.resolve_ref(schema['$ref'])
        props = schema.get('properties', {})
        if 'allOf' in schema:
            for sub in schema['allOf']:
                props.update(self.get_props(sub))
        return props

    def generate(self, output_path):
        code = self._generate_header()
        code += self._generate_api_client()
        code += self._generate_ui_components()
        
        paths = self.spec.get('paths', {})
        tags = {}
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() not in ['get', 'post', 'put', 'delete']: continue
                tag = details.get('tags', ['General'])[0]
                if tag not in tags: tags[tag] = []
                
                req_body = details.get('requestBody', {})
                content = req_body.get('content', {})
                schema = content.get('application/json', {}).get('schema', {}) or content.get('multipart/form-data', {}).get('schema', {})
                details['resolved_props'] = self.get_props(schema)
                
                tags[tag].append({'path': path, 'method': method, 'details': details})

        code += self._generate_main_app(tags)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)
            
        # GÉNÉRATION AUTOMATIQUE DU REQUIREMENTS.TXT
        req_path = os.path.join(os.path.dirname(output_path), "requirements.txt")
        with open(req_path, 'w', encoding='utf-8') as f:
            f.write("flask\nflask-cors\nPyJWT\nrequests\nurllib3\npyopenssl\nPillow\n")

    def _generate_header(self):
        return f'''
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import threading
import os
import urllib3
from PIL import Image, ImageTk

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COLORS = {{
    "bg": "#0f172a",
    "card": "#1e293b",
    "accent": "#38bdf8",
    "success": "#22c55e",
    "danger": "#ef4444",
    "text": "#f8fafc",
    "text_muted": "#94a3b8"
}}

API_BASE = "{self.base_url}"
'''

    def _generate_api_client(self):
        return '''
class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.session = requests.Session()
        self.session.verify = False
    def set_token(self, token):
        self.token = token
    def request(self, method, endpoint, params=None, json_data=None, files=None):
        url = f"{self.base_url}{endpoint}"
        h = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        # TIMEOUT ROBUSTE POUR LES MACHINES LENTES
        return self.session.request(method, url, headers=h, params=params, json=json_data, files=files, timeout=120)
'''

    def _generate_ui_components(self):
        return '''
class ResultCard(tk.Label):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Attente d'analyse...", font=("Segoe UI", 11, "bold"), 
                         bg=COLORS["card"], fg=COLORS["text_muted"], padx=15, pady=15, **kwargs)
    def update_result(self, is_genuine, confidence, decision):
        c = COLORS["success"] if is_genuine else COLORS["danger"]
        self.config(text=f"{'✅' if is_genuine else '❌'} {decision}\\nConfiance : {confidence}%", bg=c, fg="white")

class ModernScrollFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg=COLORS["bg"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["bg"])
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

class EndpointFrame(tk.LabelFrame):
    def __init__(self, parent, title, method, path, details, client, console, on_auth_success=None):
        super().__init__(parent, text=f" {method.upper()} {path} ", font=("Segoe UI", 9, "bold"),
                         bg=COLORS["card"], fg=COLORS["accent"], padx=10, pady=10, borderwidth=0)
        self.client, self.path, self.method, self.details, self.console = client, path, method, details, console
        self.on_auth_success = on_auth_success
        self.entries, self.file_vars, self.result_card = {}, {}, None
        self._build_ui()

    def _build_ui(self):
        r = 0
        if "/detection" in self.path and self.method.upper() == "POST":
            self.result_card = ResultCard(self)
            self.result_card.grid(row=r, column=0, columnspan=2, sticky="ew", pady=(0, 10))
            r += 1
        
        props = self.details.get('resolved_props', {})
        for name, info in props.items():
            tk.Label(self, text=f"{name}:", bg=COLORS["card"], fg=COLORS["text"]).grid(row=r, column=0, sticky="e", pady=2)
            if info.get('format') == 'binary':
                v = tk.StringVar(value="Aucun fichier")
                ttk.Button(self, text="Parcourir...", command=lambda x=v: self._browse(x)).grid(row=r, column=1, sticky="w", padx=5)
                tk.Label(self, textvariable=v, bg=COLORS["card"], fg=COLORS["text_muted"], font=("Arial", 7)).grid(row=r+1, column=1, sticky="w")
                self.file_vars[name] = v
                r += 1
            else:
                ent = tk.Entry(self, width=30, bg=COLORS["bg"], fg="white", borderwidth=0)
                ent.grid(row=r, column=1, sticky="w", padx=5, pady=2)
                self.entries[name] = ent
            r += 1
        tk.Button(self, text="EXÉCUTER", bg=COLORS["accent"], fg="white", font=("Arial", 9, "bold"), command=self._execute).grid(row=r, column=0, columnspan=2, pady=10)

    def _browse(self, v):
        p = filedialog.askopenfilename()
        if p: v.set(p)

    def _execute(self):
        paths = {k: v.get() for k, v in self.file_vars.items() if os.path.exists(v.get())}
        body = {k: e.get() for k, e in self.entries.items()}
        def task():
            files = {k: open(p, 'rb') for k, p in paths.items()}
            try:
                res = self.client.request(self.method, self.path, json_data=body if body else None, files=files if files else None)
                if res and res.status_code in [200, 201]:
                    d = res.json()
                    if "/login" in self.path and "access_token" in d: 
                        self.client.set_token(d["access_token"])
                        if self.on_auth_success: self.after(0, self.on_auth_success)
                    if self.result_card and "decision" in d: 
                        self.after(0, lambda: self.result_card.update_result(d.get("is_genuine", False), d.get("confidence", 0), d.get("decision", "Inconnu")))
                self.console.log_response(self.method, self.path, res)
            except Exception as e:
                self.console.log_response(self.method, self.path, None, err=str(e))
            finally:
                for f in files.values(): f.close()
        threading.Thread(target=task, daemon=True).start()

class ResponseConsole(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg"])
        tk.Label(self, text=" CONSOLE DE SORTIE ", bg=COLORS["bg"], fg=COLORS["accent"]).pack(anchor="w")
        self.text = tk.Text(self, height=6, bg="black", fg="#00ff00", font=("Consolas", 9))
        self.text.pack(fill="both", expand=True)
    def log_response(self, m, p, res, err=None):
        self.text.insert("end", f">>> {m.upper()} {p}\\n")
        if err: self.text.insert("end", f"ERREUR: {err}\\n")
        elif not res: self.text.insert("end", "ERREUR DE CONNEXION\\n")
        else:
            try:
                js = json.dumps(res.json(), indent=2)
                self.text.insert("end", f"Statut: {res.status_code}\\n{js}\\n")
            except:
                self.text.insert("end", f"Statut: {res.status_code}\\n{res.text}\\n")
        self.text.see("end")
'''

    def _generate_main_app(self, tags):
        tags_json = json.dumps(tags)
        return f'''
{self._generate_ui_components()}

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SDK PREMIUM - {self.title}")
        self.geometry("1100x850")
        self.configure(bg=COLORS["bg"])
        self.client = ApiClient(API_BASE)
        s = ttk.Style()
        s.theme_use('clam')
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        self.console = ResponseConsole(self)
        self.console.pack(side="bottom", fill="x", padx=10, pady=5)
        
        data = json.loads({repr(tags_json)})
        self.tabs = []
        for tag, endpoints in data.items():
            tab = ModernScrollFrame(self.notebook)
            self.notebook.add(tab, text=tag)
            self.tabs.append(tab)
            for ep in endpoints:
                EndpointFrame(tab.scrollable_frame, "", ep['method'], ep['path'], ep['details'], self.client, self.console, self.unlock_tabs).pack(fill="x", pady=5)
        
        for i in range(1, len(self.tabs)):
            self.notebook.tab(i, state="disabled")

    def unlock_tabs(self):
        for i in range(len(self.tabs)):
            self.notebook.tab(i, state="normal")
        messagebox.showinfo("Sécurité", "Accès autorisé !")

if __name__ == "__main__":
    MainApp().mainloop()
'''

if __name__ == "__main__":
    gen = GuiGenerator(sys.argv[1])
    gen.generate(sys.argv[2] if len(sys.argv) > 2 else "generated_gui.py")
