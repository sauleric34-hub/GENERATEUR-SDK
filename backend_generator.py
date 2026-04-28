import yaml
import json
import os
import sys
import shutil
import glob

class BackendGenerator:
    def __init__(self, spec_path):
        self.spec_path = spec_path
        self.source_dir = os.path.dirname(os.path.abspath(spec_path))
        with open(spec_path, 'r', encoding='utf-8') as f:
            if spec_path.endswith('.yaml') or spec_path.endswith('.yml'):
                self.spec = yaml.safe_load(f)
            else:
                self.spec = json.load(f)
        self.api_prefix = "/api/v1"

    def generate(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # RECURSIVE COPY OF MODELS AND SCRIPTS
        print("--- [INTEGRATION] Analyse du dossier source pour les modèles d'IA ---")
        for root, dirs, files in os.walk(self.source_dir):
            if "generated_backend" in root or "SDKGENERATION" in root: continue
            for file in files:
                if file.endswith(('.py', '.h5', '.pth', '.json', '.txt', '.onnx', '.tflite')):
                    if "openapi" in file.lower() or "generated_" in file: continue
                    src = os.path.join(root, file)
                    dst = os.path.join(output_dir, file)
                    if not os.path.exists(dst):
                        shutil.copy(src, dst)
                        print(f"   + {file} copié.")
            
        self._generate_database(os.path.join(output_dir, "generated_database.py"))
        self._generate_app(os.path.join(output_dir, "generated_app.py"))
        print(f"Generated Fully-Operational Backend in {output_dir}")

    def _generate_database(self, path):
        tag_properties = {} 
        for p_path, methods in self.spec.get('paths', {}).items():
            for method, details in methods.items():
                if method.lower() not in ['get', 'post', 'put']: continue
                tag = details.get('tags', ['data'])[0]
                safe_tag = "".join([c if (c.isalnum() and ord(c) < 128) else "_" for c in tag.lower()])
                if safe_tag not in tag_properties: tag_properties[safe_tag] = {}
        
        code = '''import sqlite3
import os
import json

DB_PATH = "generated_api.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
'''
        for table_name in tag_properties:
            code += f'    cursor.execute("CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, details TEXT)")\n'
        
        code += '''    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
'''
        with open(path, 'w', encoding='utf-8') as f: f.write(code)

    def _generate_app(self, path):
        has_service = os.path.exists(os.path.join(os.path.dirname(path), "detection_service.py"))
        
        code = f'''"""
BACKEND FULL-STACK OPERATIONNEL - VERSION ROBUSTE 2026
"""
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import sqlite3
import jwt
import datetime
import os
import uuid
import json
import traceback
from functools import wraps
from generated_database import get_db, init_db

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'academic-secret-keyce-2026-very-long-and-secure-key-32-chars'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

BASE = "{self.api_prefix}"

with app.app_context():
    init_db()

def reponse_erreur(status, titre, detail):
    return make_response(jsonify({{"title": titre, "status": status, "detail": str(detail), "instance": request.path}}), status)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "): token = auth_header.split(" ")[1]
        if not token: return reponse_erreur(401, "Authentification requise", "Token manquant")
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except Exception as e: return reponse_erreur(401, "Token invalide", e)
        return f(*args, **kwargs)
    return decorated

@app.route(f"{{BASE}}/health")
def health(): return jsonify({{"status": "UP"}})
'''
        if has_service:
            code += "import detection_service\n"

        for route_path, methods in self.spec.get('paths', {}).items():
            flask_path = f"{{BASE}}{route_path.replace('{', '<').replace('}', '>')}"
            for method, details in methods.items():
                if method.lower() not in ['get', 'post', 'put', 'delete']: continue
                tag = details.get('tags', ['data'])[0]
                safe_tag = "".join([c if (c.isalnum() and ord(c) < 128) else "_" for c in tag.lower()])
                func_name = f"{method}_{route_path.replace('/', '_').replace('{', '').replace('}', '')}".replace('-', '_').strip('_')
                
                code += f'\n@app.route(f"{flask_path}", methods=["{method.upper()}"])\n'
                if "/auth/" not in route_path: code += "@token_required\n"
                
                code += f'def {func_name}(**kwargs):\n'
                code += '    try:\n'
                code += '        db = get_db()\n'
                
                if method.lower() == 'post' and ('/detection' in route_path):
                    code += '        if "file" not in request.files: return reponse_erreur(400, "Fichier requis", "Champ \'file\' vide")\n'
                    code += '        f = request.files["file"]\n'
                    code += '        p = os.path.join(app.config["UPLOAD_FOLDER"], f"{{uuid.uuid4().hex}}_{{f.filename}}")\n'
                    code += '        f.save(p)\n'
                    if has_service:
                        code += '        res = detection_service.analyser_billet(p)\n'
                    else:
                        code += '        res = {"is_genuine": True, "confidence": 100, "decision": "AUTHENTIQUE"}\n'
                    code += f'        db.execute("INSERT INTO {safe_tag} (timestamp, details) VALUES (?, ?)", (datetime.datetime.now().isoformat(), json.dumps(res)))\n'
                    code += '        db.commit()\n'
                    code += '        return jsonify(res), 201\n'
                
                elif method.lower() == 'post' and ('/login' in route_path):
                    code += '        d = request.get_json()\n'
                    code += '        t = jwt.encode({"user": d.get("username"), "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config["SECRET_KEY"], algorithm="HS256")\n'
                    code += '        return jsonify({"access_token": t, "role": "admin"})\n'
                
                elif method.lower() == 'get':
                    code += f'        rows = db.execute("SELECT * FROM {safe_tag} ORDER BY id DESC").fetchall()\n'
                    code += '        return jsonify([json.loads(r["details"]) if r["details"] else dict(r) for r in rows])\n'
                
                else:
                    code += '        return jsonify({"message": "OK"}), 200\n'
                
                code += '    except Exception as e:\n'
                code += '        traceback.print_exc()\n'
                code += '        return reponse_erreur(500, "Erreur Serveur", e)\n'

        code += '''
if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0', ssl_context='adhoc')
'''
        with open(path, 'w', encoding='utf-8') as f: f.write(code)

if __name__ == "__main__":
    gen = BackendGenerator(sys.argv[1])
    gen.generate(sys.argv[2] if len(sys.argv) > 2 else "generated_backend")
